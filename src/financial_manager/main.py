from .database import initialize_database


def main() -> None:
    initialize_database()
    print("Financial Manager database initialized successfully.")


if __name__ == "__main__":
    main()