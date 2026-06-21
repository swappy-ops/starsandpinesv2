"""Grievances repository — SQLite CRUD for guest concerns."""

from api.db import get_db
from datetime import datetime


class GrievanceRepository:
    @staticmethod
    def create(grievance_id: str, stay_id: str, gtype: str, message: str,
               severity: str = "medium") -> dict:
        now = datetime.utcnow().isoformat()
        with get_db() as conn:
            conn.execute(
                "INSERT INTO grievances (id, stay_id, type, message, severity, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, 'open', ?, ?)",
                (grievance_id, stay_id, gtype, message, severity, now, now),
            )
        return {
            "id": grievance_id, "stay_id": stay_id, "type": gtype,
            "message": message, "severity": severity, "status": "open",
            "created_at": now, "updated_at": now,
        }

    @staticmethod
    def get_by_stay(stay_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM grievances WHERE stay_id = ? ORDER BY created_at DESC",
                (stay_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def update_status(grievance_id: str, status: str, resolved_by: str = None) -> dict | None:
        now = datetime.utcnow().isoformat()
        with get_db() as conn:
            if resolved_by:
                conn.execute(
                    "UPDATE grievances SET status = ?, resolved_by = ?, resolved_at = ?, updated_at = ? WHERE id = ?",
                    (status, resolved_by, now, now, grievance_id),
                )
            else:
                conn.execute(
                    "UPDATE grievances SET status = ?, updated_at = ? WHERE id = ?",
                    (status, now, grievance_id),
                )
            row = conn.execute("SELECT * FROM grievances WHERE id = ?", (grievance_id,)).fetchone()
        return dict(row) if row else None
