import sqlite3
from datetime import date
from decimal import Decimal

import pytest

from financial_manager.services import (
    add_transaction,
    edit_transaction,
    get_transactions_by_category,
    get_transactions_by_date_range,
    get_transactions_by_type,
    remove_transaction,
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


def test_add_transaction():
    connection = create_test_connection()

    transaction = add_transaction(
        connection,
        transaction_type="income",
        amount=Decimal("1200.00"),
        category="Salary",
        description="Monthly payment",
        transaction_date=date(2026, 9, 30),
    )

    assert transaction.id == 1
    assert transaction.amount == Decimal("1200.00")

    connection.close()


def test_edit_transaction():
    connection = create_test_connection()

    transaction = add_transaction(
        connection,
        transaction_type="expense",
        amount=Decimal("20.00"),
        category="Food",
        description="Lunch",
        transaction_date=date(2026, 9, 30),
    )

    updated = edit_transaction(
        connection,
        transaction_id=transaction.id,
        transaction_type="expense",
        amount=Decimal("35.00"),
        category="Transport",
        description="Taxi",
        transaction_date=date(2026, 9, 30),
    )

    assert updated.amount == Decimal("35.00")
    assert updated.category == "Transport"

    connection.close()


def test_remove_transaction():
    connection = create_test_connection()

    transaction = add_transaction(
        connection,
        transaction_type="expense",
        amount=Decimal("10.00"),
        category="Food",
        description="Snack",
        transaction_date=date(2026, 9, 30),
    )

    remove_transaction(connection, transaction.id)

    with pytest.raises(ValueError):
        remove_transaction(connection, transaction.id)

    connection.close()


def test_filter_by_type():
    connection = create_test_connection()

    add_transaction(
        connection,
        "income",
        Decimal("1000.00"),
        "Salary",
        "Salary",
        date(2026, 9, 30),
    )

    add_transaction(
        connection,
        "expense",
        Decimal("100.00"),
        "Food",
        "Groceries",
        date(2026, 9, 30),
    )

    results = get_transactions_by_type(connection, "expense")

    assert len(results) == 1
    assert results[0].transaction_type == "expense"

    connection.close()


def test_filter_by_category():
    connection = create_test_connection()

    add_transaction(
        connection,
        "expense",
        Decimal("20.00"),
        "Food",
        "Lunch",
        date(2026, 9, 30),
    )

    add_transaction(
        connection,
        "expense",
        Decimal("30.00"),
        "Transport",
        "Taxi",
        date(2026, 9, 30),
    )

    results = get_transactions_by_category(connection, "Food")

    assert len(results) == 1
    assert results[0].category == "Food"

    connection.close()


def test_filter_by_date_range():
    connection = create_test_connection()

    add_transaction(
        connection,
        "income",
        Decimal("500.00"),
        "Freelance",
        "Project",
        date(2026, 9, 20),
    )

    add_transaction(
        connection,
        "expense",
        Decimal("50.00"),
        "Food",
        "Dinner",
        date(2026, 9, 30),
    )

    results = get_transactions_by_date_range(
        connection,
        date(2026, 9, 25),
        date(2026, 9, 30),
    )

    assert len(results) == 1
    assert results[0].description == "Dinner"

    connection.close()


def test_invalid_date_range():
    connection = create_test_connection()

    with pytest.raises(ValueError):
        get_transactions_by_date_range(
            connection,
            date(2026, 10, 1),
            date(2026, 9, 1),
        )

    connection.close()