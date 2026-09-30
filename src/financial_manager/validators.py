from datetime import date
from decimal import Decimal


VALID_TRANSACTION_TYPES = {"income", "expense"}


def validate_transaction_type(transaction_type: str) -> None:
    if transaction_type not in VALID_TRANSACTION_TYPES:
        raise ValueError("Transaction type must be 'income' or 'expense'.")


def validate_amount(amount: Decimal) -> None:
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")


def validate_category(category: str) -> None:
    if not category.strip():
        raise ValueError("Category cannot be empty.")


def validate_description(description: str) -> None:
    if not description.strip():
        raise ValueError("Description cannot be empty.")


def validate_transaction_date(transaction_date: date) -> None:
    if not isinstance(transaction_date, date):
        raise ValueError("Transaction date must be a valid date.")


def validate_transaction(
    transaction_type: str,
    amount: Decimal,
    category: str,
    description: str,
    transaction_date: date,
) -> None:
    validate_transaction_type(transaction_type)
    validate_amount(amount)
    validate_category(category)
    validate_description(description)
    validate_transaction_date(transaction_date)