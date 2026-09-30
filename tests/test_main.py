from datetime import date
from decimal import Decimal

import pytest

from financial_manager.validators import validate_transaction

def test_valid_transaction():
    validate_transaction(
        transaction_type="income",
        amount=Decimal("1500.00"),
        category="Salary",
        description="Monthly salary",
        transaction_date=date(2026, 9, 29),
    )


def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        validate_transaction(
            transaction_type="other",
            amount=Decimal("100.00"),
            category="Test",
            description="Invalid type",
            transaction_date=date(2026, 9, 29),
        )


def test_invalid_amount():
    with pytest.raises(ValueError):
        validate_transaction(
            transaction_type="expense",
            amount=Decimal("0"),
            category="Food",
            description="Invalid amount",
            transaction_date=date(2026, 9, 29),
        )


def test_empty_category():
    with pytest.raises(ValueError):
        validate_transaction(
            transaction_type="expense",
            amount=Decimal("25.00"),
            category="",
            description="Invalid category",
            transaction_date=date(2026, 9, 29),
        )


def test_empty_description():
    with pytest.raises(ValueError):
        validate_transaction(
            transaction_type="expense",
            amount=Decimal("25.00"),
            category="Food",
            description="",
            transaction_date=date(2026, 9, 29),
        )