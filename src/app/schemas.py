from datetime import date
from pydantic import BaseModel, Field

class InboxTextIn(BaseModel):
    user_external_ref: str = Field(..., description="Ej: telegram user id")
    text: str

class InboxFileIn(BaseModel):
    user_external_ref: str

class DraftOut(BaseModel):
    id: int
    status: str
    kind: str | None
    txn_date: date | None
    currency: str
    amount: float | None
    merchant: str | None
    notes: str | None
    confidence: float

    
class DraftConfirmIn(BaseModel):
    kind: str
    txn_date: date
    currency: str = "HNL"
    amount: float
    merchant: str | None = None
    notes: str | None = None

    # nuevos:
    category_code: str | None = None
    debit_account_code: str | None = None
    credit_account_code: str | None = None


class PostingOut(BaseModel):
    transaction_id: int
    journal_entry_id: int
