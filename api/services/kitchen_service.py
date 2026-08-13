"""Kitchen service — business logic for order queue management.

Handles:
- Get pending orders (kitchen queue)
- Update order status (pending → preparing → served)
- Cancel orders
"""

from api.services.orders import OrderService
from api.repositories.orders import OrderRepository


class KitchenService:
    @staticmethod
    def get_queue() -> list[dict]:
        """Get all pending and preparing orders for the kitchen."""
        return OrderRepository.get_pending()

    @staticmethod
    def start_preparing(order_id: str, staff_name: str = None) -> dict:
        """Mark order as being prepared."""
        return OrderService.update_status(order_id, "preparing", staff_name)

    @staticmethod
    def mark_served(order_id: str, staff_name: str = None) -> dict:
        """Mark order as served. Creates ledger entry for room orders."""
        return OrderService.update_status(order_id, "served", staff_name)

    @staticmethod
    def cancel_order(order_id: str, staff_name: str = None) -> dict:
        """Cancel an order."""
        return OrderService.update_status(order_id, "cancelled", staff_name)

    @staticmethod
    def get_today_stats() -> dict:
        """Kitchen stats for today."""
        from api.db import get_db
        from datetime import datetime

        today = datetime.utcnow().strftime("%Y-%m-%d")
        with get_db() as conn:
            stats = conn.execute(
                "SELECT status, COUNT(*) as count, COALESCE(SUM(total), 0) as total "
                "FROM orders WHERE date(created_at) = ? "
                "GROUP BY status",
                (today,),
            ).fetchall()

            result = {"pending": 0, "preparing": 0, "served": 0, "cancelled": 0, "total_revenue": 0}
            for row in stats:
                result[row["status"]] = row["count"]
                if row["status"] == "served":
                    result["total_revenue"] = row["total"]
            return result
