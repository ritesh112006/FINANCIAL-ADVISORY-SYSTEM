import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.db import get_db_connection, init_db

SAMPLE_TRANSACTIONS = [
    ("2026-07-01", 65000.0, "income", "Salary", "Monthly Corporate Salary"),
    ("2026-07-02", 18000.0, "expense", "Rent", "Apartment Monthly Rent"),
    ("2026-07-05", 8500.0,  "expense", "Groceries", "Supermarket Monthly Provisions"),
    ("2026-07-08", 3200.0,  "expense", "Utilities", "Electricity & Broadband"),
    ("2026-07-12", 4500.0,  "expense", "Dining Out", "Weekend Dinners"),
    ("2026-07-15", 3800.0,  "expense", "Shopping", "Clothing"),
    ("2026-07-18", 2200.0,  "expense", "Entertainment", "Movies"),
    ("2026-07-22", 1500.0,  "expense", "Subscriptions", "Streaming Subscriptions"),
    ("2026-07-28", 5000.0,  "expense", "EMI / Loans", "Education Loan EMI"),

    ("2026-08-01", 65000.0, "income", "Salary", "Monthly Corporate Salary"),
    ("2026-08-02", 18000.0, "expense", "Rent", "Apartment Monthly Rent"),
    ("2026-08-06", 9200.0,  "expense", "Groceries", "Groceries"),
    ("2026-08-09", 3500.0,  "expense", "Utilities", "Electricity & Water"),
    ("2026-08-14", 7800.0,  "expense", "Dining Out", "Dinners & Cafes"),
    ("2026-08-17", 8500.0,  "expense", "Shopping", "Electronics & Clothes"),
    ("2026-08-20", 4200.0,  "expense", "Entertainment", "Concert Tickets"),
    ("2026-08-25", 5000.0,  "expense", "EMI / Loans", "Education Loan EMI"),
    ("2026-08-28", 2500.0,  "expense", "Healthcare", "Doctor Visit"),

    ("2026-09-01", 65000.0, "income", "Salary", "Monthly Corporate Salary"),
    ("2026-09-02", 18000.0, "expense", "Rent", "Apartment Monthly Rent"),
    ("2026-09-05", 8000.0,  "expense", "Groceries", "Groceries"),
    ("2026-09-08", 3100.0,  "expense", "Utilities", "Utilities"),
    ("2026-09-12", 3400.0,  "expense", "Dining Out", "Dining Out"),
    ("2026-09-15", 2800.0,  "expense", "Shopping", "Apparel"),
    ("2026-09-19", 1500.0,  "expense", "Entertainment", "Entertainment"),
    ("2026-09-24", 5000.0,  "expense", "EMI / Loans", "Education Loan EMI"),
    ("2026-09-28", 8000.0,  "income", "Freelance", "Freelance Project"),

    ("2026-10-01", 70000.0, "income", "Salary", "Monthly Salary"),
    ("2026-10-02", 18000.0, "expense", "Rent", "Apartment Rent"),
    ("2026-10-04", 7800.0,  "expense", "Groceries", "Groceries"),
    ("2026-10-06", 2900.0,  "expense", "Utilities", "Electricity & Internet"),
    ("2026-10-08", 2600.0,  "expense", "Dining Out", "Dining Out"),
    ("2026-10-10", 1900.0,  "expense", "Shopping", "Essentials"),
    ("2026-10-11", 5000.0,  "expense", "EMI / Loans", "Education Loan EMI"),
    ("2026-10-11", 12000.0, "income", "Freelance", "Freelance Project")
]

SAMPLE_BUDGETS = [
    ("2026-10", "Rent", 18000.0),
    ("2026-10", "Groceries", 9000.0),
    ("2026-10", "Utilities", 3500.0),
    ("2026-10", "Dining Out", 3500.0),
    ("2026-10", "Shopping", 4000.0),
    ("2026-10", "Entertainment", 2500.0),
    ("2026-10", "EMI / Loans", 5000.0),
    ("2026-10", "Healthcare", 3000.0)
]

SAMPLE_GOALS = [
    ("Emergency Fund", 120000.0, 85000.0, "2027-03-31", "in_progress"),
    ("Certification Course", 45000.0, 32000.0, "2026-12-31", "in_progress"),
    ("Laptop Purchase", 80000.0, 80000.0, "2026-10-01", "achieved"),
    ("Mutual Fund Goal", 200000.0, 65000.0, "2027-10-31", "in_progress")
]

def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM budgets")
    cursor.execute("DELETE FROM savings_goals")

    cursor.executemany("""
        INSERT INTO transactions (date, amount, type, category, description)
        VALUES (?, ?, ?, ?, ?)
    """, SAMPLE_TRANSACTIONS)

    cursor.executemany("""
        INSERT INTO budgets (month, category, limit_amount)
        VALUES (?, ?, ?)
    """, SAMPLE_BUDGETS)

    cursor.executemany("""
        INSERT INTO savings_goals (title, target_amount, current_amount, target_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, SAMPLE_GOALS)

    conn.commit()
    conn.close()
    print("Database seeded with sample records.")

if __name__ == "__main__":
    seed_database()
