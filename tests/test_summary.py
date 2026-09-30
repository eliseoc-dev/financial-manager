import sqlite3
from datetime import date
from decimal import Decimal

from financial_manager.models import Transaction
from financial_manager.repository import (
    create_transaction,
    get_expenses_by_category,
    get_financial_summary,
)


def create_test_connection():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    connection.execute(
        """
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            transaction_date TEXT NOT NULL
        )
        """
    )

    connection.commit()

    return connection


def test_financial_summary():
    connection = create_test_connection()

    create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="income",
            amount=Decimal("1500.00"),
            category="Salary",
            description="Monthly salary",
            transaction_date=date(2026, 9, 30),
        ),
    )

    create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("200.00"),
            category="Food",
            description="Groceries",
            transaction_date=date(2026, 9, 30),
        ),
    )

    create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("100.00"),
            category="Transport",
            description="Transport expenses",
            transaction_date=date(2026, 9, 30),
        ),
    )

    summary = get_financial_summary(connection)

    assert summary.total_income == Decimal("1500.00")
    assert summary.total_expenses == Decimal("300.00")
    assert summary.balance == Decimal("1200.00")
    assert summary.transaction_count == 3

    connection.close()


def test_empty_financial_summary():
    connection = create_test_connection()

    summary = get_financial_summary(connection)

    assert summary.total_income == Decimal("0")
    assert summary.total_expenses == Decimal("0")
    assert summary.balance == Decimal("0")
    assert summary.transaction_count == 0

    connection.close()


def test_expenses_grouped_by_category():
    connection = create_test_connection()

    transactions = [
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("20.00"),
            category="Food",
            description="Lunch",
            transaction_date=date(2026, 9, 30),
        ),
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("30.00"),
            category="Food",
            description="Dinner",
            transaction_date=date(2026, 9, 30),
        ),
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("15.00"),
            category="Transport",
            description="Taxi",
            transaction_date=date(2026, 9, 30),
        ),
    ]

    for transaction in transactions:
        create_transaction(connection, transaction)

    categories = get_expenses_by_category(connection)

    assert len(categories) == 2

    assert categories[0].category == "Food"
    assert categories[0].total == Decimal("50.00")
    assert categories[0].transaction_count == 2

    assert categories[1].category == "Transport"
    assert categories[1].total == Decimal("15.00")
    assert categories[1].transaction_count == 1

    connection.close()