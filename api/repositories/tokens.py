"""Guest portal token repository — raw SQLite, no ORM."""

import secrets
import string
from api.db import get_db
from datetime import datetime, timedelta


class TokenRepository:
    @staticmethod
    def generate_token() -> str:
        """Generate a 6-character alphanumeric token."""
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(6))

    @staticmethod
    def create(stay_id: str, guest_name: str, room_label: str,
               valid_hours: int = 48) -> dict:
        token = TokenRepository.generate_token()
        now = datetime.utcnow()
        valid_until = (now + timedelta(hours=valid_hours)).isoformat()
        expires_at = (now + timedelta(days=30)).isoformat()

        with get_db() as conn:
            existing = conn.execute("SELECT 1 FROM guest_portal_tokens WHERE token = ?", (token,)).fetchone()
            if existing:
                conn.commit()
                return TokenRepository.create(stay_id, guest_name, room_label, valid_hours)

            conn.execute(
                "INSERT INTO guest_portal_tokens (token, stay_id, guest_name, room_label, valid_until, expires_at) VALUES (?, ?, ?, ?, ?, ?)",
                (token, stay_id, guest_name, room_label, valid_until, expires_at),
            )
            return {
                "token": token,
                "stay_id": stay_id,
                "guest_name": guest_name,
                "room_label": room_label,
                "active": 1,
                "valid_until": valid_until,
                "expires_at": expires_at,
                "last_accessed": None,
                "created_at": now.isoformat(),
            }

    @staticmethod
    def get_by_token(token: str) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT t.*, s.status as stay_status, s.room_id, r.name as room_name "
                "FROM guest_portal_tokens t "
                "JOIN stays s ON t.stay_id = s.id "
                "JOIN rooms r ON s.room_id = r.id "
                "WHERE t.token = ?",
                (token,),
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def validate(token: str) -> dict | None:
        """Validate a token: must exist, be active, not expired, and stay must be active."""
        result = TokenRepository.get_by_token(token)
        if not result:
            return None
        if not result["active"]:
            return None

        now = datetime.utcnow()

        # Check hard expiry (expires_at)
        if result["expires_at"] and datetime.fromisoformat(result["expires_at"]) < now:
            TokenRepository.deactivate(token)
            return None

        # Check soft expiry (valid_until) — stay checkout or time-based
        if result["valid_until"] and datetime.fromisoformat(result["valid_until"]) < now:
            # Soft expiry: token still works but stay might be checked out
            if result["stay_status"] != "active":
                TokenRepository.deactivate(token)
                return None

        # Update last_accessed
        with get_db() as conn:
            conn.execute(
                "UPDATE guest_portal_tokens SET last_accessed = ? WHERE token = ?",
                (now.isoformat(), token),
            )
        return result

    @staticmethod
    def deactivate(token: str):
        with get_db() as conn:
            conn.execute(
                "UPDATE guest_portal_tokens SET active = 0 WHERE token = ?",
                (token,),
            )

    @staticmethod
    def deactivate_by_stay(stay_id: str):
        """Deactivate all tokens for a stay (called on checkout)."""
        with get_db() as conn:
            conn.execute(
                "UPDATE guest_portal_tokens SET active = 0 WHERE stay_id = ?",
                (stay_id,),
            )

    @staticmethod
    def get_by_stay(stay_id: str) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM guest_portal_tokens WHERE stay_id = ? ORDER BY created_at DESC",
                (stay_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def cleanup_expired():
        """Deactivate all expired tokens. Run periodically."""
        now = datetime.utcnow().isoformat()
        with get_db() as conn:
            conn.execute(
                "UPDATE guest_portal_tokens SET active = 0 WHERE expires_at < ? AND active = 1",
                (now,),
            )
