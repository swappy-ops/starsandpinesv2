"""Order service — business logic for orders.

Handles:
- Creating orders with items
- Updating order status
- Auto-creating ledger entries when orders are served
"""

import uuid
from datetime import datetime
from api.repositories.orders import OrderRepository
from api.repositories.ledger import LedgerRepository
from api.repositories.menu import MenuRepository


class OrderService:
    @staticmethod
    def create_order(order_type: str, stay_id: str = None, guest_id: str = None,
                     table_label: str = None, notes: str = None,
                     items: list[dict] = None, created_by: str = None) -> dict:
        """Create an order with items. Items is a list of {menu_item_id, quantity, notes}."""
        order_id = f"ord_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"

        order = OrderRepository.create(order_id, order_type, stay_id, guest_id, table_label, notes)

        total = 0
        for item in (items or []):
            menu_item = MenuRepository.get_by_id(item["menu_item_id"])
            if not menu_item:
                continue

            quantity = item.get("quantity", 1)
            subtotal = menu_item["price"] * quantity

            item_id = f"oi_{uuid.uuid4().hex[:8]}"
            OrderRepository.add_item(
                item_id, order_id, menu_item["id"],
                menu_item["name"], menu_item["price"],
                quantity, subtotal, item.get("notes"),
            )
            total += subtotal

        OrderRepository.update_total(order_id, total)

        # If this is a room order and the order is immediately served, add to ledger
        if order_type == "room" and stay_id:
            # Orders start as 'pending', ledger entry created when status changes to 'served'
            pass

        return OrderRepository.get_by_id(order_id)

    @staticmethod
    def update_status(order_id: str, new_status: str, created_by: str = None) -> dict:
        """Update order status. If served and room order, create ledger entry."""
        order = OrderRepository.get_by_id(order_id)
        if not order:
            return None

        updated = OrderRepository.update_status(order_id, new_status)

        # When a room order is served, add to guest's ledger
        if new_status == "served" and order["order_type"] == "room" and order["stay_id"]:
            item_desc = ", ".join(
                f"{i['quantity']}x {i['item_name']}" for i in order["items"]
            )
            LedgerRepository.add_food_charge(
                stay_id=order["stay_id"],
                order_id=order_id,
                description=f"Order: {item_desc}",
                amount=order["total"],
                created_by=created_by,
            )

        return updated
