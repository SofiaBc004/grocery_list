from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "grocery.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
            category TEXT NOT NULL DEFAULT '',
            purchased INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
