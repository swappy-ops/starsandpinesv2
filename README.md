# Stars & Pines V2

Local-first hospitality operations system for Stars & Pines, Kasar Devi.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  FastAPI Backend                 │
│  SQLite (sp_v2.db) — single file, no ORM        │
│                                                  │
│  /api/guests    /api/stays    /api/orders        │
│  /api/ledger    /api/menu     /api/cleaning      │
│  /api/staff     /api/tokens                      │
└──────────┬──────────────────────┬────────────────┘
           │                      │
    ┌──────▼──────┐        ┌──────▼──────┐
    │  GUEST      │        │  FAMILY     │
    │  ENTRY      │        │  DASHBOARD  │
    │             │        │             │
    │ guest-entry │        │ family-     │
    │ .html       │        │ dashboard   │
    │             │        │ .html       │
    │ Check-in    │        │             │
    │ Token gen   │        │ Kitchen     │
    │ QR share    │        │ Orders      │
    └─────────────┘        │ Requests    │
                           │ Checkout    │
                           │ Logs        │
                           └──────┬──────┘
                                  │
                           ┌──────▼──────┐
                           │  GUEST      │
                           │  PORTAL     │
                           │             │
                           │ portal      │
                           │ .html       │
                           │             │
                           │ Welcome     │
                           │ Menu/Order  │
                           │ Bill        │
                           │ Cleaning    │
                           └─────────────┘
```

## Three Products

### 1. Guest Entry (`guest-entry.html`)
Front desk only. Staff enters guest details, assigns room, generates access token, shares QR via WhatsApp.

### 2. Guest Portal (`portal.html`)
Guest scans QR → sees room details, orders food, requests cleaning, views running bill.

### 3. Family Dashboard (`family-dashboard.html`)
Operations hub for Rajat, Mona, Raman, kitchen staff. Kitchen queue, order dispatch, guest requests, cleaning, checkout, inventory, logs.

## Database

Single SQLite file (`sp_v2.db`). No ORM. Raw SQL only.

Core tables:
- `guests` — guest master
- `rooms` — rooms and dorm beds
- `stays` — check-in/out, status, charges
- `menu_items` — cafe menu
- `orders` / `order_items` — food orders
- `ledger_entries` — append-only billing
- `staff` — PIN auth
- `cleaning_requests` — housekeeping queue
- `guest_portal_tokens` — QR access tokens

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Seed sample data
python scripts/seed.py

# Start server
uvicorn api.main:app --reload --port 8000
```

## Design Principles

1. **Local-first** — Kasar Devi network is unreliable. SQLite on disk.
2. **Single file** — One `.db` file. Nightly backup to Google Drive.
3. **No ORM** — Rajat should be able to read raw SQL at 11 PM during peak season.
4. **Append-only billing** — Ledger entries are never deleted. Soft deletes everywhere.
5. **Timestamps UTC** — Frontend converts to IST for display.

## Directory Structure

```
StarsPinesV2/
├── api/                    # FastAPI backend
│   ├── main.py             # Application entry
│   ├── db.py               # SQLite connection
│   ├── schema.sql          # Database schema
│   ├── repositories/       # SQL queries (thin layer)
│   ├── services/           # Business logic
│   └── routes/             # HTTP endpoints
├── frontend/               # Single-file HTML apps
│   ├── guest-entry.html    # Check-in tool
│   ├── portal.html         # Guest portal
│   └── family-dashboard.html  # Operations dashboard
├── assets/                 # Media storage
├── backups/                # Nightly DB copies
├── scripts/                # Init, seed, backup
├── provision/              # systemd, nginx, launchers
├── tests/                  # pytest
└── docs/                   # Documentation
```

## Migration from Firebase

The existing Firebase version (`archive/firebase-version/`) is preserved as reference and fallback. V2 replaces it once stable.

1. Export Firebase data → CSV
2. Run migration script
3. Manual review 
4. Switch frontend to FastAPI endpoints
5. Archive Firebase (read-only, 90 days)
