"""Guest repository — raw SQLite, no ORM."""

from api.db import get_db


class GuestRepository:
    @staticmethod
    def create(guest_id: str, name: str, phone: str, email: str = None,
               id_type: str = None, id_number: str = None, nationality: str = "Indian") -> dict:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO guests (id, name, phone, email, id_type, id_number, nationality) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (guest_id, name, phone, email, id_type, id_number, nationality),
            )
            row = conn.execute("SELECT * FROM guests WHERE id = ? AND is_deleted = 0", (guest_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_id(guest_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM guests WHERE id = ? AND is_deleted = 0", (guest_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_phone(phone: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM guests WHERE phone = ? AND is_deleted = 0", (phone,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def search(query: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM guests WHERE is_deleted = 0 AND (name LIKE ? OR phone LIKE ?) ORDER BY created_at DESC LIMIT 20",
                (f"%{query}%", f"%{query}%"),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def list_all() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM guests WHERE is_deleted = 0 ORDER BY created_at DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def soft_delete(guest_id: str):
        with get_db() as conn:
            conn.execute("UPDATE guests SET is_deleted = 1 WHERE id = ?", (guest_id,))
