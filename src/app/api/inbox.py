import os
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import get_db
from ..config import settings
from ..models import User, InboxItem, InboxType, TransactionDraft
from ..schemas import InboxTextIn, DraftOut
from ..services.llm_adapter import MultimodalLLMAdapter

router = APIRouter(prefix="/inbox", tags=["inbox"])
llm = MultimodalLLMAdapter()

def _auth(x_api_key: str | None):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

def _get_or_create_user(db: Session, external_ref: str) -> User:
    u = db.query(User).filter(User.external_ref == external_ref).one_or_none()
    if u:
        return u
    u = User(external_ref=external_ref)
    db.add(u)
    db.flush()
    return u

@router.post("/text", response_model=DraftOut)
def inbox_text(payload: InboxTextIn, db: Session = Depends(get_db), x_api_key: str | None = Header(default=None)):
    _auth(x_api_key)
    user = _get_or_create_user(db, payload.user_external_ref)

    inbox = InboxItem(user_id=user.id, type=InboxType.TEXT, raw_text=payload.text)
    db.add(inbox)
    db.flush()

    draft_llm = llm.parse(text=payload.text, file_path=None, file_mime=None)
    draft = TransactionDraft(
        inbox_id=inbox.id,
        status="needs_info" if draft_llm.missing_fields else "pending",
        kind=draft_llm.kind,
        txn_date=draft_llm.txn_date,
        currency=draft_llm.currency,
        amount=draft_llm.amount,
        merchant=draft_llm.merchant,
        notes=draft_llm.notes,
        confidence=draft_llm.confidence,
        missing_fields=",".join(draft_llm.missing_fields) if draft_llm.missing_fields else None,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)

    return DraftOut(
        id=draft.id,
        status=draft.status,
        kind=draft.kind,
        txn_date=draft.txn_date,
        currency=draft.currency,
        amount=float(draft.amount) if draft.amount is not None else None,
        merchant=draft.merchant,
        notes=draft.notes,
        confidence=float(draft.confidence),
    )

@router.post("/file", response_model=DraftOut)
async def inbox_file(
    user_external_ref: str = Form(...),
    upload: UploadFile = File(...),
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None),
):
    _auth(x_api_key)
    user = _get_or_create_user(db, user_external_ref)

    os.makedirs(settings.storage_dir, exist_ok=True)
    ext = os.path.splitext(upload.filename or "")[1]
    fname = f"{uuid4().hex}{ext}"
    fpath = os.path.join(settings.storage_dir, fname)

    with open(fpath, "wb") as f:
        f.write(await upload.read())

    inbox = InboxItem(
        user_id=user.id,
        type=InboxType.FILE,
        raw_text=None,
        file_path=fpath,
        file_mime=upload.content_type
    )
    db.add(inbox)
    db.flush()

    draft_llm = llm.parse(text=None, file_path=fpath, file_mime=upload.content_type)
    draft = TransactionDraft(
        inbox_id=inbox.id,
        status="needs_info" if draft_llm.missing_fields else "pending",
        kind=draft_llm.kind,
        txn_date=draft_llm.txn_date,
        currency=draft_llm.currency,
        amount=draft_llm.amount,
        merchant=draft_llm.merchant,
        notes=draft_llm.notes,
        confidence=draft_llm.confidence,
        missing_fields=",".join(draft_llm.missing_fields) if draft_llm.missing_fields else None,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)

    return DraftOut(
        id=draft.id,
        status=draft.status,
        kind=draft.kind,
        txn_date=draft.txn_date,
        currency=draft.currency,
        amount=float(draft.amount) if draft.amount is not None else None,
        merchant=draft.merchant,
        notes=draft.notes,
        confidence=float(draft.confidence),
    )
