"""Staff repository — raw SQLite, no ORM."""

from api.db import get_db


class StaffRepository:
    @staticmethod
    def authenticate(staff_id: str, pin: str) -> dict | None:
        """Authenticate staff by ID and PIN."""
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM staff WHERE id = ? AND pin = ? AND is_active = 1",
                (staff_id, pin),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_id(staff_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM staff WHERE id = ? AND is_active = 1",
                (staff_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def list_all() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM staff WHERE is_active = 1 ORDER BY name"
            ).fetchall()
            return [dict(r) for r in rows]
