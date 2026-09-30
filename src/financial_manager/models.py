from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Transaction:
    id: int | None
    transaction_type: str
    amount: Decimal
    category: str
    description: str
    transaction_date: date