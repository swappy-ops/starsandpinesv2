-- Stars & Pines V2 — Database Schema
-- SQLite. Single file. No ORM.
-- Phase 1: Core operational tables only.

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- 1. GUESTS
-- ============================================================
CREATE TABLE IF NOT EXISTS guests (
    id              TEXT PRIMARY KEY,        -- UUID
    name            TEXT NOT NULL,
    phone           TEXT UNIQUE NOT NULL,
    email           TEXT,
    id_type         TEXT,                    -- 'aadhaar' | 'passport' | 'driving_license'
    id_number       TEXT,
    nationality     TEXT DEFAULT 'Indian',
    created_at      TEXT DEFAULT (datetime('now')),
    is_deleted      INTEGER DEFAULT 0
);

-- ============================================================
-- 2. ROOMS
-- ============================================================
CREATE TABLE IF NOT EXISTS rooms (
    id              TEXT PRIMARY KEY,        -- e.g. 'R01', 'DORM-A'
    name            TEXT NOT NULL,           -- 'Ridge Room 1', 'Dorm Bed A3'
    type            TEXT NOT NULL,           -- 'private' | 'dorm'
    base_price      REAL NOT NULL,           -- per night, INR
    capacity        INTEGER DEFAULT 1,
    is_active       INTEGER DEFAULT 1
);

-- ============================================================
-- 3. STAYS (Check-in / Check-out)
-- ============================================================
CREATE TABLE IF NOT EXISTS stays (
    id              TEXT PRIMARY KEY,
    guest_id        TEXT NOT NULL REFERENCES guests(id),
    room_id         TEXT NOT NULL REFERENCES rooms(id),
    bed_id          TEXT REFERENCES beds(id),   -- NULL for private rooms, set for dorms
    check_in        TEXT NOT NULL,              -- ISO datetime
    check_out       TEXT,                       -- NULL while checked in
    num_nights      INTEGER,                    -- computed on checkout
    room_charge     REAL,                       -- computed: nights x base_price
    discount_pct    REAL DEFAULT 0,             -- 5 or 10 from loyalty tier
    status          TEXT DEFAULT 'active',      -- 'active' | 'checked_out' | 'cancelled'
    checked_in_by   TEXT,                       -- staff name/id
    checked_out_by  TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 4. MENU ITEMS (Cafe)
-- ============================================================
CREATE TABLE IF NOT EXISTS menu_items (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    category        TEXT NOT NULL,           -- 'breakfast' | 'mains' | 'sandwiches' | 'beverages' | 'bakery' | 'special'
    price           REAL NOT NULL,
    prep_time_min   INTEGER DEFAULT 15,
    is_available    INTEGER DEFAULT 1,
    is_deleted      INTEGER DEFAULT 0
);

-- ============================================================
-- 5. ORDERS
-- ============================================================
CREATE TABLE IF NOT EXISTS orders (
    id              TEXT PRIMARY KEY,
    order_type      TEXT NOT NULL,           -- 'room' | 'cafe'
    stay_id         TEXT REFERENCES stays(id),     -- NULL for cafe walk-ins
    guest_id        TEXT REFERENCES guests(id),    -- NULL for anonymous cafe
    table_label     TEXT,                    -- 'Table 3', 'Room 2', 'Takeaway'
    status          TEXT DEFAULT 'pending',  -- 'pending' | 'preparing' | 'served' | 'cancelled'
    total           REAL DEFAULT 0,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS order_items (
    id              TEXT PRIMARY KEY,
    order_id        TEXT NOT NULL REFERENCES orders(id),
    menu_item_id    TEXT NOT NULL REFERENCES menu_items(id),
    item_name       TEXT NOT NULL,           -- snapshot at time of order
    item_price      REAL NOT NULL,           -- snapshot
    quantity        INTEGER NOT NULL DEFAULT 1,
    subtotal        REAL NOT NULL,
    notes           TEXT                     -- 'no onion', 'extra spicy'
);

-- ============================================================
-- 6. GUEST LEDGER (Billing)
-- ============================================================
CREATE TABLE IF NOT EXISTS ledger_entries (
    id              TEXT PRIMARY KEY,
    stay_id         TEXT NOT NULL REFERENCES stays(id),
    entry_type      TEXT NOT NULL,           -- 'room' | 'food' | 'cleaning' | 'misc' | 'discount' | 'payment'
    description     TEXT NOT NULL,
    amount          REAL NOT NULL,           -- positive = charge, negative = payment/discount
    order_id        TEXT REFERENCES orders(id),
    created_at      TEXT DEFAULT (datetime('now')),
    created_by      TEXT                     -- staff name
);

-- ============================================================
-- 7. STAFF / AUTH
-- ============================================================
CREATE TABLE IF NOT EXISTS staff (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    role            TEXT NOT NULL,           -- 'admin' | 'kitchen' | 'housekeeping' | 'manager'
    pin             TEXT,                    -- 4-digit PIN (stored as plain text for now; bcrypt later)
    phone           TEXT,
    is_active       INTEGER DEFAULT 1
);

-- ============================================================
-- 8. CLEANING REQUESTS
-- ============================================================
CREATE TABLE IF NOT EXISTS cleaning_requests (
    id              TEXT PRIMARY KEY,
    stay_id         TEXT REFERENCES stays(id),
    room_id         TEXT NOT NULL REFERENCES rooms(id),
    requested_at    TEXT DEFAULT (datetime('now')),
    status          TEXT DEFAULT 'pending',  -- 'pending' | 'in_progress' | 'done'
    completed_at    TEXT,
    notes           TEXT
);

-- ============================================================
-- 9. GUEST PORTAL TOKENS
-- ============================================================
CREATE TABLE IF NOT EXISTS guest_portal_tokens (
    token           TEXT PRIMARY KEY,        -- 6-char alphanumeric
    stay_id         TEXT NOT NULL REFERENCES stays(id),
    guest_name      TEXT,
    room_label      TEXT,
    active          INTEGER DEFAULT 1,
    valid_until     TEXT,                    -- auto-expiry time
    expires_at      TEXT,                    -- hard expiry (checkout + buffer or 30 days max)
    last_accessed   TEXT,                    -- last portal access
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 10. BEDS (for dorm bed-level tracking)
-- ============================================================
CREATE TABLE IF NOT EXISTS beds (
    id              TEXT PRIMARY KEY,        -- e.g. 'DORM-A-1', 'DORM-A-2'
    room_id         TEXT NOT NULL REFERENCES rooms(id),
    label           TEXT NOT NULL,           -- 'Bed 1', 'Bed A', etc.
    is_occupied     INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1
);

-- ============================================================
-- 11. PAYMENTS (separate from ledger entries)
-- ============================================================
CREATE TABLE IF NOT EXISTS payments (
    id              TEXT PRIMARY KEY,
    stay_id         TEXT NOT NULL REFERENCES stays(id),
    amount          REAL NOT NULL,
    method          TEXT,                    -- 'cash' | 'upi' | 'card'
    upi_txn_id      TEXT,
    receipt_ref     TEXT,
    collected_by    TEXT,                    -- staff name
    collected_at    TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 12. TASKS (housekeeping, maintenance, general)
-- ============================================================
CREATE TABLE IF NOT EXISTS tasks (
    id              TEXT PRIMARY KEY,
    type            TEXT NOT NULL,           -- 'cleaning' | 'maintenance' | 'restock' | 'other'
    title           TEXT NOT NULL,
    description     TEXT,
    room_id         TEXT REFERENCES rooms(id),
    assigned_to     TEXT REFERENCES staff(id),
    status          TEXT DEFAULT 'pending',  -- 'pending' | 'in_progress' | 'done' | 'cancelled'
    priority        TEXT DEFAULT 'normal',   -- 'low' | 'normal' | 'high' | 'urgent'
    created_by      TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    completed_at    TEXT
);

-- ============================================================
-- 13. INVENTORY
-- ============================================================
CREATE TABLE IF NOT EXISTS inventory_categories (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL            -- 'Grocery', 'Fruits & Vegetables', 'Beverages'
);

CREATE TABLE IF NOT EXISTS inventory_items (
    id              TEXT PRIMARY KEY,
    category_id     TEXT REFERENCES inventory_categories(id),
    name            TEXT NOT NULL,
    unit            TEXT NOT NULL,           -- 'kg' | 'g' | 'pcs' | 'litre' | 'dozen'
    current_stock   REAL DEFAULT 0,
    threshold       REAL NOT NULL,           -- alert when stock falls below
    last_updated    TEXT DEFAULT (datetime('now')),
    is_active       INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS inventory_log (
    id              TEXT PRIMARY KEY,
    item_id         TEXT NOT NULL REFERENCES inventory_items(id),
    change_type     TEXT NOT NULL,           -- 'restock' | 'used' | 'waste' | 'correction'
    quantity        REAL NOT NULL,           -- positive = added, negative = consumed
    note            TEXT,
    logged_by       TEXT,
    logged_at       TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 14. GRIEVANCES (guest concerns/complaints)
-- ============================================================
CREATE TABLE IF NOT EXISTS grievances (
    id              TEXT PRIMARY KEY,
    stay_id         TEXT NOT NULL REFERENCES stays(id),
    type            TEXT NOT NULL,           -- 'room' | 'housekeeping' | 'food' | 'staff' | 'water' | 'electricity' | 'noise' | 'other'
    message         TEXT NOT NULL,
    severity        TEXT DEFAULT 'medium',   -- 'low' | 'medium' | 'high' | 'urgent'
    status          TEXT DEFAULT 'open',     -- 'open' | 'acknowledged' | 'resolved' | 'dismissed'
    resolved_by     TEXT,                    -- staff name
    resolved_at     TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 15. NOTIFICATIONS (guest-facing alerts)
-- ============================================================
CREATE TABLE IF NOT EXISTS notifications (
    id              TEXT PRIMARY KEY,
    stay_id         TEXT REFERENCES stays(id),  -- NULL for broadcast
    message         TEXT NOT NULL,
    type            TEXT DEFAULT 'info',     -- 'info' | 'warning' | 'order' | 'grievance' | 'payment'
    priority        TEXT DEFAULT 'normal',   -- 'low' | 'normal' | 'high' | 'urgent'
    is_read         INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 16. SERVICE REQUESTS (experiences + concierge)
-- ============================================================
CREATE TABLE IF NOT EXISTS service_requests (
    id              TEXT PRIMARY KEY,
    stay_id         TEXT NOT NULL REFERENCES stays(id),
    request_type    TEXT NOT NULL,           -- 'experience' | 'concierge'
    type            TEXT NOT NULL,           -- specific type (e.g. 'bonfire', 'taxi', 'laundry')
    notes           TEXT,
    status          TEXT DEFAULT 'requested', -- 'requested' | 'in_progress' | 'completed' | 'cancelled'
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_stays_guest ON stays(guest_id);
CREATE INDEX IF NOT EXISTS idx_stays_status ON stays(status);
CREATE INDEX IF NOT EXISTS idx_stays_bed ON stays(bed_id);
CREATE INDEX IF NOT EXISTS idx_orders_stay ON orders(stay_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_ledger_stay ON ledger_entries(stay_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_cleaning_room ON cleaning_requests(room_id);
CREATE INDEX IF NOT EXISTS idx_cleaning_status ON cleaning_requests(status);
CREATE INDEX IF NOT EXISTS idx_tokens_stay ON guest_portal_tokens(stay_id);
CREATE INDEX IF NOT EXISTS idx_tokens_active ON guest_portal_tokens(active);
CREATE INDEX IF NOT EXISTS idx_beds_room ON beds(room_id);
CREATE INDEX IF NOT EXISTS idx_beds_occupied ON beds(is_occupied);
CREATE INDEX IF NOT EXISTS idx_payments_stay ON payments(stay_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(type);
CREATE INDEX IF NOT EXISTS idx_inventory_category ON inventory_items(category_id);
CREATE INDEX IF NOT EXISTS idx_inventory_low ON inventory_items(current_stock, threshold);
CREATE INDEX IF NOT EXISTS idx_grievances_stay ON grievances(stay_id);
CREATE INDEX IF NOT EXISTS idx_grievances_status ON grievances(status);
CREATE INDEX IF NOT EXISTS idx_notifications_stay ON notifications(stay_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_service_requests_stay ON service_requests(stay_id);
CREATE INDEX IF NOT EXISTS idx_service_requests_type ON service_requests(request_type);
