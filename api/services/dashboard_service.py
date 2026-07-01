"""Dashboard service — single endpoint for Family App.

Aggregates occupancy, kitchen, inventory, revenue into one call.
Family App calls GET /api/dashboard and gets everything.
"""

from api.services.occupancy_service import OccupancyService
from api.services.kitchen_service import KitchenService
from api.services.inventory_service import InventoryService


class DashboardService:
    @staticmethod
    def get_full_dashboard() -> dict:
        """One call returns everything the Family App needs."""
        return {
            "occupancy": OccupancyService.current_occupancy(),
            "arrivals": OccupancyService.arrivals_today(),
            "departures": OccupancyService.departures_today(),
            "kitchen": {
                "queue": KitchenService.get_queue(),
                "stats": KitchenService.get_today_stats(),
            },
            "inventory": InventoryService.get_full_inventory(),
            "revenue": OccupancyService.revenue_today(),
        }
