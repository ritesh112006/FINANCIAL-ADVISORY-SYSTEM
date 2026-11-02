import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'finwise.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'schema.sql')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM system_settings WHERE key = 'currency'")
    if not cursor.fetchone():
        cursor.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES ('currency', '₹')")
        cursor.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES ('monthly_income_baseline', '65000')")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database ready.")
