import sqlite3
from datetime import date
from decimal import Decimal

from financial_manager.repository import (
    create_transaction,
    delete_transaction,
    get_transaction,
    list_transactions,
    update_transaction,
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


def test_create_transaction():
    connection = create_test_connection()

    transaction_id = create_transaction(
        connection,
        __import__(
            "financial_manager.models",
            fromlist=["Transaction"],
        ).Transaction(
            id=None,
            transaction_type="income",
            amount=Decimal("1500.50"),
            category="Salary",
            description="Monthly salary",
            transaction_date=date(2026, 9, 30),
        ),
    )

    assert transaction_id == 1

    connection.close()


def test_get_transaction():
    connection = create_test_connection()

    from financial_manager.models import Transaction

    transaction_id = create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("25.50"),
            category="Food",
            description="Lunch",
            transaction_date=date(2026, 9, 30),
        ),
    )

    transaction = get_transaction(connection, transaction_id)

    assert transaction is not None
    assert transaction.amount == Decimal("25.50")
    assert transaction.category == "Food"

    connection.close()


def test_list_transactions():
    connection = create_test_connection()

    from financial_manager.models import Transaction

    create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="income",
            amount=Decimal("1000.00"),
            category="Salary",
            description="Salary",
            transaction_date=date(2026, 9, 29),
        ),
    )

    create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("100.00"),
            category="Food",
            description="Groceries",
            transaction_date=date(2026, 9, 30),
        ),
    )

    transactions = list_transactions(connection)

    assert len(transactions) == 2
    assert transactions[0].category == "Food"

    connection.close()


def test_update_transaction():
    connection = create_test_connection()

    from financial_manager.models import Transaction

    transaction_id = create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("50.00"),
            category="Food",
            description="Lunch",
            transaction_date=date(2026, 9, 30),
        ),
    )

    updated_transaction = Transaction(
        id=transaction_id,
        transaction_type="expense",
        amount=Decimal("75.00"),
        category="Transport",
        description="Taxi",
        transaction_date=date(2026, 9, 30),
    )

    update_transaction(connection, updated_transaction)

    transaction = get_transaction(connection, transaction_id)

    assert transaction is not None
    assert transaction.amount == Decimal("75.00")
    assert transaction.category == "Transport"

    connection.close()


def test_delete_transaction():
    connection = create_test_connection()

    from financial_manager.models import Transaction

    transaction_id = create_transaction(
        connection,
        Transaction(
            id=None,
            transaction_type="expense",
            amount=Decimal("30.00"),
            category="Food",
            description="Dinner",
            transaction_date=date(2026, 9, 30),
        ),
    )

    delete_transaction(connection, transaction_id)

    transaction = get_transaction(connection, transaction_id)

    assert transaction is None

    connection.close()