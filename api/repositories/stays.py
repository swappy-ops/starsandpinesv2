"""Stay repository — raw SQLite, no ORM."""

from api.db import get_db
from datetime import datetime


class StayRepository:
    @staticmethod
    def create(stay_id: str, guest_id: str, room_id: str, check_in: str,
               checked_in_by: str, bed_id: str = None, notes: str = None) -> dict:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO stays (id, guest_id, room_id, bed_id, check_in, checked_in_by, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (stay_id, guest_id, room_id, bed_id, check_in, checked_in_by, notes),
            )
            row = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "WHERE s.id = ?",
                (stay_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_id(stay_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "WHERE s.id = ?",
                (stay_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_active_stays() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name, "
                "b.label as bed_label "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "LEFT JOIN beds b ON s.bed_id = b.id "
                "WHERE s.status = 'active' "
                "ORDER BY s.check_in DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_guest(guest_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT s.*, r.name as room_name, b.label as bed_label "
                "FROM stays s "
                "JOIN rooms r ON s.room_id = r.id "
                "LEFT JOIN beds b ON s.bed_id = b.id "
                "WHERE s.guest_id = ? ORDER BY s.check_in DESC",
                (guest_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def checkout(stay_id: str, checked_out_by: str) -> dict:
        """Compute nights, room charge, mark checked out."""
        with get_db() as conn:
            stay = conn.execute(
                "SELECT s.*, r.base_price FROM stays s JOIN rooms r ON s.room_id = r.id WHERE s.id = ?",
                (stay_id,),
            ).fetchone()
            if not stay:
                return None

            check_in = datetime.fromisoformat(stay["check_in"])
            check_out = datetime.utcnow()
            nights = max(1, (check_out - check_in).days)
            room_charge = nights * stay["base_price"] * (1 - stay["discount_pct"] / 100)

            conn.execute(
                "UPDATE stays SET check_out = ?, num_nights = ?, room_charge = ?, "
                "status = 'checked_out', checked_out_by = ? WHERE id = ?",
                (check_out.isoformat(), nights, room_charge, checked_out_by, stay_id),
            )
            row = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "WHERE s.id = ?",
                (stay_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def cancel(stay_id: str) -> dict:
        with get_db() as conn:
            conn.execute(
                "UPDATE stays SET status = 'cancelled' WHERE id = ?",
                (stay_id,),
            )
            row = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "WHERE s.id = ?",
                (stay_id,),
            ).fetchone()
            return dict(row) if row else None
