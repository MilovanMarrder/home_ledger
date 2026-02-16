import enum
from datetime import datetime, date
from sqlalchemy import (
    String, Integer, DateTime, Date, Numeric, ForeignKey, Boolean, Text,
    Enum, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class InboxType(str, enum.Enum):
    TEXT = "text"
    FILE = "file"

class DraftStatus(str, enum.Enum):
    PENDING = "pending"
    NEEDS_INFO = "needs_info"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

class TxnKind(str, enum.Enum):
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"
    PAYMENT_CC = "payment_cc"
    LOAN = "loan"
    ADJUSTMENT = "adjustment"

class AccountType(str, enum.Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    INCOME = "income"
    EXPENSE = "expense"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_ref: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)  # telegram user id etc
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True)        # ej: 1.1.02
    name: Mapped[str] = mapped_column(String(120))
    type: Mapped[AccountType] = mapped_column(Enum(AccountType))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True)   # ej: EXP.FOOD.GROCERY
    name: Mapped[str] = mapped_column(String(140))
    kind: Mapped[str] = mapped_column(String(20))               # expense | income | transfer
    group: Mapped[str | None] = mapped_column(String(80), nullable=True)
    subgroup: Mapped[str | None] = mapped_column(String(80), nullable=True)
    default_debit_account_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    default_credit_account_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True)  # CSV simple (MVP)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class InboxItem(Base):
    __tablename__ = "inbox_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[InboxType] = mapped_column(Enum(InboxType))
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_mime: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class TransactionDraft(Base):
    __tablename__ = "transaction_drafts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inbox_id: Mapped[int] = mapped_column(ForeignKey("inbox_items.id"), unique=True)
    status: Mapped[DraftStatus] = mapped_column(Enum(DraftStatus), default=DraftStatus.PENDING)
    kind: Mapped[TxnKind | None] = mapped_column(Enum(TxnKind), nullable=True)
    txn_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="HNL")
    amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    merchant: Mapped[str | None] = mapped_column(String(180), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Numeric(4, 3), default=0.0)
    missing_fields: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string simple (MVP)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    inbox = relationship("InboxItem")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inbox_id: Mapped[int] = mapped_column(ForeignKey("inbox_items.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    kind: Mapped[TxnKind] = mapped_column(Enum(TxnKind))
    txn_date: Mapped[date] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String(10), default="HNL")
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    merchant: Mapped[str | None] = mapped_column(String(180), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    posted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    inbox = relationship("InboxItem")
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    category = relationship("Category")


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    txn_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), unique=True)
    entry_date: Mapped[date] = mapped_column(Date)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    txn = relationship("Transaction")
    lines = relationship(
    "JournalLine",
    back_populates="entry",
    cascade="all, delete-orphan"
)


class JournalLine(Base):
    __tablename__ = "journal_lines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    debit: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    credit: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    entry = relationship(
    "JournalEntry",
    back_populates="lines"
)


    account = relationship("Account")

    __table_args__ = (
        UniqueConstraint("entry_id", "account_id", "debit", "credit", name="uq_line_dedupe"),
    )
