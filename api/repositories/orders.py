"""Order repository — raw SQLite, no ORM."""

from api.db import get_db
from datetime import datetime


class OrderRepository:
    @staticmethod
    def create(order_id: str, order_type: str, stay_id: str = None,
               guest_id: str = None, table_label: str = None, notes: str = None) -> dict:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO orders (id, order_type, stay_id, guest_id, table_label, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, order_type, stay_id, guest_id, table_label, notes),
            )
            return OrderRepository._get_row(conn, order_id)

    @staticmethod
    def _get_row(conn, order_id: str) -> dict | None:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if row:
            result = dict(row)
            result["items"] = OrderRepository.get_items(order_id)
            return result
        return None

    @staticmethod
    def get_by_id(order_id: str) -> dict | None:
        with get_db() as conn:
            return OrderRepository._get_row(conn, order_id)

    @staticmethod
    def get_items(order_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM order_items WHERE order_id = ?",
                (order_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def add_item(item_id: str, order_id: str, menu_item_id: str,
                 item_name: str, item_price: float, quantity: int,
                 subtotal: float, notes: str = None):
        with get_db() as conn:
            conn.execute(
                "INSERT INTO order_items (id, order_id, menu_item_id, item_name, item_price, quantity, subtotal, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (item_id, order_id, menu_item_id, item_name, item_price, quantity, subtotal, notes),
            )

    @staticmethod
    def update_total(order_id: str, total: float):
        with get_db() as conn:
            conn.execute(
                "UPDATE orders SET total = ?, updated_at = ? WHERE id = ?",
                (total, datetime.utcnow().isoformat(), order_id),
            )

    @staticmethod
    def update_status(order_id: str, status: str) -> dict:
        with get_db() as conn:
            conn.execute(
                "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
                (status, datetime.utcnow().isoformat(), order_id),
            )
            return OrderRepository._get_row(conn, order_id)

    @staticmethod
    def get_pending() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT o.*, s.room_id, r.name as room_name, g.name as guest_name "
                "FROM orders o "
                "LEFT JOIN stays s ON o.stay_id = s.id "
                "LEFT JOIN rooms r ON s.room_id = r.id "
                "LEFT JOIN guests g ON o.guest_id = g.id "
                "WHERE o.status IN ('pending', 'preparing') "
                "ORDER BY o.created_at ASC"
            ).fetchall()
            results = []
            for row in rows:
                result = dict(row)
                result["items"] = OrderRepository.get_items(result["id"])
                results.append(result)
            return results

    @staticmethod
    def get_by_stay(stay_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM orders WHERE stay_id = ? ORDER BY created_at DESC",
                (stay_id,),
            ).fetchall()
            results = []
            for row in rows:
                result = dict(row)
                result["items"] = OrderRepository.get_items(result["id"])
                results.append(result)
            return results

    @staticmethod
    def get_recent(limit: int = 50) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT o.*, s.room_id, r.name as room_name "
                "FROM orders o "
                "LEFT JOIN stays s ON o.stay_id = s.id "
                "LEFT JOIN rooms r ON s.room_id = r.id "
                "ORDER BY o.created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            results = []
            for row in rows:
                result = dict(row)
                result["items"] = OrderRepository.get_items(result["id"])
                results.append(result)
            return results
