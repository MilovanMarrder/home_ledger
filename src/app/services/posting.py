from datetime import date
from sqlalchemy.orm import Session
from ..models import Transaction, JournalEntry, JournalLine, Account

class PostingError(Exception):
    pass

def _get_account_by_code(db: Session, code: str) -> Account:
    acct = db.query(Account).filter(Account.code == code, Account.is_active == True).one_or_none()
    if not acct:
        raise PostingError(f"Cuenta contable no encontrada: {code}")
    return acct

def post_double_entry(
    db: Session,
    *,
    txn: Transaction,
    debit_account_code: str,
    credit_account_code: str,
    memo: str | None = None
) -> JournalEntry:
    dr = _get_account_by_code(db, debit_account_code)
    cr = _get_account_by_code(db, credit_account_code)

    entry = JournalEntry(
        txn_id=txn.id,
        entry_date=txn.txn_date,
        memo=memo
    )
    entry.lines = [
        JournalLine(account_id=dr.id, debit=txn.amount, credit=0),
        JournalLine(account_id=cr.id, debit=0, credit=txn.amount),
    ]
    db.add(entry)
    txn.posted = True
    db.add(txn)
    return entry
