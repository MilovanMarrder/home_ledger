import re
from datetime import date
from dataclasses import dataclass

@dataclass
class LLMDraft:
    kind: str | None
    txn_date: date | None
    currency: str
    amount: float | None
    merchant: str | None
    notes: str | None
    confidence: float
    missing_fields: list[str]

class MultimodalLLMAdapter:

    def parse(self, *, text: str | None, file_path: str | None, file_mime: str | None) -> LLMDraft:

        if not text:
            return LLMDraft(
                kind=None,
                txn_date=None,
                currency="HNL",
                amount=None,
                merchant=None,
                notes=None,
                confidence=0.0,
                missing_fields=["kind", "amount"]
            )

        lower = text.lower()

        # ---- Detectar tipo ----
        if any(word in lower for word in ["gasto", "compré", "pagué"]):
            kind = "expense"
        elif any(word in lower for word in ["ingreso", "recibí"]):
            kind = "income"
        else:
            kind = None

        # ---- Detectar monto (soporta 250, 250.50, L 250, 250lps, etc) ----
        amount = None
        amount_match = re.search(r"(\d+[.,]?\d*)", lower)
        if amount_match:
            amount = float(amount_match.group(1).replace(",", "."))

        # ---- Detectar comercio simple ----
        merchant = None
        if "colonia" in lower:
            merchant = "Supermercado La Colonia"
        elif "walmart" in lower:
            merchant = "Walmart"
        elif "texaco" in lower:
            merchant = "Texaco"

        missing = []
        if not kind:
            missing.append("kind")
        if not amount:
            missing.append("amount")

        return LLMDraft(
            kind=kind,
            txn_date=None,
            currency="HNL",
            amount=amount,
            merchant=merchant,
            notes=text,
            confidence=0.7 if kind and amount else 0.3,
            missing_fields=missing
        )
