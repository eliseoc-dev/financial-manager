import sqlite3
from datetime import date
from decimal import Decimal

from .models import FinancialSummary, Transaction
from .repository import (
    create_transaction,
    delete_transaction,
    get_financial_summary,
    get_transaction,
    list_transactions,
    update_transaction,
    filter_transactions_by_category,
    filter_transactions_by_date_range,
    filter_transactions_by_type
)


def add_transaction(
    connection: sqlite3.Connection,
    transaction_type: str,
    amount: Decimal,
    category: str,
    description: str,
    transaction_date: date,
) -> Transaction:
    transaction = Transaction(
        id=None,
        transaction_type=transaction_type,
        amount=amount,
        category=category,
        description=description,
        transaction_date=transaction_date,
    )

    transaction_id = create_transaction(connection, transaction)

    created_transaction = get_transaction(connection, transaction_id)

    if created_transaction is None:
        raise RuntimeError("Transaction was created but could not be retrieved.")

    return created_transaction


def edit_transaction(
    connection: sqlite3.Connection,
    transaction_id: int,
    transaction_type: str,
    amount: Decimal,
    category: str,
    description: str,
    transaction_date: date,
) -> Transaction:
    existing_transaction = get_transaction(connection, transaction_id)

    if existing_transaction is None:
        raise ValueError("Transaction not found.")

    updated_transaction = Transaction(
        id=transaction_id,
        transaction_type=transaction_type,
        amount=amount,
        category=category,
        description=description,
        transaction_date=transaction_date,
    )

    update_transaction(connection, updated_transaction)

    result = get_transaction(connection, transaction_id)

    if result is None:
        raise RuntimeError("Transaction was updated but could not be retrieved.")

    return result


def remove_transaction(
    connection: sqlite3.Connection,
    transaction_id: int,
) -> None:
    existing_transaction = get_transaction(connection, transaction_id)

    if existing_transaction is None:
        raise ValueError("Transaction not found.")

    delete_transaction(connection, transaction_id)


def get_all_transactions(
    connection: sqlite3.Connection,
) -> list[Transaction]:
    return list_transactions(connection)


def get_summary(
    connection: sqlite3.Connection,
) -> FinancialSummary:
    return get_financial_summary(connection)


def get_transactions_by_type(
    connection: sqlite3.Connection,
    transaction_type: str,
) -> list[Transaction]:
    return filter_transactions_by_type(connection, transaction_type)


def get_transactions_by_category(
    connection: sqlite3.Connection,
    category: str,
) -> list[Transaction]:
    return filter_transactions_by_category(connection, category)


def get_transactions_by_date_range(
    connection: sqlite3.Connection,
    start_date: date,
    end_date: date,
) -> list[Transaction]:
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date.")

    return filter_transactions_by_date_range(
        connection,
        start_date,
        end_date,
    )