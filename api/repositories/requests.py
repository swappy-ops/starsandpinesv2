"""Service requests repository — SQLite CRUD for experiences and concierge requests."""

from api.db import get_db
from datetime import datetime


class ServiceRequestRepository:
    @staticmethod
    def create(request_id: str, stay_id: str, request_type: str, rtype: str,
               notes: str = None) -> dict:
        now = datetime.utcnow().isoformat()
        with get_db() as conn:
            conn.execute(
                "INSERT INTO service_requests (id, stay_id, request_type, type, notes, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, 'requested', ?, ?)",
                (request_id, stay_id, request_type, rtype, notes, now, now),
            )
        return {
            "id": request_id, "stay_id": stay_id, "request_type": request_type,
            "type": rtype, "notes": notes, "status": "requested",
            "created_at": now, "updated_at": now,
        }

    @staticmethod
    def get_by_stay(stay_id: str, request_type: str | None = None) -> list[dict]:
        with get_db() as conn:
            if request_type:
                rows = conn.execute(
                    "SELECT * FROM service_requests WHERE stay_id = ? AND request_type = ? ORDER BY created_at DESC",
                    (stay_id, request_type),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM service_requests WHERE stay_id = ? ORDER BY created_at DESC",
                    (stay_id,),
                ).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def update_status(request_id: str, status: str) -> dict | None:
        now = datetime.utcnow().isoformat()
        with get_db() as conn:
            conn.execute(
                "UPDATE service_requests SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, request_id),
            )
            row = conn.execute("SELECT * FROM service_requests WHERE id = ?", (request_id,)).fetchone()
        return dict(row) if row else None
