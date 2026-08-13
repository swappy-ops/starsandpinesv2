#!/usr/bin/env python3
"""Initialize the Stars & Pines V2 database.

Usage:
    python scripts/init_db.py

Creates sp_v2.db with all tables from api/schema.sql.
Safe to run multiple times (uses CREATE TABLE IF NOT EXISTS).
"""

import sys
from pathlib import Path

# Add project root to path so we can import api
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.db import init_db

if __name__ == "__main__":
    print("Initializing Stars & Pines V2 database...")
    init_db()
    print("Done. Database created at: sp_v2.db")
