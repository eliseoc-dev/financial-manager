import sqlite3
from datetime import date
from decimal import Decimal

from .models import Transaction
from .validators import validate_transaction


def _decimal_to_cents(amount: Decimal) -> int:
    return int(amount * 100)


def _row_to_transaction(row: sqlite3.Row) -> Transaction:
    return Transaction(
        id=row["id"],
        transaction_type=row["transaction_type"],
        amount=Decimal(row["amount_cents"]) / Decimal("100"),
        category=row["category"],
        description=row["description"],
        transaction_date=date.fromisoformat(row["transaction_date"]),
    )


def create_transaction(
    connection: sqlite3.Connection,
    transaction: Transaction,
) -> int:
    validate_transaction(
        transaction.transaction_type,
        transaction.amount,
        transaction.category,
        transaction.description,
        transaction.transaction_date,
    )

    cursor = connection.execute(
        """
        INSERT INTO transactions (
            transaction_type,
            amount_cents,
            category,
            description,
            transaction_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            transaction.transaction_type,
            _decimal_to_cents(transaction.amount),
            transaction.category.strip(),
            transaction.description.strip(),
            transaction.transaction_date.isoformat(),
        ),
    )

    connection.commit()
    return cursor.lastrowid


def get_transaction(
    connection: sqlite3.Connection,
    transaction_id: int,
) -> Transaction | None:
    row = connection.execute(
        """
        SELECT
            id,
            transaction_type,
            amount_cents,
            category,
            description,
            transaction_date
        FROM transactions
        WHERE id = ?
        """,
        (transaction_id,),
    ).fetchone()

    if row is None:
        return None

    return _row_to_transaction(row)


def list_transactions(
    connection: sqlite3.Connection,
) -> list[Transaction]:
    rows = connection.execute(
        """
        SELECT
            id,
            transaction_type,
            amount_cents,
            category,
            description,
            transaction_date
        FROM transactions
        ORDER BY transaction_date DESC, id DESC
        """
    ).fetchall()

    return [_row_to_transaction(row) for row in rows]


def update_transaction(
    connection: sqlite3.Connection,
    transaction: Transaction,
) -> None:
    if transaction.id is None:
        raise ValueError("Transaction ID is required for update.")

    validate_transaction(
        transaction.transaction_type,
        transaction.amount,
        transaction.category,
        transaction.description,
        transaction.transaction_date,
    )

    cursor = connection.execute(
        """
        UPDATE transactions
        SET
            transaction_type = ?,
            amount_cents = ?,
            category = ?,
            description = ?,
            transaction_date = ?
        WHERE id = ?
        """,
        (
            transaction.transaction_type,
            _decimal_to_cents(transaction.amount),
            transaction.category.strip(),
            transaction.description.strip(),
            transaction.transaction_date.isoformat(),
            transaction.id,
        ),
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise ValueError("Transaction not found.")


def delete_transaction(
    connection: sqlite3.Connection,
    transaction_id: int,
) -> None:
    cursor = connection.execute(
        """
        DELETE FROM transactions
        WHERE id = ?
        """,
        (transaction_id,),
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise ValueError("Transaction not found.")