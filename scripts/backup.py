#!/usr/bin/env python3
"""Nightly backup of sp_v2.db.

Copies the database file to the backups directory with a timestamp.
Designed to be run via systemd timer or cron.

Usage:
    python scripts/backup.py
"""

import shutil
import os
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path(__file__).resolve().parent.parent / "backups"
DB_PATH = os.environ.get("SP_DB_PATH", str(Path(__file__).resolve().parent.parent / "sp_v2.db"))


def backup():
    """Copy the database to backups/ with timestamp."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"sp_v2_{timestamp}.db"

    if not Path(DB_PATH).exists():
        print(f"Database not found at {DB_PATH}")
        return

    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")

    # Clean up backups older than 30 days
    cutoff = datetime.now().timestamp() - (30 * 86400)
    for f in BACKUP_DIR.glob("sp_v2_*.db"):
        if f.stat().st_mtime < cutoff:
            f.unlink()
            print(f"  Removed old backup: {f.name}")


if __name__ == "__main__":
    backup()
