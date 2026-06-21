"""Ledger repository — raw SQLite, no ORM."""

from api.db import get_db
from datetime import datetime


class LedgerRepository:
    @staticmethod
    def add_entry(entry_id: str, stay_id: str, entry_type: str,
                  description: str, amount: float, order_id: str = None,
                  created_by: str = None) -> dict:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO ledger_entries (id, stay_id, entry_type, description, amount, order_id, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (entry_id, stay_id, entry_type, description, amount, order_id, created_by),
            )
            row = conn.execute("SELECT * FROM ledger_entries WHERE id = ?", (entry_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_entry(entry_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM ledger_entries WHERE id = ?", (entry_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_stay(stay_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM ledger_entries WHERE stay_id = ? ORDER BY created_at ASC",
                (stay_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_balance(stay_id: str) -> float:
        with get_db() as conn:
            row = conn.execute(
                "SELECT SUM(amount) as balance FROM ledger_entries WHERE stay_id = ?",
                (stay_id,),
            ).fetchone()
            return row["balance"] or 0.0

    @staticmethod
    def add_food_charge(stay_id: str, order_id: str, description: str, amount: float, created_by: str = None):
        """Convenience: add a food charge to the ledger."""
        entry_id = f"ledger_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{order_id}"
        return LedgerRepository.add_entry(entry_id, stay_id, "food", description, amount, order_id, created_by)

    @staticmethod
    def add_room_charge(stay_id: str, description: str, amount: float, created_by: str = None):
        """Convenience: add a room charge to the ledger."""
        entry_id = f"ledger_room_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{stay_id}"
        return LedgerRepository.add_entry(entry_id, stay_id, "room", description, amount, created_by=created_by)

    @staticmethod
    def add_cleaning_charge(stay_id: str, description: str, amount: float, created_by: str = None):
        """Convenience: add a cleaning charge to the ledger."""
        entry_id = f"ledger_clean_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{stay_id}"
        return LedgerRepository.add_entry(entry_id, stay_id, "cleaning", description, amount, created_by=created_by)

    @staticmethod
    def add_payment(stay_id: str, description: str, amount: float, created_by: str = None):
        """Convenience: add a payment (negative amount) to the ledger."""
        entry_id = f"ledger_pay_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{stay_id}"
        return LedgerRepository.add_entry(entry_id, stay_id, "payment", description, -abs(amount), created_by=created_by)
