import sqlite3
from config import DB_DIR


DB_PATH = DB_DIR / "sessions.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            photo_count INTEGER
        )
        """
    )

    conn.commit()

    conn.close()


def get_sessions():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("SELECT * FROM sessions")

    rows = cur.fetchall()

    conn.close()

    return rows