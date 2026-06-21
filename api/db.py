"""Stars & Pines V2 — Database connection.

Thin wrapper around sqlite3. No ORM. No magic.
The .db file is the source of truth.
"""

import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path

# Database path — defaults to ./sp_v2.db in project root
DB_PATH = os.environ.get("SP_DB_PATH", str(Path(__file__).resolve().parent.parent / "sp_v2.db"))


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with WAL mode and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # dict-like access
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    """Context manager for database connections. Commits on success, rolls back on error."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(schema_path: str | None = None):
    """Create all tables from schema.sql. Idempotent — safe to run multiple times."""
    if schema_path is None:
        schema_path = str(Path(__file__).resolve().parent / "schema.sql")

    conn = get_connection()
    try:
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
