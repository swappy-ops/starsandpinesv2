"""Cleaning requests repository — raw SQLite, no ORM."""

from api.db import get_db
from datetime import datetime


class CleaningRepository:
    @staticmethod
    def create(request_id: str, stay_id: str, room_id: str, notes: str = None) -> dict:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO cleaning_requests (id, stay_id, room_id, notes) VALUES (?, ?, ?, ?)",
                (request_id, stay_id, room_id, notes),
            )
            row = conn.execute(
                "SELECT c.*, r.name as room_name "
                "FROM cleaning_requests c "
                "JOIN rooms r ON c.room_id = r.id "
                "WHERE c.id = ?",
                (request_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_id(request_id: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT c.*, r.name as room_name "
                "FROM cleaning_requests c "
                "JOIN rooms r ON c.room_id = r.id "
                "WHERE c.id = ?",
                (request_id,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_pending() -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT c.*, r.name as room_name, g.name as guest_name "
                "FROM cleaning_requests c "
                "JOIN rooms r ON c.room_id = r.id "
                "LEFT JOIN stays s ON c.stay_id = s.id "
                "LEFT JOIN guests g ON s.guest_id = g.id "
                "WHERE c.status = 'pending' "
                "ORDER BY c.requested_at ASC"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_stay(stay_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT c.*, r.name as room_name "
                "FROM cleaning_requests c "
                "JOIN rooms r ON c.room_id = r.id "
                "WHERE c.stay_id = ? "
                "ORDER BY c.requested_at DESC",
                (stay_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def update_status(request_id: str, status: str) -> dict:
        with get_db() as conn:
            completed_at = datetime.utcnow().isoformat() if status == "done" else None
            conn.execute(
                "UPDATE cleaning_requests SET status = ?, completed_at = ? WHERE id = ?",
                (status, completed_at, request_id),
            )
            row = conn.execute(
                "SELECT c.*, r.name as room_name "
                "FROM cleaning_requests c "
                "JOIN rooms r ON c.room_id = r.id "
                "WHERE c.id = ?",
                (request_id,),
            ).fetchone()
            return dict(row) if row else None
