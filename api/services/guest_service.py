"""Guest service — business logic for guest operations.

Handles:
- Guest lookup/creation (find existing or create new)
- Guest search
"""

import uuid
from api.repositories.guests import GuestRepository


class GuestService:
    @staticmethod
    def find_or_create(name: str, phone: str, email: str = None,
                       id_type: str = None, id_number: str = None,
                       nationality: str = "Indian") -> dict:
        """Find existing guest by phone, or create new one."""
        existing = GuestRepository.get_by_phone(phone)
        if existing:
            return existing

        guest_id = f"guest_{uuid.uuid4().hex[:8]}"
        return GuestRepository.create(guest_id, name, phone, email, id_type, id_number, nationality)

    @staticmethod
    def search(query: str) -> list[dict]:
        return GuestRepository.search(query)

    @staticmethod
    def get_guest_history(guest_id: str) -> dict:
        """Get guest with all their stays."""
        from api.repositories.stays import StayRepository
        guest = GuestRepository.get_by_id(guest_id)
        if not guest:
            return None
        stays = StayRepository.get_by_guest(guest_id)
        guest["stays"] = stays
        guest["total_visits"] = len(stays)
        return guest
