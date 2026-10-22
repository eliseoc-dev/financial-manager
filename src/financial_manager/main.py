from datetime import date
from decimal import Decimal, InvalidOperation

from .database import get_connection, initialize_database
from .services import (
    add_transaction,
    edit_transaction,
    get_all_transactions,
    get_summary,
    get_transactions_by_category,
    get_transactions_by_date_range,
    get_transactions_by_type,
    remove_transaction,
)


def print_header() -> None:
    print()
    print("=" * 50)
    print("FINANCIAL MANAGER")
    print("=" * 50)


def print_menu() -> None:
    print()
    print("1. Register income")
    print("2. Register expense")
    print("3. List transactions")
    print("4. View financial summary")
    print("5. Filter transactions")
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


def read_date(prompt: str = "Date (YYYY-MM-DD): ") -> date:
    while True:
        value = input(prompt).strip()

        try:
            return date.fromisoformat(value)

        except ValueError:
            print("Invalid date. Example: 2026-09-30")


def read_transaction_id(prompt: str) -> int:
    while True:
        value = input(prompt).strip()

        try:
            transaction_id = int(value)

            if transaction_id <= 0:
                print("ID must be greater than zero.")
                continue

            return transaction_id

        except ValueError:
            print("Invalid ID. Enter a number.")


def read_transaction_type() -> str:
    while True:
        transaction_type = input(
            "Type (income/expense): "
        ).strip().lower()

        if transaction_type in {"income", "expense"}:
            return transaction_type

        print("Invalid type. Use 'income' or 'expense'.")


def print_transaction(transaction) -> None:
    print(
        f"[{transaction.id}] "
        f"{transaction.transaction_date} | "
        f"{transaction.transaction_type.upper()} | "
        f"${transaction.amount:.2f} | "
        f"{transaction.category} | "
        f"{transaction.description}"
    )


def print_transactions(
    transactions,
    title: str = "TRANSACTIONS",
) -> None:
    print()
    print(title)
    print("-" * 50)

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print_transaction(transaction)


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
        print(
            "Transaction created successfully. "
            f"ID: {transaction.id}"
        )

    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")


def list_transactions_flow(connection) -> None:
    transactions = get_all_transactions(
        connection
    )

    print_transactions(
        transactions,
        "ALL TRANSACTIONS",
    )


def summary_flow(connection) -> None:
    summary = get_summary(connection)

    print()
    print("FINANCIAL SUMMARY")
    print("-" * 50)
    print(
        f"Total income:   "
        f"${summary.total_income:.2f}"
    )
    print(
        f"Total expenses: "
        f"${summary.total_expenses:.2f}"
    )
    print(
        f"Balance:        "
        f"${summary.balance:.2f}"
    )
    print(
        f"Transactions:   "
        f"{summary.transaction_count}"
    )


def category_filter_flow(connection) -> None:
    category = input(
        "Category: "
    ).strip()

    if not category:
        print("Category cannot be empty.")
        return

    transactions = get_transactions_by_category(
        connection,
        category,
    )

    print_transactions(
        transactions,
        f"CATEGORY: {category}",
    )


def type_filter_flow(connection) -> None:
    transaction_type = read_transaction_type()

    transactions = get_transactions_by_type(
        connection,
        transaction_type,
    )

    print_transactions(
        transactions,
        f"TYPE: {transaction_type.upper()}",
    )


def date_range_filter_flow(connection) -> None:
    print()
    print("FILTER BY DATE RANGE")

    start_date = read_date(
        "Start date (YYYY-MM-DD): "
    )

    end_date = read_date(
        "End date (YYYY-MM-DD): "
    )

    try:
        transactions = (
            get_transactions_by_date_range(
                connection,
                start_date,
                end_date,
            )
        )

        print_transactions(
            transactions,
            (
                f"TRANSACTIONS FROM "
                f"{start_date} TO {end_date}"
            ),
        )

    except ValueError as error:
        print(f"Error: {error}")


def filter_transactions_flow(connection) -> None:
    while True:
        print()
        print("FILTER TRANSACTIONS")
        print("-" * 50)
        print("1. By category")
        print("2. By type")
        print("3. By date range")
        print("0. Back")
        print()

        option = input(
            "Choose a filter: "
        ).strip()

        match option:
            case "1":
                category_filter_flow(
                    connection
                )

            case "2":
                type_filter_flow(
                    connection
                )

            case "3":
                date_range_filter_flow(
                    connection
                )

            case "0":
                break

            case _:
                print("Invalid option.")


def edit_transaction_flow(connection) -> None:
    transaction_id = read_transaction_id(
        "Transaction ID to edit: "
    )

    print("Enter the new transaction data.")

    transaction_type = read_transaction_type()
    amount = read_amount()

    category = input(
        "Category: "
    ).strip()

    description = input(
        "Description: "
    ).strip()

    transaction_date = read_date()

    try:
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
        print(
            "Transaction updated successfully."
        )
        print_transaction(transaction)

    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")


def delete_transaction_flow(connection) -> None:
    transaction_id = read_transaction_id(
        "Transaction ID to delete: "
    )

    confirmation = input(
        f"Delete transaction "
        f"{transaction_id}? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Deletion cancelled.")
        return

    try:
        remove_transaction(
            connection,
            transaction_id,
        )

        print(
            "Transaction deleted successfully."
        )

    except ValueError as error:
        print(f"Error: {error}")


def run() -> None:
    initialize_database()

    with get_connection() as connection:
        while True:
            print_header()
            print_menu()

            option = input(
                "Choose an option: "
            ).strip()

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
                    list_transactions_flow(
                        connection
                    )

                case "4":
                    summary_flow(
                        connection
                    )

                case "5":
                    filter_transactions_flow(
                        connection
                    )

                case "6":
                    edit_transaction_flow(
                        connection
                    )

                case "7":
                    delete_transaction_flow(
                        connection
                    )

                case "0":
                    print()
                    print("Goodbye.")
                    break

                case _:
                    print("Invalid option.")


if __name__ == "__main__":
    run()