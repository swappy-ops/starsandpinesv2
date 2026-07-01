"""Notifications repository — SQLite CRUD for guest-facing alerts."""

from api.db import get_db
from datetime import datetime


class NotificationRepository:
    @staticmethod
    def create(notification_id: str, stay_id: str | None, message: str,
               ntype: str = "info", priority: str = "normal") -> dict:
        now = datetime.utcnow().isoformat()
        with get_db() as conn:
            conn.execute(
                "INSERT INTO notifications (id, stay_id, message, type, priority, is_read, created_at) "
                "VALUES (?, ?, ?, ?, ?, 0, ?)",
                (notification_id, stay_id, message, ntype, priority, now),
            )
        return {
            "id": notification_id, "stay_id": stay_id, "message": message,
            "type": ntype, "priority": priority, "is_read": False, "created_at": now,
        }

    @staticmethod
    def get_by_stay(stay_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM notifications WHERE stay_id = ? ORDER BY created_at DESC",
                (stay_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_broadcasts() -> list[dict]:
        """Get broadcast notifications (stay_id IS NULL)."""
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM notifications WHERE stay_id IS NULL ORDER BY created_at DESC LIMIT 20",
            ).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def mark_read(notification_id: str) -> dict | None:
        with get_db() as conn:
            conn.execute(
                "UPDATE notifications SET is_read = 1 WHERE id = ?",
                (notification_id,),
            )
            row = conn.execute("SELECT * FROM notifications WHERE id = ?", (notification_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def mark_all_read(stay_id: str) -> int:
        with get_db() as conn:
            cursor = conn.execute(
                "UPDATE notifications SET is_read = 1 WHERE stay_id = ? AND is_read = 0",
                (stay_id,),
            )
        return cursor.rowcount
