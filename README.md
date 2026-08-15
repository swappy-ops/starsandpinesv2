# Stars & Pines V2

Local-first hospitality operations software for **Stars & Pines**, Kasar Devi, Almora.

Stars & Pines V2 is a small, self-hosted property-management and guest-experience system. It is designed for a mountain property where the local network may be more reliable than the internet, the team needs to keep operating during outages, and the database must remain understandable and recoverable by the people running the property.

The system provides:

- A front-desk check-in tool that creates guest access QR codes.
- A guest portal for food ordering, stay information, services, billing, places, and checkout.
- A family operations dashboard for property status, kitchen orders, inventory, and checkout.
- A separate cafe flow for customers who are not staying guests.
- A FastAPI backend backed by one SQLite database file.
- Seed data, automated tests, backups, provisioning scripts, and generated API documentation.

## Contents

1. [Product Overview](#product-overview)
2. [Architecture](#architecture)
3. [Applications](#applications)
4. [Technology](#technology)
5. [Requirements](#requirements)
6. [Installation](#installation)
7. [Running the Server](#running-the-server)
8. [Application URLs](#application-urls)
9. [Daily Workflows](#daily-workflows)
10. [Authentication and Access](#authentication-and-access)
11. [Database](#database)
12. [API Overview](#api-overview)
13. [Frontend Conventions](#frontend-conventions)
14. [Configuration](#configuration)
15. [Seed Data](#seed-data)
16. [Backups and Recovery](#backups-and-recovery)
17. [Testing](#testing)
18. [Deployment](#deployment)
19. [Troubleshooting](#troubleshooting)
20. [Development Guide](#development-guide)
21. [Design References](#design-references)
22. [Project Status](#project-status)
23. [Architectural Rules](#architectural-rules)

## Product Overview

Stars & Pines V2 is organized around three connected operational surfaces and one separate cafe surface.

```text
                         +----------------------+
                         |   FastAPI Backend     |
                         |   SQLite source       |
                         |   /api/*              |
                         +----------+-----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
     +----------------+   +----------------+   +----------------+
     | Guest Entry    |   | Family App     |   | Guest Portal   |
     | Front desk     |   | Operations     |   | Guest-facing   |
     | Check-in       |   | Property       |   | Stay, menu,    |
     | QR generation  |   | Kitchen        |   | services, bill |
     | Room assignment|   | Inventory      |   | and checkout   |
     +----------------+   | Checkout       |   +----------------+
                          +----------------+

     +----------------+
     | Cafe           |
     | Public cafe    |
     | Menu and order |
     | UPI request    |
     +----------------+
```

### Core operating model

- **SQLite is the source of truth.** The application can continue operating on a local machine or local network without depending on a hosted database.
- **The backend owns state.** Order status, checkout state, tokens, payments, inventory changes, and service requests are persisted server-side.
- **The guest portal is capability-based.** A guest uses a generated access token associated with their stay instead of receiving broad staff access.
- **Guest and cafe orders are separate.** The `order_type` boundary prevents walk-in cafe orders from being confused with room charges or staying guests.
- **Billing is ledger-oriented.** Charges and payments are recorded as entries rather than silently overwriting an amount.
- **The Family App is local operations software.** It currently opens without a PIN gate and allows the operator on duty to be selected as Amrit, Raman, or Mona. The selected name is sent with operational actions.

## Architecture

### Backend request path

```text
Browser
  |
  | HTTP / JSON
  v
FastAPI application (api/main.py)
  |
  +-- API router (api/routes/__init__.py)
  |     |
  |     +-- repositories: SQL reads and writes
  |     +-- services: business rules and workflow logic
  |     +-- Pydantic request/response models
  |
  +-- SQLite connection wrapper (api/db.py)
        |
        +-- sp_v2.db
```

### Backend responsibilities

`api/main.py` is the application entry point. It:

- Creates the FastAPI application.
- Initializes the database during application startup.
- Enables permissive CORS for the local-first frontend surfaces.
- Mounts the static frontend applications.
- Adds no-cache behavior for HTML pages.
- Exposes `/health`.
- Includes the API router under `/api`.

`api/routes/__init__.py` defines the HTTP contract. It validates requests, calls services or repositories, and returns JSON responses.

`api/services/` contains workflow logic such as order idempotency, billing, kitchen operations, inventory, stays, and guest portal behavior.

`api/repositories/` contains the thin SQL access layer. The project intentionally does not use an ORM.

`api/db.py` manages SQLite connections with:

- `sqlite3.Row` dictionary-like rows.
- WAL journal mode.
- Foreign-key enforcement.
- Commit on successful context-manager exit.
- Rollback on exceptions.
- Idempotent schema initialization.

### Static frontend mounting

The backend mounts these directories when they exist:

| URL | Directory | Purpose |
|---|---|---|
| `/guest-entry/` | `guest-entry/` | Staff check-in and QR generation |
| `/guest-portal/` | `guest-portal/` | Guest stay portal |
| `/family-app/` | `family-app/` | Family operations dashboard |
| `/cafe/` | `cafe/` | Walk-in cafe menu and order flow |
| `/shared/` | `shared/` | Shared frontend API client |

## Applications

### Guest Entry

**Path:** `guest-entry/index.html`

Guest Entry is the front-desk workflow for starting a stay.

Current capabilities:

- Shows the next server-generated booking number.
- Collects guest name and phone number.
- Loads rooms and beds from the API.
- Collects check-in and check-out dates.
- Creates a stay and guest record through `/api/checkin`.
- Generates a guest portal access token.
- Displays the token as a QR code.
- Provides a WhatsApp sharing link when configured or supported by the browser.
- Displays a confirmation state after successful check-in.

Typical workflow:

1. Open `/guest-entry/`.
2. Enter the guest name and phone number.
3. Select a room or bed.
4. Choose check-in and check-out dates.
5. Select **Generate QR Code**.
6. Show the QR code to the guest or share it through WhatsApp.
7. Keep the generated token associated with the guest's stay until checkout.

### Guest Portal

**Path:** `guest-portal/index.html`

Guest Portal is accessed with a stay-specific capability token. The current portal contains ten numbered destinations:

| Tab | Purpose |
|---|---|
| Menu | Browse menu items, adjust quantities, and submit a room order |
| Stay | View guest, room, booking, and stay details |
| Bill | View the running bill and payment options |
| Service | Request cleaning, experiences, or concierge support |
| Places | Browse the local guide for Kasar Devi and nearby places |
| Perool | Browse the product categories and products store |
| Contacts | View staff contact information |
| Alerts | View notifications and order updates |
| Concerns | Submit and review grievances or concerns |
| Out | Request checkout and complete the guest checkout flow |

The portal also polls order state so a guest can see progress after submitting an order. The backend invalidates the portal token after checkout, preventing continued access to the completed stay.

### Family App

**Path:** `family-app/index.html`

Family App is the operations hub for the property team.

Current visible sections:

| Section | Purpose |
|---|---|
| Property | Occupancy, beds, rooms, revenue, low stock, and current stays |
| Kitchen | Pending, preparing, served, and cancelled orders |
| Inventory | Stock levels, low-stock warnings, restock, and consume actions |
| Checkout | Departures, bills, payment recording, and checkout completion |

The app currently has **no frontend authentication gate**. It opens directly into the dashboard. The header includes an operator selector with:

- Amrit, selected by default.
- Raman.
- Mona.

The selected operator is used for the `logged_by`, `collected_by`, or checkout operator field when the relevant action is sent to the API. This is an operator attribution control, not an authentication system.

The backend `/api/staff/login` endpoint still exists for API compatibility and other clients, but the current Family App does not call it.

### Cafe

**Path:** `cafe/index.html`

The cafe is intentionally separate from the guest portal. It serves walk-in cafe customers who do not necessarily have a room or stay.

The cafe flow uses cafe-specific API boundaries and supports:

- Cafe menu loading.
- Category filtering.
- Cafe order creation.
- Payment request creation.
- UPI payment-related state.
- A clear distinction between cafe orders and guest room orders.

## Technology

### Runtime

- Python 3.10 or newer.
- FastAPI 0.115.6.
- Uvicorn 0.34.0.
- SQLite through Python's built-in `sqlite3` module.
- Pydantic 2.10.4.
- `python-dotenv` for environment configuration.
- `schedule` for backup/operations support.

### Testing

- pytest 8.3.4.
- HTTPX 0.28.1.
- FastAPI test client support through the test suite.
- Browser verification through the local application URLs.

### Frontend

The current frontend is intentionally lightweight:

- Plain HTML.
- Inline CSS.
- Vanilla JavaScript.
- One shared API helper at `shared/api.js`.
- No Node.js build step.
- No frontend bundler.
- Google Fonts for the editorial type system.

## Requirements

### Required

- Python 3.10 or newer.
- SQLite support, included with normal Python installations.
- A modern browser such as Chrome, Edge, Firefox, or Safari.

### Recommended for development

- Git.
- A virtual environment.
- A terminal capable of running the platform's launcher script.
- A browser with developer tools for checking network requests and console errors.

### Platform notes

- `setup.sh` supports Linux and macOS.
- `setup.bat` supports Windows.
- The production provisioning scripts target Linux/systemd and nginx.
- The application itself is platform-independent as long as Python and SQLite are available.

## Installation

### Windows

Open Command Prompt or PowerShell in the repository root and run:

```bat
setup.bat
```

The Windows setup script:

1. Checks for Python.
2. Creates `venv` if it does not exist.
3. Activates the virtual environment.
4. Installs `requirements.txt`.
5. Creates `.env` from `.env.example` if needed.
6. Initializes the SQLite schema.
7. Seeds rooms, beds, menu items, staff, inventory, places, and Perool products.
8. Creates `assets/` and `backups/`.

### Linux or macOS

Run:

```bash
bash setup.sh
```

The script checks for Python 3.10+, creates a virtual environment, installs dependencies, initializes the database, seeds the default data, and creates required directories.

### Manual installation

If you prefer to control each step:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

On Windows Command Prompt:

```bat
copy .env.example .env
```

Initialize the schema and seed data:

```bash
python -c "from api.db import init_db; init_db()"
python scripts/seed.py
```

## Running the Server

### Launcher scripts

Windows:

```bat
start.bat
```

Linux or macOS:

```bash
bash start.sh
```

Both launchers start Uvicorn on `0.0.0.0:8000` with reload enabled.

### Direct Uvicorn command

After activating the virtual environment:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

For a local-only development server:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

### What happens at startup

When the application starts, FastAPI's lifespan handler calls `init_db()`.

This means the server will:

- Create missing tables from `api/schema.sql`.
- Preserve existing tables.
- Enable SQLite WAL mode for connections.
- Enable foreign-key enforcement.
- Mount the frontend directories that exist.
- Expose the interactive API documentation.

Database initialization is designed to be idempotent. Running the server should not erase existing data.

## Application URLs

With the default port:

| URL | Description |
|---|---|
| `http://localhost:8000/guest-entry/` | Front-desk guest check-in |
| `http://localhost:8000/guest-portal/` | Guest token access screen and portal |
| `http://localhost:8000/family-app/` | Family operations dashboard |
| `http://localhost:8000/cafe/` | Walk-in cafe flow |
| `http://localhost:8000/docs` | Swagger UI API documentation |
| `http://localhost:8000/redoc` | ReDoc API documentation |
| `http://localhost:8000/health` | API and database health check |

The `/health` response contains a status, database connection status, and the names of discovered SQLite tables.

Example:

```bash
curl http://localhost:8000/health
```

## Daily Workflows

### Check in a guest

1. Open Guest Entry.
2. Confirm the automatically assigned booking number.
3. Enter the guest's name and phone number.
4. Select the room or bed.
5. Enter check-in and check-out dates.
6. Generate the QR code.
7. Share the QR code with the guest.
8. Ask the guest to open the portal and enter or scan the access code.

### Guest orders food

1. Guest opens the portal with their stay token.
2. Guest opens Menu.
3. Guest selects quantities and submits the order.
4. The backend persists the order and order items.
5. The order appears in the Family App kitchen queue.
6. Staff moves the order through pending, preparing, served, or cancelled.
7. The guest portal polls and displays the current order state.

### Process a kitchen order

1. Open Family App and select the Kitchen section.
2. Review the order room/table label and item list.
3. Select **Start** to mark a pending order as preparing.
4. Prepare the food.
5. Select **Serve** when the order is complete.
6. Use **Void** only when the order should be cancelled.

### Manage inventory

1. Open Family App and select Inventory.
2. Review low-stock alerts and category tables.
3. Use `+ In` to record a restock.
4. Use `− Out` to record consumption.
5. Enter the quantity when prompted.
6. The selected on-duty operator is sent as the inventory log user.

### Check out a guest

1. Open Family App and select Checkout.
2. Select **Bill** for the departing stay.
3. Review ledger charges and payments.
4. Enter the payment amount.
5. Select cash, UPI, or card.
6. Select **Record Payment**.
7. Select **Complete Checkout** after confirming the balance and guest.
8. The stay is checked out and the guest portal token is invalidated.

## Authentication and Access

### Family App

The current Family App has no frontend authentication gate. This is intentional for the present local-first operating model. Anyone who can reach the Family App URL can operate the dashboard.

The operator selector provides attribution only:

- `Amrit` is the default.
- `Raman` and `Mona` can be selected.
- The selected name is sent in operational requests.
- The selector does not verify identity.

If the Family App is exposed outside the trusted local network, authentication and authorization must be restored before deployment.

### Staff API

The backend still exposes:

```text
POST /api/staff/login
GET  /api/staff/list
GET  /api/staff/contacts
```

The login endpoint is retained for API compatibility and future clients. Staff PINs are not returned in staff list or successful login responses.

### Guest Portal

Guest access is token-based. The token is associated with a stay and grants access to portal operations for that stay. The token should be treated as a capability credential:

- Do not publish it publicly.
- Do not log it unnecessarily.
- Do not reuse one guest's token for another stay.
- Invalidate it on checkout.
- Keep QR codes private to the guest or booking party.

### CORS

The current backend allows all origins because the product is designed for local-first deployments and separate static frontend surfaces. Review and restrict CORS before deploying to an untrusted network.

## Database

### Database file

The default database is:

```text
./sp_v2.db
```

The location can be changed with `SP_DB_PATH`.

SQLite is opened with WAL mode and foreign keys enabled. The database file is the source of truth; do not treat WhatsApp, browser state, or frontend memory as a record of operations.

### Tables

The schema currently defines the following major tables:

| Table | Responsibility |
|---|---|
| `guests` | Guest master records |
| `rooms` | Property rooms and room metadata |
| `beds` | Beds for dorms or room assignments |
| `stays` | Check-in, check-out, room assignment, and stay status |
| `menu_items` | Guest and cafe menu items |
| `orders` | Order headers and order type/status |
| `order_items` | Individual items within an order |
| `cafe_payments` | Cafe payment request/payment state |
| `ledger_entries` | Append-oriented room charges and payments |
| `payments` | Payment records used by checkout flows |
| `staff` | Staff identities and legacy PIN authentication data |
| `cleaning_requests` | Cleaning and housekeeping requests |
| `guest_portal_tokens` | Token access for guest stays |
| `tasks` | Operational task records |
| `inventory_categories` | Inventory grouping |
| `inventory_items` | Stock items and thresholds |
| `inventory_log` | Restock and consumption history |
| `grievances` | Guest concerns and grievances |
| `notifications` | Guest or staff notifications |
| `service_requests` | Guest service requests |
| `places` | Local guide places |
| `perool_categories` | Perool product categories |
| `perool_products` | Perool product catalog |

### Schema changes

The schema initializer is intentionally tolerant of already-existing tables and columns. For more complex production migrations, add an explicit migration step rather than relying on a destructive rebuild.

### Inspecting the database

List tables:

```bash
sqlite3 sp_v2.db ".tables"
```

Inspect the schema:

```bash
sqlite3 sp_v2.db ".schema"
```

Check recent orders:

```bash
sqlite3 -header -column sp_v2.db "SELECT id, order_type, status, created_at FROM orders ORDER BY created_at DESC LIMIT 20;"
```

Do not edit production data directly unless the operation is understood and a backup exists.

## API Overview

Interactive documentation is generated automatically:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

### System

```text
GET /health
```

### Staff and access

```text
POST /api/staff/login
GET  /api/staff/list
GET  /api/staff/contacts
GET  /api/portal/validate
```

### Guests, stays, and rooms

```text
POST /api/checkin
GET  /api/next-booking-number
GET  /api/guests/search
GET  /api/guests/{guest_id}
GET  /api/rooms
GET  /api/rooms/available
GET  /api/rooms/{room_id}/beds
GET  /api/beds/available
POST /api/checkout
```

### Menu and orders

```text
GET  /api/menu
GET  /api/menu/available
GET  /api/cafe/menu
POST /api/menu/{item_id}/toggle
POST /api/orders
POST /api/cafe/orders
POST /api/orders/{order_id}/status
GET  /api/portal/{token}/orders
```

### Kitchen and dashboard

```text
GET /api/kitchen/queue
GET /api/kitchen/stats
GET /api/dashboard
GET /api/dashboard/occupancy
GET /api/dashboard/arrivals
GET /api/dashboard/departures
GET /api/dashboard/revenue
```

### Billing and payments

```text
GET  /api/bill/{stay_id}
POST /api/payment
POST /api/portal/{token}/payment
POST /api/cafe/payment-request
POST /api/cafe/payment/{payment_id}
```

### Cleaning and service requests

```text
POST /api/cleaning
GET  /api/cleaning/pending
GET  /api/cleaning/stay/{stay_id}
POST /api/cleaning/{request_id}/status
POST /api/service-requests
GET  /api/service-requests
POST /api/service-requests/{request_id}/status
```

### Inventory

```text
GET  /api/inventory
POST /api/inventory/restock
POST /api/inventory/consume
```

### Guest experience

```text
GET  /api/places
GET  /api/perool/categories
GET  /api/perool/products
POST /api/grievances
GET  /api/grievances
POST /api/grievances/{grievance_id}/status
GET  /api/notifications
POST /api/notifications/{notification_id}/read
POST /api/notifications/read-all
```

For exact request models, response shapes, validation rules, and status codes, use `/docs` rather than duplicating the models in this README.

## Frontend Conventions

### Shared API client

`shared/api.js` centralizes browser-to-backend calls. Frontend code should use the existing API client methods rather than creating ad hoc `fetch` calls unless a new endpoint is being added.

The client is mounted at `/shared/api.js` by the FastAPI application and imported by the HTML applications with a relative script path.

### State ownership

- Server data is authoritative.
- Frontends may keep transient UI state such as an open panel, current cart, or selected operator.
- Refreshing the browser should not erase persisted order, stay, inventory, payment, or token state.
- Order status must be changed through the API.
- Billing must be recorded through ledger/payment endpoints.

### Visual system

The visual language is editorial, material, and restrained:

- Playfair Display for display headings.
- EB Garamond for narrative or guest-facing body copy.
- DM Sans for labels, navigation, and operational UI.
- DM Mono for codes, IDs, prices, and operational values.
- Pine, paper, cream, mist, stone, warm gold, alert red, and success green tokens.
- Square buttons, inputs, cards, and images by default.
- Hairline borders instead of decorative shadows.
- No gradients, glass effects, decorative blobs, or emoji interface icons.

The canonical reference is `pict/DESIGN.md`. The implementation shorthand is `pict/VISUAL-SYSTEM.md`.

## Configuration

Copy `.env.example` to `.env` and adjust values for the environment.

| Variable | Default | Description |
|---|---|---|
| `SP_DB_PATH` | `./sp_v2.db` | SQLite database path |
| `SP_HOST` | `0.0.0.0` | Intended server bind host |
| `SP_PORT` | `8000` | Intended server port |
| `SP_ENV` | `development` | Environment label |
| `SP_ASSETS_DIR` | `./assets` | Asset storage directory |
| `SP_BACKUP_DIR` | `./backups` | Backup directory |
| `SP_BACKUP_SCHEDULE` | `02:00` | Intended backup schedule |
| `SP_WHATSAPP_NUMBER` | empty | WhatsApp integration number placeholder |
| `SP_WHATSAPP_API_KEY` | empty | WhatsApp integration key placeholder |
| `SP_ADMIN_PIN` | empty | Seed/admin PIN placeholder |

Important:

- `.env` should not be committed.
- API keys and phone numbers should not be placed in frontend HTML.
- The launcher scripts currently pass host and port directly to Uvicorn; use the environment file for application components that read these variables, or update the launcher if a deployment needs configurable binding.
- Keep database, backup, and asset paths writable by the service account.

## Seed Data

The seed script is:

```text
scripts/seed.py
```

It populates development or fresh-install data for:

- Rooms.
- Dorm beds.
- Menu items.
- Staff records.
- Inventory categories and items.
- Local places.
- Perool categories and products.

Run it with:

```bash
python scripts/seed.py
```

The seed script uses insert-or-ignore behavior for many records so it can be rerun during development. Review the script before using it against a database containing real guest data.

To create a clean local development database, stop the server, move the existing database out of the way, then initialize and seed:

```bash
mv sp_v2.db sp_v2.db.before-clean-seed
python -c "from api.db import init_db; init_db()"
python scripts/seed.py
```

On Windows PowerShell:

```powershell
Move-Item sp_v2.db sp_v2.db.before-clean-seed
python -c "from api.db import init_db; init_db()"
python scripts/seed.py
```

Do not perform this workflow on a production database without a verified backup.

## Backups and Recovery

The backup script is:

```text
scripts/backup.py
```

Run a manual backup:

```bash
python scripts/backup.py
```

The script:

- Creates `backups/` if needed.
- Copies the configured SQLite file.
- Names backups `sp_v2_YYYYMMDD_HHMMSS.db`.
- Removes backups older than 30 days.

The repository also includes Linux provisioning files:

```text
provision/systemd/starsandpines-backup.service
provision/systemd/starsandpines-backup.timer
provision/systemd/starsandpines-web.service
provision/nginx/starsandpines
```

### Recovery procedure

1. Stop the application service.
2. Identify the latest verified backup.
3. Copy the current database to a separate quarantine filename.
4. Restore the backup to the configured `SP_DB_PATH`.
5. Start the application.
6. Check `/health`.
7. Verify rooms, stays, orders, bills, and inventory in the application.
8. Record the incident and the restored backup timestamp.

Example Linux commands:

```bash
sudo systemctl stop starsandpines-web
cp sp_v2.db sp_v2.db.before-restore
cp backups/sp_v2_YYYYMMDD_HHMMSS.db sp_v2.db
sudo systemctl start starsandpines-web
curl http://127.0.0.1:8000/health
```

SQLite WAL files may exist while the application is running. Always stop the service before making a file-level restore.

## Testing

### Run the automated suite

Activate the virtual environment and run:

```bash
pytest
```

Run with more output:

```bash
pytest -v
```

Run one test file:

```bash
pytest tests/test_phase0.py -v
```

### Test database behavior

`tests/conftest.py` sets `SP_DB_PATH` to a temporary SQLite file before importing the application database module. Each test initializes the schema and removes the temporary file afterward.

This prevents tests from modifying the repository's `sp_v2.db`.

### Browser verification checklist

After starting the server, check:

- `/health` returns status `ok`.
- `/guest-entry/` loads and room options are populated.
- Guest Entry can create a test check-in in a test database.
- `/guest-portal/` loads without a token and shows the access screen.
- A valid guest token opens the portal.
- `/family-app/` opens directly without a PIN prompt.
- Family App lists Amrit, Raman, and Mona in the operator selector.
- Menu orders appear in the Family kitchen queue.
- Kitchen status transitions persist after refresh.
- Inventory changes update stock and log the selected operator.
- Checkout records payments and invalidates the guest token.
- `/cafe/` keeps cafe orders separate from guest orders.
- No unexpected console errors or horizontal overflow appear at mobile width.

## Deployment

### Local network deployment

For a property LAN:

1. Install Python and SQLite on the host machine.
2. Clone the repository.
3. Run the platform setup script.
4. Set `SP_DB_PATH`, `SP_BACKUP_DIR`, and asset paths in `.env`.
5. Seed only if this is a new database.
6. Configure the service to bind to the LAN interface or `0.0.0.0`.
7. Configure a nightly backup.
8. Restrict the host firewall to the trusted network.
9. Open the application from a staff or guest device on the LAN.
10. Test the complete check-in, order, kitchen, payment, and checkout lifecycle.

### systemd and nginx

The `provision/` directory contains service, timer, nginx, launcher, and Firefox setup files. Review every path, user, group, domain, and environment variable before installing them.

Typical Linux service checks:

```bash
sudo systemctl status starsandpines-web
sudo journalctl -u starsandpines-web -f
sudo systemctl status starsandpines-backup.timer
sudo nginx -t
```

Do not expose the no-auth Family App to the public internet. If external access is required, put it behind an authenticated network boundary and add application-level authorization.

### Production checklist

- Use a dedicated service account.
- Keep `.env` outside version control.
- Restrict file permissions on `sp_v2.db` and `backups/`.
- Configure and test automated backups.
- Confirm the restore procedure before accepting real bookings.
- Restrict CORS to known origins where practical.
- Put the application behind TLS if traffic leaves the trusted LAN.
- Protect `/docs` if the API is externally reachable.
- Add authentication and role-based authorization before public exposure.
- Monitor service logs and disk space.
- Confirm the server timezone strategy while keeping stored timestamps in UTC.

## Troubleshooting

### `ModuleNotFoundError: No module named 'fastapi'`

The virtual environment is probably not active or dependencies are not installed.

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

Windows:

```bat
venv\Scripts\activate
python -m pip install -r requirements.txt
```

### `Address already in use`

Another process is using port 8000. Stop it or use another port:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8001 --reload
```

If the frontend calls a different API origin, update the relevant configuration or serve all surfaces from the same server.

### The app loads but data is empty

Check the following:

1. Confirm the server started successfully.
2. Open `/health`.
3. Confirm `sp_v2.db` exists at the configured `SP_DB_PATH`.
4. Run `python scripts/seed.py` for a new development database.
5. Inspect the browser Network tab for failed `/api/*` requests.
6. Review the server console for SQLite or validation errors.

### Database locked

Confirm that:

- Only the expected application processes are using the database.
- The database is on a writable local filesystem.
- The server is not being started multiple times against an unstable shared folder.
- The backup process is not copying or replacing the database while writes are active.
- WAL sidecar files are not being deleted independently of the database.

### Guest token does not work

Check:

- The token was copied completely.
- The associated stay has not been checked out.
- The token has not expired or been invalidated.
- The browser is reaching the same backend that created the token.
- The API response from `/api/portal/validate`.

### Family App shows no PIN screen

This is expected in the current version. Family App opens directly and uses the on-duty operator selector for attribution. This selector does not provide security.

### Static app returns 404

Confirm that the expected directory exists:

```text
guest-entry/index.html
guest-portal/index.html
family-app/index.html
cafe/index.html
```

The backend only mounts directories that exist at startup. Restart Uvicorn after creating or renaming an application directory.

### Favicon 404 in the browser console

The application currently does not provide a root favicon. This does not block the workflows, but it creates a browser console 404. Add a local favicon and reference it from each HTML entry point when addressing frontend polish.

## Development Guide

### Adding an API endpoint

1. Define or update the request model in `api/routes/__init__.py` or a nearby module.
2. Add the route in the appropriate API group.
3. Put non-trivial business rules in `api/services/`.
4. Put SQL access in `api/repositories/`.
5. Update the schema only when the data model genuinely requires it.
6. Add or update tests.
7. Update `shared/api.js`.
8. Wire the endpoint into the relevant frontend.
9. Verify loading, empty, error, success, and disabled states.
10. Run `pytest` and browser checks.

### Adding a frontend flow

1. Identify the owning backend endpoint.
2. Add the API client method first.
3. Keep server state and UI state separate.
4. Preserve existing API contracts.
5. Use the established visual tokens.
6. Add semantic labels and keyboard-accessible controls.
7. Check mobile widths before considering the work complete.
8. Confirm the flow survives a reload where persistence is expected.

### Modifying the database

1. Update `api/schema.sql`.
2. Consider existing databases and migration behavior.
3. Update seed data if the new records are required for development.
4. Add tests that prove the table or column exists.
5. Add a data migration for production if the change cannot be safely handled by idempotent initialization.
6. Back up a real database before applying the change.

### Logging and operational attribution

Operational writes should include the staff/operator value available from the calling workflow. The Family App currently uses the selected operator name:

```text
Amrit
Raman
Mona
```

Do not use the browser as the only source of truth for financial state. The API and SQLite database must record the actual operation.

## Design References

The design source files are under `pict/`:

| File | Purpose |
|---|---|
| `pict/DESIGN.md` | Canonical Stars & Pines design system |
| `pict/VISUAL-SYSTEM.md` | Practical CSS tokens and component patterns |
| `pict/DESIGN-HANDOFF.md` | Design handoff and implementation details |
| `pict/DESIGN-MANIFEST.json` | Design manifest |
| `DESIGN-IMPLEMENTATION-PLAN.md` | Current redesign surface map and implementation plan |
| `DESIGN-AUDIT.md` | Visual and accessibility audit findings |
| `OPERATIONS-PLAYBOOK.md` | Daily operating procedures, rollout plan, contingencies, and recovery guides |

The visual system favors:

- Editorial hierarchy over generic SaaS dashboard styling.
- Square geometry and hairline borders.
- Restrained earth, paper, stone, pine, and warm-gold colors.
- Clear labels and operational density.
- Tables and lists when they communicate operations better than cards.
- Responsive layouts without horizontal overflow.

## Project Status

### Implemented

- FastAPI backend.
- SQLite database with idempotent initialization.
- Guest Entry check-in and QR generation.
- Guest Portal token access.
- Guest menu ordering.
- Kitchen queue and order state transitions.
- Billing and checkout workflow.
- Cleaning and service request endpoints.
- Inventory tracking and logs.
- Grievances and notifications.
- Places guide and Perool catalog endpoints.
- Separate cafe menu/order/payment boundary.
- Shared browser API client.
- Seed data scripts.
- Backup script and Linux provisioning files.
- Family App direct access with Amrit, Raman, and Mona operator selection.

### Known limitations

- Family App operator selection is attribution, not authentication.
- Role-based staff access is not implemented.
- CORS is permissive for local-first development.
- WhatsApp integration values are placeholders unless configured.
- Payment provider integration must be configured before treating online payment as live.
- Some operational backend routes are not yet represented as visible Family App sections.
- Room photos and some data-driven guest content remain future work.
- Favicon is not currently served.

### Planned work

Potential next areas include:

- Role-based access for kitchen, operations, and management.
- Inventory low-stock notifications.
- Order ETA display using menu preparation times.
- Room photography and richer room selection.
- Data-driven Wi-Fi and property information.
- Full browser end-to-end lifecycle coverage.
- Hardened authentication before any public exposure.
- Explicit data migrations for production schema changes.

## Architectural Rules

These rules protect the operational model and should be treated as non-negotiable unless the product owner explicitly changes them:

```text
SQLite is the source of truth.
WhatsApp is a communication surface, never the database.
Guest orders and cafe orders remain separate.
Booking IDs are server-generated.
Guest portal tokens are capability credentials.
Order status is persistent server state.
Billing entries are never silently deleted.
Stored timestamps use UTC; frontends format for local display.
Never expose the Family App without a trusted network or real authentication.
Never change production data without a verified backup.
```

## License and Operations

Review the repository's licensing and operational policies before distributing the software or exposing it outside the Stars & Pines property network. Keep guest data, phone numbers, payment information, access tokens, and database backups private.
