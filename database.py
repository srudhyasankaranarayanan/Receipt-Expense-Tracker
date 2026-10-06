import sqlite3
from datetime import datetime


DB_NAME = "expenses.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(item, price):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO expenses (item, price, date)
        VALUES (?, ?, ?)
    """, (item, price, current_date))

    conn.commit()
    conn.close()


def get_expenses():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, item, price, date
        FROM expenses
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data