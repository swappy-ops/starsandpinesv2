"""Occupancy service — business logic for property occupancy dashboard.

Three levels:
- Property: total beds, occupied beds, occupancy rate
- Room: each room with bed-level detail
- Bed: individual bed status
"""

from api.db import get_db
from datetime import datetime


class OccupancyService:
    @staticmethod
    def current_occupancy() -> dict:
        """Full occupancy dashboard: property stats, room-level, bed-level."""
        with get_db() as conn:
            # Property-level stats
            total_beds = conn.execute("SELECT COUNT(*) as c FROM beds WHERE is_active = 1").fetchone()["c"]
            occupied_beds = conn.execute("SELECT COUNT(*) as c FROM beds WHERE is_active = 1 AND is_occupied = 1").fetchone()["c"]
            available_beds = total_beds - occupied_beds
            occupancy_rate = round((occupied_beds / total_beds * 100) if total_beds > 0 else 0, 1)

            # Room-level with bed details
            rooms = conn.execute(
                "SELECT r.id, r.name, r.type, r.base_price, r.capacity, r.is_active "
                "FROM rooms r WHERE r.is_active = 1 ORDER BY r.type, r.name"
            ).fetchall()

            room_details = []
            for room in rooms:
                room_id = room["id"]

                # Get beds for this room
                beds = conn.execute(
                    "SELECT b.id, b.label, b.is_occupied, "
                    "s.id as stay_id, s.guest_id, g.name as guest_name, g.phone as guest_phone "
                    "FROM beds b "
                    "LEFT JOIN stays s ON b.id = s.bed_id AND s.status = 'active' "
                    "LEFT JOIN guests g ON s.guest_id = g.id "
                    "WHERE b.room_id = ? AND b.is_active = 1 "
                    "ORDER BY b.label",
                    (room_id,),
                ).fetchall()

                bed_list = [dict(b) for b in beds]
                room_occupied = sum(1 for b in bed_list if b["is_occupied"])

                # For private rooms (no beds), check if room has an active stay
                if room["type"] == "private" and not bed_list:
                    private_stay = conn.execute(
                        "SELECT s.id as stay_id, s.guest_id, g.name as guest_name, g.phone as guest_phone "
                        "FROM stays s JOIN guests g ON s.guest_id = g.id "
                        "WHERE s.room_id = ? AND s.status = 'active'",
                        (room_id,),
                    ).fetchone()
                    if private_stay:
                        room_occupied = 1
                        room_details.append({
                            **dict(room),
                            "beds": [],
                            "occupied_beds": 1,
                            "total_beds": 1,
                            "is_occupied": True,
                            "guest": dict(private_stay),
                        })
                    else:
                        room_details.append({
                            **dict(room),
                            "beds": [],
                            "occupied_beds": 0,
                            "total_beds": 1,
                            "is_occupied": False,
                            "guest": None,
                        })
                else:
                    room_details.append({
                        **dict(room),
                        "beds": bed_list,
                        "occupied_beds": room_occupied,
                        "total_beds": len(bed_list) if bed_list else room["capacity"],
                        "is_occupied": room_occupied > 0,
                        "guest": None,  # Dorms have multiple guests
                    })

            return {
                "property": {
                    "total_beds": total_beds,
                    "occupied_beds": occupied_beds,
                    "available_beds": available_beds,
                    "occupancy_rate": occupancy_rate,
                },
                "rooms": room_details,
            }

    @staticmethod
    def arrivals_today() -> list[dict]:
        """Guests checking in today."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        with get_db() as conn:
            rows = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name, "
                "b.label as bed_label "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "LEFT JOIN beds b ON s.bed_id = b.id "
                "WHERE date(s.check_in) = ? AND s.status = 'active' "
                "ORDER BY s.check_in",
                (today,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def departures_today() -> list[dict]:
        """All active stays — staff decides who checks out."""
        with get_db() as conn:
            rows = conn.execute(
                "SELECT s.*, g.name as guest_name, g.phone as guest_phone, r.name as room_name, "
                "b.label as bed_label "
                "FROM stays s "
                "JOIN guests g ON s.guest_id = g.id "
                "JOIN rooms r ON s.room_id = r.id "
                "LEFT JOIN beds b ON s.bed_id = b.id "
                "WHERE s.status = 'active' "
                "ORDER BY s.check_in"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def revenue_today() -> dict:
        """Revenue summary for today."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        with get_db() as conn:
            food = conn.execute(
                "SELECT COUNT(*) as count, COALESCE(SUM(total), 0) as total "
                "FROM orders WHERE date(created_at) = ? AND status = 'served'",
                (today,),
            ).fetchone()

            payments = conn.execute(
                "SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total "
                "FROM payments WHERE date(collected_at) = ?",
                (today,),
            ).fetchone()

            # Ledger balance for today's charges
            ledger_charges = conn.execute(
                "SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total "
                "FROM ledger_entries WHERE date(created_at) = ? AND amount > 0",
                (today,),
            ).fetchone()

            return {
                "food_orders": dict(food),
                "payments_received": dict(payments),
                "ledger_charges": dict(ledger_charges),
            }
