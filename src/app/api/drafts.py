from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import get_db
from ..config import settings
from ..models import TransactionDraft, Transaction, InboxItem, User, Category
from ..schemas import DraftConfirmIn, PostingOut
from ..services.posting import post_double_entry

router = APIRouter(prefix="/drafts", tags=["drafts"])

def _auth(x_api_key: str | None):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

@router.post("/{draft_id}/confirm", response_model=PostingOut)
def confirm_and_post(
    draft_id: int,
    body: DraftConfirmIn,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None),
):
    _auth(x_api_key)

    draft = db.query(TransactionDraft).filter(TransactionDraft.id == draft_id).one_or_none()
    if not draft:
        raise HTTPException(404, "Draft not found")

    inbox = db.query(InboxItem).filter(InboxItem.id == draft.inbox_id).one()
    user = db.query(User).filter(User.id == inbox.user_id).one()

    txn = Transaction(
        inbox_id=inbox.id,
        user_id=user.id,
        kind=body.kind,
        txn_date=body.txn_date,
        currency=body.currency,
        amount=body.amount,
        merchant=body.merchant,
        notes=body.notes,
        posted=False
    )
    db.add(txn)
    db.flush()

    # MVP: regla simple por kind → (dr, cr)
    # Determinar dr/cr
    dr = body.debit_account_code
    cr = body.credit_account_code

    if not dr or not cr:
        if body.category_code:
            cat = _get_category(db, body.category_code)
            dr = cat.default_debit_account_code
            cr = cat.default_credit_account_code

    if not dr or not cr:
        raise HTTPException(400, "Missing debit_account_code/credit_account_code or category_code mapping")

    entry = post_double_entry(db, txn=txn, debit_account_code=dr, credit_account_code=cr, memo=body.notes)
    draft.status = "confirmed"
    db.add(draft)

    db.commit()
    return PostingOut(transaction_id=txn.id, journal_entry_id=entry.id)

def _get_category(db: Session, code: str) -> Category:
    cat = db.query(Category).filter(Category.code == code, Category.is_active == True).one_or_none()
    if not cat:
        raise HTTPException(400, f"Category not found: {code}")
    return cat