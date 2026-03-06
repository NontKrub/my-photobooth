"""
database.py – SQLite persistence for session metadata.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_DB_DIR = Path(__file__).parent.parent / "storage"
_DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = _DB_DIR / "photobooth.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the database schema if it doesn't exist."""
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id   TEXT    UNIQUE NOT NULL,
            timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP,
            photo_count  INTEGER NOT NULL,
            layout       TEXT    NOT NULL,
            collage_path TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    logger.info("Database ready at %s", DB_PATH)


def save_session(
    session_id: str,
    photo_count: int,
    layout: str,
    collage_path: str,
) -> int:
    """Insert a session record and return its rowid."""
    conn = _connect()
    cur = conn.execute(
        """
        INSERT INTO sessions (session_id, photo_count, layout, collage_path)
        VALUES (?, ?, ?, ?)
        """,
        (session_id, photo_count, layout, collage_path),
    )
    conn.commit()
    rowid: int = cur.lastrowid  # type: ignore[assignment]
    conn.close()
    logger.info("Session %s saved (rowid=%d)", session_id, rowid)
    return rowid


def get_all_sessions() -> List[Dict[str, Any]]:
    """Return all sessions ordered by most-recent first."""
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM sessions ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Return a single session by its session_id, or None."""
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None
