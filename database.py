import sqlite3
from datetime import datetime


# ---------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------

DB_NAME = "expenses.db"


# ---------------------------------------------------
# CREATE DATABASE AND TABLE
# ---------------------------------------------------

def create_database():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# ---------------------------------------------------
# ADD EXPENSE
# ---------------------------------------------------

def add_expense(item, price):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    current_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO expenses
        (item, price, date)
        VALUES (?, ?, ?)
        """,
        (item, price, current_date)
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------
# GET ALL EXPENSES
# ---------------------------------------------------

def get_expenses():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, item, price, date
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# ---------------------------------------------------
# GET TOTAL EXPENSE
# ---------------------------------------------------

def get_total_expense():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(price), 0)
        FROM expenses
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


# ---------------------------------------------------
# DELETE ONE EXPENSE
# ---------------------------------------------------

def delete_expense(expense_id):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------
# CLEAR ALL EXPENSES
# ---------------------------------------------------

def clear_expenses():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses"
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------
# TEST DATABASE
# ---------------------------------------------------

if __name__ == "__main__":

    create_database()

    print("SQLite database created successfully!")