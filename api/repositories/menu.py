"""Menu repository — raw SQLite, no ORM."""

from api.db import get_db


class MenuRepository:
    @staticmethod
    def list_all() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM menu_items WHERE is_deleted = 0 ORDER BY category, name"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_available() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM menu_items WHERE is_deleted = 0 AND is_available = 1 ORDER BY category, name"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(item_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM menu_items WHERE id = ? AND is_deleted = 0",
                (item_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def toggle_availability(item_id: str, is_available: bool):
        with get_db() as conn:
            conn.execute(
                "UPDATE menu_items SET is_available = ? WHERE id = ?",
                (1 if is_available else 0, item_id),
            )

    @staticmethod
    def get_by_category() -> dict[str, list[dict]]:
        """Return menu items grouped by category."""
        items = MenuRepository.get_available()
        grouped = {}
        for item in items:
            cat = item["category"]
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(item)
        return grouped
