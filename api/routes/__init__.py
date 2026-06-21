"""Stars & Pines V2 — API Routes.

Thin routes. All business logic in services.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from api.services.guest_service import GuestService
from api.services.stay_service import StayService
from api.services.billing_service import BillingService
from api.services.kitchen_service import KitchenService
from api.services.occupancy_service import OccupancyService
from api.services.inventory_service import InventoryService
from api.services.dashboard_service import DashboardService
from api.services.orders import OrderService
from api.repositories.menu import MenuRepository
from api.repositories.guests import GuestRepository
from api.repositories.grievances import GrievanceRepository
from api.repositories.notifications import NotificationRepository
from api.repositories.requests import ServiceRequestRepository
from api.repositories.tokens import TokenRepository
from api.repositories.staff import StaffRepository
from api.repositories.cleaning import CleaningRepository
from api.repositories.rooms import RoomRepository, BedRepository

router = APIRouter(prefix="/api")


# ─── Pydantic Models ───

class CheckInRequest(BaseModel):
    guest_name: str
    guest_phone: str
    guest_email: Optional[str] = None
    id_type: Optional[str] = None
    id_number: Optional[str] = None
    nationality: str = "Indian"
    room_id: str
    bed_id: Optional[str] = None
    notes: Optional[str] = None
    staff_name: str


class CheckoutRequest(BaseModel):
    stay_id: str
    staff_name: str


class OrderRequest(BaseModel):
    order_type: str  # 'room' | 'cafe'
    stay_id: Optional[str] = None
    guest_id: Optional[str] = None
    table_label: Optional[str] = None
    notes: Optional[str] = None
    items: list[dict]  # [{menu_item_id, quantity, notes}]


class OrderStatusRequest(BaseModel):
    status: str  # 'preparing' | 'served' | 'cancelled'
    staff_name: Optional[str] = None


class PaymentRequest(BaseModel):
    stay_id: str
    amount: float
    method: str = "cash"
    upi_txn_id: Optional[str] = None
    receipt_ref: Optional[str] = None
    collected_by: Optional[str] = None


class StaffLoginRequest(BaseModel):
    staff_id: str
    pin: str


class CleaningRequest(BaseModel):
    stay_id: str
    room_id: str
    notes: Optional[str] = None


class RestockRequest(BaseModel):
    item_id: str
    quantity: float
    note: Optional[str] = None
    logged_by: Optional[str] = None


class ConsumeRequest(BaseModel):
    item_id: str
    quantity: float
    note: Optional[str] = None
    logged_by: Optional[str] = None


class GrievanceRequest(BaseModel):
    stay_id: str
    type: str
    message: str
    severity: str = "medium"


class ServiceRequestCreate(BaseModel):
    stay_id: str
    request_type: str  # 'experience' | 'concierge'
    type: str
    notes: Optional[str] = None


class PortalPaymentRequest(BaseModel):
    stay_id: str
    amount: float
    method: str = "cash"  # 'cash' | 'upi' | 'card' | 'pay_later'
    notes: Optional[str] = None


# ─── Staff Auth ───

@router.post("/staff/login")
def staff_login(req: StaffLoginRequest):
    staff = StaffRepository.authenticate(req.staff_id, req.pin)
    if not staff:
        raise HTTPException(status_code=401, detail="Invalid staff ID or PIN")
    return staff


@router.get("/staff/list")
def list_staff():
    return StaffRepository.list_all()


# ─── Guest Entry (Check-in / Checkout) ───

@router.post("/checkin")
def checkin(req: CheckInRequest):
    """Check in a guest: creates guest (if new), stay, and token."""
    # Find or create guest
    guest = GuestService.find_or_create(
        name=req.guest_name,
        phone=req.guest_phone,
        email=req.guest_email,
        id_type=req.id_type,
        id_number=req.id_number,
        nationality=req.nationality,
    )

    # Create stay + token
    stay = StayService.checkin(
        guest_id=guest["id"],
        room_id=req.room_id,
        staff_name=req.staff_name,
        notes=req.notes,
        bed_id=req.bed_id,
    )

    return {
        "guest": guest,
        "stay": stay,
        "token": stay.get("token"),
        "portal_url": f"/guest-portal?token={stay.get('token')}",
    }


@router.get("/next-booking-number")
def next_booking_number():
    """Return the next sequential booking number (1, 2, 3, ...)."""
    from api.db import get_db
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM stays").fetchone()
        return {"booking_number": row["cnt"] + 1}


@router.post("/checkout")
def checkout(req: CheckoutRequest):
    """Check out a guest: computes charges, closes stay, deactivates token."""
    stay = StayService.checkout(req.stay_id, req.staff_name)
    if not stay:
        raise HTTPException(status_code=404, detail="Stay not found")

    bill = BillingService.get_bill(req.stay_id)
    return {"stay": stay, "bill": bill}


@router.get("/guests/search")
def search_guests(q: str):
    return GuestService.search(q)


@router.get("/guests/{guest_id}")
def get_guest(guest_id: str):
    guest = GuestService.get_guest_history(guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest


# ─── Guest Portal ───

@router.get("/portal/validate")
def validate_token(token: str):
    """Validate a guest portal token. Returns stay info if valid."""
    result = TokenRepository.validate(token)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return result


@router.get("/portal/{token}/bill")
def get_portal_bill(token: str):
    """Get bill for a guest portal token."""
    token_data = TokenRepository.validate(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return BillingService.get_bill(token_data["stay_id"])


@router.get("/portal/{token}/orders")
def get_portal_orders(token: str):
    """Get orders for a guest portal token."""
    from api.repositories.orders import OrderRepository
    token_data = TokenRepository.validate(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return OrderRepository.get_by_stay(token_data["stay_id"])


# ─── Menu ───

@router.get("/menu")
def get_menu():
    return MenuRepository.get_by_category()


@router.get("/menu/available")
def get_available_menu():
    return MenuRepository.get_available()


@router.post("/menu/{item_id}/toggle")
def toggle_menu_item(item_id: str, is_available: bool = True):
    MenuRepository.toggle_availability(item_id, is_available)
    return {"item_id": item_id, "is_available": is_available}


# ─── Orders ───

@router.post("/orders")
def create_order(req: OrderRequest):
    return OrderService.create_order(
        order_type=req.order_type,
        stay_id=req.stay_id,
        guest_id=req.guest_id,
        table_label=req.table_label,
        notes=req.notes,
        items=req.items,
    )


@router.post("/orders/{order_id}/status")
def update_order_status(order_id: str, req: OrderStatusRequest):
    result = OrderService.update_status(order_id, req.status, req.staff_name)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


# ─── Kitchen Queue ───

@router.get("/kitchen/queue")
def get_kitchen_queue():
    return KitchenService.get_queue()


@router.get("/kitchen/stats")
def get_kitchen_stats():
    return KitchenService.get_today_stats()


# ─── Dashboard / Occupancy ───

@router.get("/dashboard")
def get_full_dashboard():
    """Single endpoint: everything the Family App needs."""
    return DashboardService.get_full_dashboard()


@router.get("/dashboard/occupancy")
def get_occupancy():
    return OccupancyService.current_occupancy()


@router.get("/dashboard/arrivals")
def get_arrivals():
    return OccupancyService.arrivals_today()


@router.get("/dashboard/departures")
def get_departures():
    return OccupancyService.departures_today()


@router.get("/dashboard/revenue")
def get_revenue():
    return OccupancyService.revenue_today()


# ─── Rooms & Beds ───

@router.get("/rooms")
def get_rooms():
    return RoomRepository.list_all()


@router.get("/rooms/available")
def get_available_rooms():
    return RoomRepository.get_available_rooms()


@router.get("/rooms/{room_id}/beds")
def get_room_beds(room_id: str):
    return BedRepository.list_by_room(room_id)


@router.get("/beds/available")
def get_available_beds():
    return BedRepository.get_available_beds()


# ─── Billing ───

@router.get("/bill/{stay_id}")
def get_bill(stay_id: str):
    return BillingService.get_bill(stay_id)


@router.post("/payment")
def record_payment(req: PaymentRequest):
    return BillingService.record_payment(
        stay_id=req.stay_id,
        amount=req.amount,
        method=req.method,
        upi_txn_id=req.upi_txn_id,
        receipt_ref=req.receipt_ref,
        collected_by=req.collected_by,
    )


# ─── Cleaning Requests ───

@router.post("/cleaning")
def create_cleaning_request(req: CleaningRequest):
    import uuid
    from datetime import datetime
    request_id = f"clean_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
    return CleaningRepository.create(request_id, req.stay_id, req.room_id, req.notes)


@router.get("/cleaning/pending")
def get_pending_cleaning():
    return CleaningRepository.get_pending()


@router.get("/cleaning/stay/{stay_id}")
def get_cleaning_by_stay(stay_id: str):
    return CleaningRepository.get_by_stay(stay_id)


@router.post("/cleaning/{request_id}/status")
def update_cleaning_status(request_id: str, status: str):
    result = CleaningRepository.update_status(request_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Cleaning request not found")
    return result


# ─── Inventory ───

@router.get("/inventory")
def get_inventory():
    return InventoryService.get_full_inventory()


@router.post("/inventory/restock")
def restock_item(req: RestockRequest):
    return InventoryService.restock(req.item_id, req.quantity, req.note, req.logged_by)


@router.post("/inventory/consume")
def consume_item(req: ConsumeRequest):
    return InventoryService.consume(req.item_id, req.quantity, req.note, req.logged_by)


# ─── Grievances ───

@router.post("/grievances")
def create_grievance(req: GrievanceRequest):
    import uuid
    from datetime import datetime
    gid = f"griev_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
    grievance = GrievanceRepository.create(gid, req.stay_id, req.type, req.message, req.severity)

    # Create notification for staff
    NotificationRepository.create(
        f"notif_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}",
        stay_id=req.stay_id,
        message=f"Guest concern: {req.type} — {req.message[:50]}",
        ntype="grievance",
        priority="high" if req.severity in ("high", "urgent") else "normal",
    )
    return grievance


@router.get("/grievances")
def get_grievances(stay_id: str):
    return GrievanceRepository.get_by_stay(stay_id)


@router.post("/grievances/{grievance_id}/status")
def update_grievance_status(grievance_id: str, status: str, staff_name: Optional[str] = None):
    result = GrievanceRepository.update_status(grievance_id, status, staff_name)
    if not result:
        raise HTTPException(status_code=404, detail="Grievance not found")
    return result


# ─── Notifications ───

@router.get("/notifications")
def get_notifications(stay_id: str):
    stay_notifs = NotificationRepository.get_by_stay(stay_id)
    broadcasts = NotificationRepository.get_broadcasts()
    return stay_notifs + broadcasts


@router.post("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str):
    result = NotificationRepository.mark_read(notification_id)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return result


@router.post("/notifications/read-all")
def mark_all_notifications_read(stay_id: str):
    count = NotificationRepository.mark_all_read(stay_id)
    return {"marked_read": count}


# ─── Service Requests (Experiences + Concierge) ───

@router.post("/service-requests")
def create_service_request(req: ServiceRequestCreate):
    import uuid
    from datetime import datetime
    rid = f"sr_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
    return ServiceRequestRepository.create(rid, req.stay_id, req.request_type, req.type, req.notes)


@router.get("/service-requests")
def get_service_requests(stay_id: str, request_type: Optional[str] = None):
    return ServiceRequestRepository.get_by_stay(stay_id, request_type)


@router.post("/service-requests/{request_id}/status")
def update_service_request_status(request_id: str, status: str):
    result = ServiceRequestRepository.update_status(request_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Service request not found")
    return result


# ─── Portal Payment ───

@router.post("/portal/{token}/payment")
def portal_payment(token: str, req: PortalPaymentRequest):
    """Record a payment from the guest portal."""
    token_data = TokenRepository.validate(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    payment = BillingService.record_payment(
        stay_id=req.stay_id,
        amount=req.amount,
        method=req.method,
        collected_by="Guest Portal",
    )

    # Create notification
    import uuid
    from datetime import datetime
    NotificationRepository.create(
        f"notif_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}",
        stay_id=req.stay_id,
        message=f"Payment of ₹{req.amount} recorded via portal ({req.method})",
        ntype="payment",
        priority="normal",
    )

    return payment
