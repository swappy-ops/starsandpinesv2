"""Inventory repository — raw SQLite, no ORM."""

from api.db import get_db
from datetime import datetime


class InventoryRepository:
    @staticmethod
    def list_categories() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM inventory_categories ORDER BY name").fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def list_items(category_id: str = None) -> list[dict]:
        with get_db() as conn:
            if category_id:
                rows = conn.execute(
                    "SELECT i.*, c.name as category_name FROM inventory_items i "
                    "JOIN inventory_categories c ON i.category_id = c.id "
                    "WHERE i.is_active = 1 AND i.category_id = ? "
                    "ORDER BY i.name",
                    (category_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT i.*, c.name as category_name FROM inventory_items i "
                    "JOIN inventory_categories c ON i.category_id = c.id "
                    "WHERE i.is_active = 1 "
                    "ORDER BY c.name, i.name"
                ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_low_stock() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT i.*, c.name as category_name FROM inventory_items i "
                "JOIN inventory_categories c ON i.category_id = c.id "
                "WHERE i.is_active = 1 AND i.current_stock <= i.threshold "
                "ORDER BY (i.current_stock / i.threshold) ASC"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def log_change(item_id: str, change_type: str, quantity: float,
                   note: str = None, logged_by: str = None) -> dict:
        """Log an inventory change and update current_stock."""
        import uuid
        log_id = f"ilog_{uuid.uuid4().hex[:8]}"
        with get_db() as conn:
            conn.execute(
                "INSERT INTO inventory_log (id, item_id, change_type, quantity, note, logged_by) VALUES (?, ?, ?, ?, ?, ?)",
                (log_id, item_id, change_type, quantity, note, logged_by),
            )
            conn.execute(
                "UPDATE inventory_items SET current_stock = current_stock + ?, last_updated = ? WHERE id = ?",
                (quantity, datetime.utcnow().isoformat(), item_id),
            )
            return InventoryRepository.get_log_entry(log_id)

    @staticmethod
    def get_log_entry(log_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM inventory_log WHERE id = ?", (log_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_item_log(item_id: str, limit: int = 50) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM inventory_log WHERE item_id = ? ORDER BY logged_at DESC LIMIT ?",
                (item_id, limit),
            ).fetchall()
            return [dict(r) for r in rows]
