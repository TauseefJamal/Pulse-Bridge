import sqlite3
from pathlib import Path

DB_PATH = Path("data/pulsebridge.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Enable WAL mode: crucial for FastAPI + Background Scrapers
    conn.execute("PRAGMA journal_mode=WAL;") 
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Added UNIQUE constraint to title
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE, 
                source TEXT,
                category TEXT,
                sentiment_score REAL,
                sentiment_label TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT,
                message TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

if __name__ == "__main__":
    create_tables()