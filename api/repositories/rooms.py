"""Rooms repository — raw SQLite, no ORM."""

from api.db import get_db


class RoomRepository:
    @staticmethod
    def list_all() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM rooms WHERE is_active = 1 ORDER BY type, name"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(room_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM rooms WHERE id = ?",
                (room_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_available_rooms() -> list[dict]:
        """Rooms that don't have an active stay."""
        with get_db() as conn:
            rows = conn.execute(
                "SELECT r.* FROM rooms r "
                "WHERE r.is_active = 1 "
                "AND r.id NOT IN ("
                "    SELECT s.room_id FROM stays s WHERE s.status = 'active'"
                ") "
                "ORDER BY r.type, r.name"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_occupancy() -> list[dict]:
        """Current occupancy: which rooms are occupied by whom."""
        with get_db() as conn:
            rows = conn.execute(
                "SELECT r.id as room_id, r.name as room_name, r.type, r.base_price, "
                "s.id as stay_id, s.guest_id, g.name as guest_name, g.phone as guest_phone, "
                "s.check_in, s.status "
                "FROM rooms r "
                "LEFT JOIN stays s ON r.id = s.room_id AND s.status = 'active' "
                "LEFT JOIN guests g ON s.guest_id = g.id "
                "WHERE r.is_active = 1 "
                "ORDER BY r.type, r.name"
            ).fetchall()
            return [dict(r) for r in rows]


class BedRepository:
    @staticmethod
    def list_by_room(room_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM beds WHERE room_id = ? AND is_active = 1 ORDER BY label",
                (room_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_available_beds() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT b.*, r.name as room_name FROM beds b "
                "JOIN rooms r ON b.room_id = r.id "
                "WHERE b.is_active = 1 AND b.is_occupied = 0 "
                "ORDER BY r.name, b.label"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def occupy(bed_id: str):
        with get_db() as conn:
            conn.execute("UPDATE beds SET is_occupied = 1 WHERE id = ?", (bed_id,))

    @staticmethod
    def vacate(bed_id: str):
        with get_db() as conn:
            conn.execute("UPDATE beds SET is_occupied = 0 WHERE id = ?", (bed_id,))
