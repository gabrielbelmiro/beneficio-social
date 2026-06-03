import re
from decimal import Decimal


BENEFIT_INCOME_LIMIT = Decimal("2500.00")


def normalize_money(value: str) -> Decimal:
    clean = value.replace(".", "").replace(",", ".")
    return Decimal(clean)


def extract_income(text: str) -> Decimal | None:
    patterns = [
        r"renda mensal[:\s]*R?\$?\s*([\d\.]+,\d{2})",
        r"sal[aá]rio[:\s]*R?\$?\s*([\d\.]+,\d{2})",
        r"rendimentos[:\s]*R?\$?\s*([\d\.]+,\d{2})",
        r"total[:\s]*R?\$?\s*([\d\.]+,\d{2})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return normalize_money(match.group(1))

    return None


def classify_income(text: str) -> dict:
    income = extract_income(text)

    if income is None:
        return {
            "status": "INCONCLUSIVE",
            "reason": "Não foi possível identificar a renda no documento.",
            "income": None,
            "confidence": 0.45
        }

    if income <= BENEFIT_INCOME_LIMIT:
        return {
            "status": "APPROVED",
            "reason": "Renda dentro do limite permitido.",
            "income": str(income),
            "confidence": 0.90
        }

    return {
        "status": "REJECTED",
        "reason": "Renda acima do limite permitido.",
        "income": str(income),
        "confidence": 0.90
    }