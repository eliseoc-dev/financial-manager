# Financial Manager — Project Specification

## 1. Purpose

Financial Manager is a personal finance management application built with Python.

The project is designed to demonstrate practical programming skills including:

* Python
* Object-Oriented Programming
* SQL
* SQLite
* CRUD operations
* Data validation
* Error handling
* Automated testing
* Debugging
* Git and GitHub
* Software organization and documentation

## 2. Version 1 Goals

The first functional version will allow users to:

1. Register income.
2. Register expenses.
3. List transactions.
4. Search and filter transactions.
5. Update transactions.
6. Delete transactions.
7. Organize transactions by category.
8. Calculate financial summaries.
9. Store information persistently in a database.
10. Validate incorrect user input.

## 3. Transaction Data

Each transaction will contain:

* ID
* Type: income or expense
* Amount
* Category
* Description
* Date

## 4. Financial Rules

* Amounts must be greater than zero.
* Transaction type must be either income or expense.
* Required fields cannot be empty.
* Dates must use a consistent format.
* Financial calculations must avoid floating-point precision problems.

For financial values, the application will use integer cents in the database and appropriate Python numeric handling instead of relying on binary floating-point arithmetic for monetary calculations.

## 5. Database

Version 1 will use SQLite.

The database will persist locally and will not be committed to GitHub when it contains personal or generated user data.

## 6. Main Operations

### Create

Register a new transaction.

### Read

Display transactions and financial summaries.

### Update

Modify an existing transaction.

### Delete

Remove an existing transaction.

## 7. Testing

The project will include automated tests for:

* Validation
* Transaction creation
* Transaction updates
* Transaction deletion
* Database operations
* Financial calculations
* Error conditions
* Edge cases

## 8. Project Principles

The project will prioritize:

* Readable code
* Small functions
* Clear responsibilities
* Meaningful names
* Input validation
* Error handling
* Testability
* Documentation
* Version control

## 9. Future Improvements

Possible later versions may include:

* User accounts
* Authentication
* Multiple financial accounts
* Budget management
* CSV import/export
* Data visualization
* REST API
* Web interface
* React frontend
* Deployment
* AI-assisted financial insights
