from datetime import date
from decimal import Decimal, InvalidOperation

from .database import get_connection, initialize_database
from .services import (
    add_transaction,
    edit_transaction,
    get_all_transactions,
    get_summary,
    get_transactions_by_category,
    remove_transaction,
)


def print_header() -> None:
    print()
    print("=" * 40)
    print("FINANCIAL MANAGER")
    print("=" * 40)


def print_menu() -> None:
    print()
    print("1. Register income")
    print("2. Register expense")
    print("3. List transactions")
    print("4. View financial summary")
    print("5. Filter by category")
    print("6. Edit transaction")
    print("7. Delete transaction")
    print("0. Exit")
    print()


def read_amount() -> Decimal:
    while True:
        value = input("Amount: ").strip()

        try:
            amount = Decimal(value)

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except InvalidOperation:
            print("Invalid amount. Example: 25.50")


def read_date() -> date:
    while True:
        value = input("Date (YYYY-MM-DD): ").strip()

        try:
            return date.fromisoformat(value)

        except ValueError:
            print("Invalid date. Example: 2026-09-30")


def create_transaction_flow(
    connection,
    transaction_type: str,
) -> None:
    print()
    print(f"REGISTER {transaction_type.upper()}")

    amount = read_amount()
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    transaction_date = read_date()

    try:
        transaction = add_transaction(
            connection=connection,
            transaction_type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=transaction_date,
        )

        print()
        print(f"Transaction created successfully. ID: {transaction.id}")

    except ValueError as error:
        print(f"Error: {error}")


def print_transaction(transaction) -> None:
    print(
        f"[{transaction.id}] "
        f"{transaction.transaction_date} | "
        f"{transaction.transaction_type.upper()} | "
        f"${transaction.amount:.2f} | "
        f"{transaction.category} | "
        f"{transaction.description}"
    )


def list_transactions_flow(connection) -> None:
    transactions = get_all_transactions(connection)

    print()
    print("TRANSACTIONS")
    print("-" * 40)

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print_transaction(transaction)


def summary_flow(connection) -> None:
    summary = get_summary(connection)

    print()
    print("FINANCIAL SUMMARY")
    print("-" * 40)
    print(f"Total income:   ${summary.total_income:.2f}")
    print(f"Total expenses: ${summary.total_expenses:.2f}")
    print(f"Balance:        ${summary.balance:.2f}")
    print(f"Transactions:   {summary.transaction_count}")


def category_filter_flow(connection) -> None:
    category = input("Category: ").strip()

    transactions = get_transactions_by_category(
        connection,
        category,
    )

    print()
    print(f"CATEGORY: {category}")
    print("-" * 40)

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print_transaction(transaction)


def edit_transaction_flow(connection) -> None:
    try:
        transaction_id = int(
            input("Transaction ID to edit: ").strip()
        )

        print("Enter the new transaction data.")

        transaction_type = input(
            "Type (income/expense): "
        ).strip().lower()

        amount = read_amount()
        category = input("Category: ").strip()
        description = input("Description: ").strip()
        transaction_date = read_date()

        transaction = edit_transaction(
            connection=connection,
            transaction_id=transaction_id,
            transaction_type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=transaction_date,
        )

        print()
        print("Transaction updated successfully.")
        print_transaction(transaction)

    except ValueError as error:
        print(f"Error: {error}")


def delete_transaction_flow(connection) -> None:
    try:
        transaction_id = int(
            input("Transaction ID to delete: ").strip()
        )

        confirmation = input(
            f"Delete transaction {transaction_id}? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        remove_transaction(
            connection,
            transaction_id,
        )

        print("Transaction deleted successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def run() -> None:
    initialize_database()

    with get_connection() as connection:

        while True:
            print_header()
            print_menu()

            option = input("Choose an option: ").strip()

            match option:
                case "1":
                    create_transaction_flow(
                        connection,
                        "income",
                    )

                case "2":
                    create_transaction_flow(
                        connection,
                        "expense",
                    )

                case "3":
                    list_transactions_flow(connection)

                case "4":
                    summary_flow(connection)

                case "5":
                    category_filter_flow(connection)

                case "6":
                    edit_transaction_flow(connection)

                case "7":
                    delete_transaction_flow(connection)

                case "0":
                    print()
                    print("Goodbye.")
                    break

                case _:
                    print("Invalid option.")


if __name__ == "__main__":
    run()