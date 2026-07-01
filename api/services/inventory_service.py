"""Inventory service — business logic for stock management.

Handles:
- List inventory with low-stock alerts
- Log stock changes (restock, used, waste)
- Get inventory summary
"""

from api.repositories.inventory import InventoryRepository


class InventoryService:
    @staticmethod
    def get_full_inventory() -> dict:
        """All inventory grouped by category, with low-stock alerts."""
        categories = InventoryRepository.list_categories()
        items = InventoryRepository.list_items()
        low_stock = InventoryRepository.get_low_stock()

        grouped = {}
        for cat in categories:
            grouped[cat["name"]] = {
                "id": cat["id"],
                "items": [i for i in items if i["category_id"] == cat["id"]],
            }

        return {
            "categories": grouped,
            "low_stock": low_stock,
            "low_stock_count": len(low_stock),
        }

    @staticmethod
    def restock(item_id: str, quantity: float, note: str = None, logged_by: str = None) -> dict:
        """Add stock."""
        return InventoryRepository.log_change(item_id, "restock", quantity, note, logged_by)

    @staticmethod
    def consume(item_id: str, quantity: float, note: str = None, logged_by: str = None) -> dict:
        """Deduct stock (used in kitchen)."""
        return InventoryRepository.log_change(item_id, "used", -abs(quantity), note, logged_by)

    @staticmethod
    def waste(item_id: str, quantity: float, note: str = None, logged_by: str = None) -> dict:
        """Mark as waste."""
        return InventoryRepository.log_change(item_id, "waste", -abs(quantity), note, logged_by)

    @staticmethod
    def correct(item_id: str, new_quantity: float, note: str = None, logged_by: str = None) -> dict:
        """Manual stock correction."""
        from api.db import get_db
        with get_db() as conn:
            current = conn.execute(
                "SELECT current_stock FROM inventory_items WHERE id = ?",
                (item_id,),
            ).fetchone()
            if not current:
                return None
            diff = new_quantity - current["current_stock"]
            return InventoryRepository.log_change(item_id, "correction", diff, note, logged_by)
