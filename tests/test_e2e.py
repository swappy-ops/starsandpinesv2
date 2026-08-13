#!/usr/bin/env python3
"""Stars & Pines V2 — End-to-End Test

Tests the full guest lifecycle:
1. Staff login
2. Check-in guest → token generated
3. Validate token (Guest Portal)
4. Place order from portal
5. Kitchen sees order
6. Kitchen marks order served
7. Bill updates with food charge
8. Record payment
9. Checkout guest
10. Dashboard reflects checkout

Usage:
    python tests/test_e2e.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx

BASE = "http://127.0.0.1:8000"
client = httpx.Client(base_url=BASE, timeout=10)

passed = 0
failed = 0

def test(name, fn):
    global passed, failed
    try:
        result = fn()
        passed += 1
        print(f"  ✓ {name}")
        return result
    except Exception as e:
        failed += 1
        print(f"  ✗ {name}: {e}")
        raise

def assert_ok(resp):
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    return resp.json()

def assert_201(resp):
    assert resp.status_code in (200, 201), f"Expected 200/201, got {resp.status_code}: {resp.text}"
    return resp.json()

print("=" * 60)
print("Stars & Pines V2 — End-to-End Test")
print("=" * 60)

# ─── 1. Health ───
print("\n[1] Health check")
test("API is running", lambda: assert_ok(client.get("/health")))

# ─── 2. Staff login ───
print("\n[2] Staff login")
staff = test("Login as Mona", lambda: assert_201(client.post("/api/staff/login", json={
    "staff_id": "S03", "pin": "9012"
})))
assert staff["name"] == "Mona", f"Expected Mona, got {staff['name']}"
staff_name = staff["name"]

# ─── 3. Get available rooms ───
print("\n[3] Room availability")
rooms = test("Get available rooms", lambda: assert_ok(client.get("/api/rooms/available")))
assert len(rooms) > 0, "No available rooms"
print(f"    Available: {len(rooms)} rooms")

# Get a private room for check-in
private_room = next((r for r in rooms if r["type"] == "private"), rooms[0])
print(f"    Using: {private_room['name']} ({private_room['id']})")

# ─── 4. Check-in guest ───
print("\n[4] Check-in guest")
checkin = test("Check in new guest", lambda: assert_201(client.post("/api/checkin", json={
    "guest_name": "E2E Test Guest",
    "guest_phone": "+919999999999",
    "room_id": private_room["id"],
    "staff_name": staff_name,
})))
assert "token" in checkin, "No token in checkin response"
token = checkin["token"]
stay_id = checkin["stay"]["id"]
guest_id = checkin["guest"]["id"]
print(f"    Token: {token}")
print(f"    Stay: {stay_id}")
print(f"    Guest: {guest_id}")

# ─── 5. Validate token ───
print("\n[5] Token validation (Guest Portal)")
portal = test("Validate token", lambda: assert_ok(client.get(f"/api/portal/validate?token={token}")))
assert portal["stay_status"] == "active", f"Stay not active: {portal['stay_status']}"
print(f"    Guest: {portal['guest_name']}")
print(f"    Room: {portal['room_name']}")

# ─── 6. Get menu ───
print("\n[6] Menu")
menu = test("Get menu", lambda: assert_ok(client.get("/api/menu")))
assert len(menu) > 0, "Menu is empty"
print(f"    Categories: {list(menu.keys())}")

# Get first available item
first_cat = list(menu.keys())[0]
first_item = menu[first_cat][0]
print(f"    Ordering: {first_item['name']} (₹{first_item['price']})")

# ─── 7. Place order ───
print("\n[7] Place order from portal")
order = test("Create order", lambda: assert_201(client.post("/api/orders", json={
    "order_type": "room",
    "stay_id": stay_id,
    "table_label": private_room["name"],
    "items": [{"menu_item_id": first_item["id"], "quantity": 2}],
})))
order_id = order["id"]
print(f"    Order: {order_id}")
print(f"    Total: ₹{order['total']}")

# ─── 8. Kitchen queue ───
print("\n[8] Kitchen queue")
queue = test("Get kitchen queue", lambda: assert_ok(client.get("/api/kitchen/queue")))
assert len(queue) > 0, "Kitchen queue is empty"
assert any(o["id"] == order_id for o in queue), "Our order not in queue"
print(f"    Pending orders: {len(queue)}")

# ─── 9. Mark order served ───
print("\n[9] Kitchen marks order served")
served = test("Mark order served", lambda: assert_201(client.post(
    f"/api/orders/{order_id}/status",
    json={"status": "served", "staff_name": staff_name}
)))
assert served["status"] == "served", f"Order not served: {served['status']}"
print(f"    Order status: {served['status']}")

# ─── 10. Bill updated ───
print("\n[10] Bill reflects food charge")
bill = test("Get portal bill", lambda: assert_ok(client.get(f"/api/portal/{token}/bill")))
assert bill["balance"] > 0, f"Bill balance should be > 0, got {bill['balance']}"
food_entries = [e for e in bill["entries"] if e["entry_type"] == "food"]
assert len(food_entries) > 0, "No food entries in bill"
print(f"    Balance: ₹{bill['balance']}")
print(f"    Food charges: {len(food_entries)}")

# ─── 11. Dashboard ───
print("\n[11] Family Dashboard")
dashboard = test("Get full dashboard", lambda: assert_ok(client.get("/api/dashboard")))
assert "occupancy" in dashboard, "No occupancy in dashboard"
assert "kitchen" in dashboard, "No kitchen in dashboard"
assert "inventory" in dashboard, "No inventory in dashboard"
assert "revenue" in dashboard, "No revenue in dashboard"
occ = dashboard["occupancy"]["property"]
print(f"    Occupancy: {occ['occupied_beds']}/{occ['total_beds']} ({occ['occupancy_rate']}%)")
print(f"    Kitchen served: {dashboard['kitchen']['stats'].get('served', 0)}")

# ─── 12. Record payment ───
print("\n[12] Record payment")
payment = test("Record payment", lambda: assert_201(client.post("/api/payment", json={
    "stay_id": stay_id,
    "amount": bill["balance"],
    "method": "cash",
    "collected_by": staff_name,
})))
assert payment["new_balance"] == 0, f"Balance should be 0 after payment, got {payment['new_balance']}"
print(f"    Paid: ₹{payment['amount']}")
print(f"    New balance: ₹{payment['new_balance']}")

# ─── 13. Checkout ───
print("\n[13] Checkout guest")
checkout = test("Checkout guest", lambda: assert_201(client.post("/api/checkout", json={
    "stay_id": stay_id,
    "staff_name": staff_name,
})))
assert checkout["stay"]["status"] == "checked_out", f"Stay not checked out: {checkout['stay']['status']}"
print(f"    Stay status: {checkout['stay']['status']}")
print(f"    Nights: {checkout['stay']['num_nights']}")
print(f"    Room charge: ₹{checkout['stay']['room_charge']}")

# ─── 14. Token deactivated ───
print("\n[14] Token deactivated after checkout")
try:
    resp = client.get(f"/api/portal/validate?token={token}")
    assert resp.status_code == 401, f"Token should be invalid after checkout, got {resp.status_code}"
    print("    Token correctly deactivated")
except Exception as e:
    if "401" in str(e):
        print("    Token correctly deactivated")
    else:
        raise

# ─── 15. Dashboard after checkout ───
print("\n[15] Dashboard after checkout")
dashboard2 = test("Get dashboard after checkout", lambda: assert_ok(client.get("/api/dashboard")))
occ2 = dashboard2["occupancy"]["property"]
print(f"    Occupancy: {occ2['occupied_beds']}/{occ2['total_beds']} ({occ2['occupancy_rate']}%)")

# ─── SUMMARY ───
print("\n" + "=" * 60)
print(f"Results: {passed} passed, {failed} failed")
print("=" * 60)

if failed > 0:
    sys.exit(1)
else:
    print("\n✓ All E2E tests passed! Stars & Pines V2 is operational.")
