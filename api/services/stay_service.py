"""Stay service — business logic for check-in/checkout.

Handles:
- Check-in: create stay, generate token, occupy bed
- Checkout: compute charges, close stay, vacate EXACT bed, deactivate token
"""

import uuid
from datetime import datetime, timedelta
from api.repositories.stays import StayRepository
from api.repositories.tokens import TokenRepository
from api.repositories.ledger import LedgerRepository
from api.repositories.rooms import BedRepository


class StayService:
    @staticmethod
    def checkin(guest_id: str, room_id: str, staff_name: str,
                notes: str = None, bed_id: str = None) -> dict:
        """Check in a guest. Creates stay + token. Optionally occupies a bed."""
        stay_id = f"stay_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
        check_in = datetime.utcnow().isoformat()

        stay = StayRepository.create(stay_id, guest_id, room_id, check_in, staff_name, bed_id, notes)

        # If a bed is specified, mark it occupied
        if bed_id:
            BedRepository.occupy(bed_id)

        # Generate portal token
        from api.repositories.guests import GuestRepository
        from api.repositories.rooms import RoomRepository
        guest = GuestRepository.get_by_id(guest_id)
        room = RoomRepository.get_by_id(room_id)

        token = TokenRepository.create(
            stay_id=stay_id,
            guest_name=guest["name"] if guest else "Guest",
            room_label=room["name"] if room else room_id,
        )

        stay["token"] = token["token"]
        return stay

    @staticmethod
    def checkout(stay_id: str, staff_name: str) -> dict:
        """Check out a guest. Computes charges, closes stay, vacates EXACT bed, deactivates token."""
        from api.db import get_db

        # Get stay before checkout to find the exact bed
        with get_db() as conn:
            stay_row = conn.execute(
                "SELECT s.*, r.type as room_type FROM stays s JOIN rooms r ON s.room_id = r.id WHERE s.id = ?",
                (stay_id,),
            ).fetchone()
            if not stay_row:
                return None
            bed_id = stay_row["bed_id"]  # The exact bed assigned at check-in
            room_type = stay_row["room_type"]

        # Perform checkout (computes nights, room_charge)
        stay = StayRepository.checkout(stay_id, staff_name)
        if not stay:
            return None

        # Add room charge to ledger
        nights = stay["num_nights"] or 1
        charge = stay["room_charge"] or 0
        if charge > 0:
            LedgerRepository.add_room_charge(
                stay_id=stay_id,
                description=f"Room charge: {nights} night(s)",
                amount=charge,
                created_by=staff_name,
            )

        # Vacate the EXACT bed assigned to this stay (not just any bed in the room)
        if bed_id:
            BedRepository.vacate(bed_id)

        # Deactivate all tokens for this stay
        tokens = TokenRepository.get_by_stay(stay_id)
        for t in tokens:
            TokenRepository.deactivate(t["token"])

        return stay
