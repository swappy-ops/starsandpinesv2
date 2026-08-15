# Stars & Pines V2 Operations Playbook

Practical plan for getting Stars & Pines V2 into dependable daily use at Stars & Pines, Kasar Devi.

**Document status:** Operational draft for pilot and launch preparation
**Repository:** https://github.com/swappy-ops/starsandpinesv2
**Primary server assumption:** One local property server on the trusted Stars & Pines network
**Primary operators:** Amrit, Raman, and Mona
**Companion documents:** `README.md`, `DESIGN-AUDIT.md`, `pict/DESIGN.md`

## 1. Purpose

This document is not a feature list. It is the plan for making the software useful during an actual working day.

It defines:

- Who does what.
- What happens before opening, during service, and at closing.
- How check-in, orders, inventory, payments, and checkout are handled.
- What to do when Wi-Fi, power, the server, QR codes, payments, or the database fail.
- How to run a controlled pilot before depending on the system for every guest.
- Which current limitations must be resolved before public or internet exposure.
- How the team returns from paper/manual operation back into the system without losing records.

The objective is not “the app is installed.” The objective is:

> Every guest, order, payment, stock movement, and checkout can be understood by the team, recovered after a failure, and reconciled at the end of the day.

## 2. Operating Principles

These rules should be printed and kept beside the operations computer.

1. **The database is the source of truth.** WhatsApp messages, browser tabs, screenshots, and memory are communication aids, not records.
2. **Do not silently work around a failed operation.** Record the failure, use the manual fallback, and reconcile later.
3. **Never create a second guest, order, or payment just because the screen appears slow.** Check the database or refresh first.
4. **Every manual transaction gets a temporary reference number.** Use the date, time, and operator initials.
5. **Every shift handover includes open work.** Open stays, unpaid bills, preparing orders, pending requests, low stock, and manual records must be named.
6. **No one exposes the Family App to the public internet in its current no-auth state.** It is for a trusted local network until real authentication and authorization are restored.
7. **Never restore or replace `sp_v2.db` while the server is running.** Stop the service first.
8. **Never seed a production database casually.** `scripts/seed.py` is for setup/development unless each insert has been reviewed.
9. **Do not promise a guest that payment succeeded until the payment state is visible in the system or verified through the payment provider.**
10. **A backup is not proven until a restore test has succeeded.**

## 3. Current System Reality

### 3.1 What works now

The current repository contains:

- FastAPI backend with SQLite.
- Guest Entry check-in flow.
- Guest portal token access.
- Guest menu and room-order flow.
- Family dashboard for property, kitchen, inventory, and checkout.
- Family App operator selector for Amrit, Raman, and Mona.
- Cafe menu/order/payment-request flow.
- Cleaning and service-request APIs.
- Grievances, notifications, places, and Perool API surfaces.
- Database initialization and seed scripts.
- Automated tests.
- Manual backup script.
- Linux provisioning files.

### 3.2 What is intentionally different from a hardened production PMS

- The Family App currently has **no frontend authentication gate**.
- The operator selector identifies the person operating the screen but does not verify identity.
- The backend still has a legacy staff login endpoint, but the Family App does not currently use it.
- CORS is permissive.
- Payment integrations may contain placeholders and must not be presented as live until configured and tested.
- Some backend operational routes are not yet visible as Family App sections.
- The checked-in nginx configuration contains legacy filenames and routes that do not exactly match the current `*/index.html` directory structure.
- The checked-in `starsandpines-web.service` starts nginx, not Uvicorn. Production deployment must decide whether nginx is only a reverse proxy/static layer or whether Uvicorn is managed separately.

### 3.3 Go-live rule

The team may run a limited pilot on a trusted LAN after the pilot checklist passes. Do not expose the current Family App directly to the internet or an untrusted network.

## 4. Proposed Team Model

The names below are an operating proposal. Change the assignment if the actual shift responsibilities differ.

| Person | Suggested primary responsibility | Backup responsibility |
|---|---|---|
| Amrit | Guest-facing desk, check-in, guest portal help, QR handoff | Guest requests and checkout support |
| Raman | Kitchen queue, order status, stock movements | Cafe orders and service requests |
| Mona | Shift lead, payment review, exception approval, end-of-day reconciliation | Check-in and guest support |

### 4.1 Shared rules for all operators

- Use the Family App operator selector before making an attributable action.
- Do not share one person's operator selection while another person performs the action.
- Do not use the same browser tab for guest-facing and staff-facing work if it risks exposing the dashboard.
- Do not write guest access tokens in public group chats.
- Call out every exception verbally and write it in the shift log.
- If the system is down, use the paper fallback immediately rather than waiting silently.

### 4.2 Shift handover format

Every handover should answer these questions:

```text
Date / time:
Outgoing operator:
Incoming operator:

Current occupied rooms/beds:
Expected arrivals:
Expected departures:
Unpaid or disputed bills:
Open kitchen orders:
Open guest/service requests:
Low-stock items:
Manual fallback records created:
Known technical problems:
Next action and owner for each open item:
```

## 5. Staged Action Plan

Do not move directly from “code exists” to “every guest depends on it.” Use the following stages.

### Stage 0: Confirm the operating decision

**Owner:** Mona or property owner
**Output:** Written decisions, not assumptions

Decide:

- Which computer is the primary operations terminal.
- Which computer is the backup terminal.
- Who is responsible for the server power and network hardware.
- Whether the server is a laptop, desktop, mini PC, or hosted machine.
- Whether the property network is private and password-protected.
- Who can access the database file.
- Who approves refunds, voids, manual bill corrections, and checkout overrides.
- Whether Family App no-auth is acceptable for the pilot LAN.
- What payment methods are officially accepted.
- Which paper forms are used during outages.
- Where the daily shift log is kept.

Do not proceed until the team can answer “what do we do if the server does not start?” in one sentence.

### Stage 1: Technical baseline

**Owner:** Raman or technical owner
**Output:** A repeatable installation on the actual property machine

1. Install Python 3.10+.
2. Clone the repository.
3. Create and activate a virtual environment.
4. Install `requirements.txt`.
5. Create `.env` from `.env.example`.
6. Set a deliberate absolute database path if the working directory can change.
7. Initialize the database.
8. Seed a development database only.
9. Run `python -m pytest -q`.
10. Start Uvicorn manually.
11. Open `/health`.
12. Open all application URLs from a second device on the local network.
13. Record the server IP address and hostname.
14. Record the exact start/stop commands.
15. Make a manual database backup.
16. Restore that backup into a temporary test database.

Baseline acceptance:

- Server starts after a reboot.
- `/health` reports database connected.
- All four current frontend surfaces load.
- A test check-in can be created.
- A test guest order reaches the kitchen queue.
- The operator name is recorded on an operational write.
- A test payment and checkout can be completed.
- The database backup can be copied and reopened.

### Stage 2: Correct deployment packaging

**Owner:** Technical owner
**Output:** One documented deployment path

Before installing the files under `provision/`, reconcile them with the current repository.

Required decisions:

- Is Uvicorn run directly by systemd?
- Is nginx a reverse proxy to Uvicorn, or does it serve static HTML separately?
- Are the current URLs `/guest-entry/`, `/guest-portal/`, `/family-app/`, and `/cafe/` the production URLs?
- Will the database be owned by the Uvicorn service account or a separate restricted account?
- Where do backups live if the server disk fails?
- How will staff reach the system if nginx is unavailable?

Do not install the existing nginx vhost unchanged. Its `try_files` entries reference legacy filenames such as `guest-portal.html` and `dashboard.html`, while the current application uses directories with `index.html` files. Update and test the vhost first.

Recommended target architecture:

```text
Client browser
    |
    v
nginx :80 or :443
    |
    +-- reverse proxy /api/* -> Uvicorn 127.0.0.1:8000
    +-- serve current frontend directories
    |
    v
Uvicorn FastAPI process
    |
    v
SQLite database on local disk
```

For a very small pilot, Uvicorn alone is acceptable on the trusted LAN. For production, use a service manager and a tested reverse proxy.

### Stage 3: Load realistic test data

**Owner:** Mona and Amrit
**Output:** A database that matches the property

Replace sample assumptions with real operational data:

- Actual rooms and room names.
- Actual dorm beds.
- Actual base prices.
- Actual check-in and check-out rules.
- Actual menu items, prices, categories, and preparation times.
- Actual inventory units and thresholds.
- Actual places descriptions and travel estimates.
- Actual staff contact information.
- Actual payment instructions.

Do not edit live data directly in SQLite without a backup. Use a controlled data-loading script or a reviewed SQL change.

### Stage 4: Run a shadow pilot

**Duration:** 3 to 7 operating days
**Owner:** Entire team
**Output:** Evidence from real work while the old process remains the fallback

During the shadow pilot:

- Record every real check-in in the system and on the existing paper/booking process.
- Send guest QR codes, but keep the normal contact method available.
- Put real test or low-risk orders through the system.
- Reconcile every order against the kitchen's existing method.
- Record real inventory movements and compare at close.
- Generate test bills and compare them with the agreed billing process.
- Do not rely on automated payment success until verified.
- Log every delay, duplicate, unclear label, or operator mistake.

Pilot metrics:

| Metric | Target before full rollout |
|---|---|
| Check-ins completed without technical intervention | 95%+ |
| Guest tokens delivered correctly | 100% |
| Orders reaching kitchen correctly | 100% |
| Duplicate orders caused by UI uncertainty | 0 |
| Checkout totals reconciled | 100% |
| Successful daily backup verification | 100% of pilot days |
| Staff able to use manual fallback | 100% of operators |

### Stage 5: Controlled go-live

Go live only after:

- The pilot has no unresolved financial discrepancy.
- Staff can perform every critical workflow without technical assistance.
- The manual fallback forms are printed.
- A backup and restore test has been completed.
- A power/network/server contingency has been rehearsed.
- The local server and backup device have stable power protection.
- The team knows which URLs to open.
- The no-auth Family App is restricted to the trusted LAN.
- Mona has authority to pause digital payments or revert to manual operation.

During the first full week:

- Keep the previous process available.
- Reconcile every day, not just at the end of the week.
- Do not introduce unrelated redesigns or schema changes.
- Review the incident log at the end of each shift.

## 6. Daily Operating Guide

### 6.1 Opening checklist

**Target:** Complete before the first arrival or breakfast service.

#### Server and network

- [ ] Server has power and is connected to the intended network.
- [ ] Router/access point is powered and internet/LAN status is normal.
- [ ] Confirm the server IP address has not changed.
- [ ] Open `http://SERVER-IP:8000/health` or the production URL.
- [ ] Confirm the health response says `status: ok` and `database: connected`.
- [ ] Check that the database file is on the expected disk.
- [ ] Confirm there is enough disk space for the day.
- [ ] Confirm the latest backup exists.
- [ ] If the server restarted overnight, inspect the service log.

#### Family App

- [ ] Open `/family-app/`.
- [ ] Confirm the dashboard loads without a PIN prompt.
- [ ] Confirm Amrit, Raman, and Mona are present in the operator selector.
- [ ] Select the person currently operating the terminal.
- [ ] Review occupancy and current stays.
- [ ] Review arrivals and departures using the available data.
- [ ] Review the kitchen queue.
- [ ] Review low-stock items.
- [ ] Review checkout balances and expected departures.

#### Guest Entry

- [ ] Open `/guest-entry/` on the front-desk device.
- [ ] Confirm rooms and beds load.
- [ ] Confirm the next booking number is reasonable.
- [ ] Create one test only if the property permits it; otherwise confirm the form and API response without creating a real stay.

#### Kitchen

- [ ] Confirm Raman or the kitchen operator knows where the queue is displayed.
- [ ] Confirm the printer, kitchen display, or backup paper order board is available.
- [ ] Confirm the first shift's menu availability.
- [ ] Confirm low-stock ingredients before accepting menu promises.

#### Cash and payment

- [ ] Confirm starting cash float.
- [ ] Confirm UPI/payment QR is visible and working if used.
- [ ] Confirm the person approving refunds or voids is on shift.
- [ ] Confirm paper receipt or manual payment log is available.

### 6.2 Arrival/check-in procedure

1. Ask for the guest's booking name and contact number.
2. Confirm the room/bed assignment before creating a stay.
3. Check the dates carefully.
4. Create the guest entry once.
5. Verify the guest name, room, dates, and booking number on the confirmation screen.
6. Generate the access QR/token.
7. Send or show the QR privately to the guest.
8. Ask the guest to open the portal while still at the desk.
9. Confirm that the guest sees the correct name and room.
10. Tell the guest how to request food, cleaning, help, and checkout.
11. If the guest cannot access the portal, write the token on the approved private handoff method and use the manual support fallback.

Never create a second check-in because the confirmation appears slow. Refresh or check the stay list first.

### 6.3 Guest portal orientation

At check-in, explain only the high-value paths:

- **Menu:** order food for the room/stay.
- **Stay:** confirm room and booking details.
- **Bill:** view charges and payment state.
- **Service:** request cleaning or assistance.
- **Places:** find local recommendations.
- **Alerts:** track order/service updates.
- **Out:** request checkout.

Do not tell guests that a payment is complete solely because they saw a button or redirect. Confirm the payment state.

### 6.4 Kitchen order procedure

For every order:

1. Check the room/table label.
2. Check item quantities.
3. Check notes and dietary information.
4. Check whether it is a guest order or cafe order.
5. Start preparation in the Family App.
6. Prepare the items.
7. Verify the complete order before serving.
8. Serve or hand off.
9. Mark served only after handoff.
10. If an item cannot be made, contact the guest/operator before voiding or substituting.

Never mark an order served merely to remove it from the queue.

### 6.5 Inventory procedure

Record stock movement at the time it occurs, not from memory at the end of the day.

Use `+ In` for:

- Supplier deliveries.
- Market purchases.
- Transfers into the counted store.
- Corrected counts approved by the shift lead.

Use `− Out` for:

- Kitchen consumption.
- Spoilage.
- Staff use.
- Damaged or discarded stock.

For every adjustment, note the reason in the shift log if the current UI only requests a quantity. The inventory log must be explainable during reconciliation.

### 6.6 Checkout procedure

1. Confirm the departing guest and room.
2. Open the correct stay in Checkout.
3. Review room charges, food orders, payments, and balance.
4. Ask the guest to confirm disputed items before payment.
5. Record payment with the correct method.
6. Reopen or refresh the bill and verify the resulting balance.
7. Complete checkout only after the operator approves the final state.
8. Confirm that the guest no longer has portal access.
9. Mark the room/bed for cleaning through the approved housekeeping process.

If the guest disputes an item, do not delete it. Pause checkout, record the dispute, and escalate to Mona.

### 6.7 Cafe procedure

1. Use `/cafe/`, not the guest portal, for walk-in customers.
2. Confirm the order is marked as cafe order type.
3. Take payment or create the payment request according to the current accepted method.
4. Give the cafe order a clear customer/table reference.
5. Confirm it appears in the kitchen queue as cafe work.
6. Do not attach a cafe order to a room unless the property has explicitly approved that business case.

### 6.8 Closing checklist

#### Operations reconciliation

- [ ] All kitchen orders are served, cancelled, or explicitly carried over.
- [ ] All guest service requests have an owner or a handover note.
- [ ] All expected departures are checked out or documented.
- [ ] All payments are recorded with method.
- [ ] All disputes are listed for Mona.
- [ ] All stock movements are entered.
- [ ] Low-stock items are copied into the next-day purchase list.
- [ ] Cafe orders are reconciled separately from guest orders.
- [ ] Manual fallback transactions are entered or clearly queued for entry.

#### Financial close

- [ ] Compare cash collected with the cash log.
- [ ] Compare UPI/card/payment-provider totals with the system.
- [ ] Verify no payment is marked successful without evidence.
- [ ] Verify voids, refunds, and corrections have an approver.
- [ ] Record the closing cash amount.

#### Technical close

- [ ] Run a manual backup if the automated backup has not completed.
- [ ] Confirm the backup file exists and has a non-zero size.
- [ ] Confirm the server remains powered if it is the overnight host.
- [ ] Record open sessions, known failures, and next actions.
- [ ] Lock the operations terminal or close the browser if the room is accessible to guests.

## 7. Manual Fallback Forms

Print these forms before pilot launch. Store them in a clearly labeled folder beside the operations terminal.

### 7.1 Manual check-in form

```text
Manual check-in reference: __________
Date/time: __________  Operator: __________

Guest name: __________________________________
Phone: _______________________________________
Booking/reference: ____________________________
Room/bed: ____________________________________
Check-in date/time: ____________________________
Expected check-out date/time: _________________
Payment/deposit note: _________________________
Portal token/QR delivered:  Yes / No
Token reference, if safe to record: ____________

System entry completed later by: ______________
System booking ID: ____________________________
Reconciled by: __________________ Date: ________
```

### 7.2 Manual food order form

```text
Manual order reference: _______________________
Date/time: __________  Operator: __________
Guest room OR cafe table: _____________________
Guest/cafe order: _____________________________

Item                         Qty       Notes
________________________________________________
________________________________________________
________________________________________________

Order accepted by kitchen: __________
Started: __________  Served: __________  Voided: __________
Payment/charge note: __________________________

System order ID entered later: ________________
Reconciled by: __________________ Date: ________
```

### 7.3 Manual payment form

```text
Manual payment reference: ____________________
Date/time: __________  Operator: __________
Guest/stay or cafe reference: _________________
Amount: ______________________________________
Method: Cash / UPI / Card / Other: ____________
Provider/reference number: ____________________
Evidence attached: Yes / No
Approved by: _________________________________

System payment ID entered later: ______________
Reconciled by: __________________ Date: ________
```

### 7.4 Manual inventory form

```text
Date/time: __________  Operator: __________
Item: ________________________________________
Unit: ________________________________________
Quantity: ____________________________________
Movement: Delivery / Consumption / Spoilage / Correction
Reason: ______________________________________
Approved by, if correction: ___________________

System log entered later: _____________________
Reconciled by: __________________ Date: ________
```

## 8. Contingency Plans

### C1: Guest cannot connect to Wi-Fi

**Symptoms:** Portal or Family App does not load, but devices may still have power.

**Immediate action:**

1. Confirm whether the problem affects one device or all devices.
2. Ask the operator to check the network name and password.
3. Try the server IP directly instead of a hostname.
4. Check whether the server itself is reachable from another device.
5. Do not reset the router during active service unless approved by the shift lead.

**Fallback:**

- Use the operations terminal if it is still connected.
- Use paper check-in and order forms for guests.
- Give guests the approved manual contact method for food and support.
- Keep recording manual references.

**Recovery:**

- Reconnect one staff device first.
- Verify `/health`.
- Enter manual records into the system in chronological order.
- Reconcile every inserted record against the paper form.

### C2: Internet is down but the LAN is working

The system is designed to operate locally when the server and LAN are available.

**Expected behavior:**

- Local application URLs should still work.
- Guest QR/token validation should work against the local server.
- External WhatsApp sharing may not work.
- External payment confirmation may not work.
- Google Drive or remote backup may not work.

**Procedure:**

1. Keep the local server running.
2. Use local URLs or the server IP.
3. Use manual guest communication instead of WhatsApp.
4. Accept cash or approved offline methods if policy permits.
5. Record any payment that still needs online confirmation.
6. Do not claim remote backup success.
7. Back up to a local USB/device when possible.

### C3: Server is unreachable

**Immediate action:**

1. Check server power.
2. Check network cable or Wi-Fi.
3. Try a second device.
4. Check the server's local screen if available.
5. Check whether the process is listening on port 8000.

Linux checks:

```bash
systemctl status starsandpines-web
systemctl status nginx
ss -ltnp | grep -E ':80|:8000'
curl http://127.0.0.1:8000/health
```

Development/Uvicorn check:

```bash
ps aux | grep uvicorn
```

**Fallback:** Switch immediately to paper forms. Do not spend 30 minutes debugging while guests wait.

**Recovery:**

1. Restart only the application process first.
2. Check `/health`.
3. Do not restart or replace the database unless the service cannot start because of database corruption.
4. Enter manual records after stability is confirmed.

### C4: Power outage

**Preparation:**

- Put the server and router on a UPS if possible.
- Keep one charged device available.
- Keep printed forms, contact numbers, and current occupancy list offline.
- Know the safe shutdown procedure.

**During outage:**

1. Switch to paper check-in, orders, and payment logs.
2. Do not write transactions into a browser that cannot reach the server.
3. Keep a clear outage start time.
4. Keep references sequential.
5. Preserve receipts and payment evidence.

**After power returns:**

1. Wait for the router/server to stabilize.
2. Check `/health`.
3. Confirm the database opens.
4. Take a backup before entering a large batch of manual records.
5. Enter records one at a time.
6. Reconcile each record immediately.

### C5: Database cannot be opened or appears corrupted

**Do not:**

- Delete `sp_v2.db`.
- Run seed scripts.
- Copy a random database over it.
- Continue taking digital payments as if the system were accurate.

**Procedure:**

1. Stop Uvicorn/nginx/application services.
2. Preserve the current database and any `-wal` or `-shm` files.
3. Copy the entire database set to a quarantine directory.
4. Record the time and error message.
5. Run SQLite integrity checking on a copy:

```bash
sqlite3 sp_v2.db "PRAGMA integrity_check;"
```

6. Identify the latest known-good backup.
7. Restore only after Mona or the technical owner approves.
8. Start the service and check `/health`.
9. Compare current occupancy, stays, orders, balances, and stock to paper records.
10. Enter transactions created after the backup.

### C6: QR code does not scan

**Immediate checks:**

- Increase screen brightness.
- Clean the guest's camera lens.
- Display the QR at a readable size.
- Try the token manually if the portal supports code entry.
- Verify the token belongs to the correct guest/stay.

**Fallback:** Use the access code through the approved private handoff. Never send a guest token to a public group.

**If the token is wrong or invalid:**

1. Do not create a second stay immediately.
2. Check the original confirmation record.
3. Validate the token through the portal/API.
4. Reissue or correct access only through an approved staff workflow.
5. Record the incident if a token was exposed or sent to the wrong person.

### C7: Order appears duplicated

**Immediate action:**

1. Stop pressing Submit.
2. Refresh the order list.
3. Compare item list, time, room/table, and idempotency/reference data.
4. Ask the kitchen not to start both until confirmed.
5. Keep the original and void only the accidental duplicate with approval.

**Never:** Delete both orders because neither looks correct.

### C8: Order is stuck in pending/preparing

1. Check whether the kitchen actually received it.
2. Confirm the room/table label.
3. Contact the kitchen operator.
4. If the order is being prepared, do not create a replacement.
5. If the item is unavailable, contact the guest and agree on a replacement/refund path.
6. Update the status only when the real-world state is known.

### C9: Payment is unclear or provider is unavailable

**Procedure:**

1. Ask for the provider reference or screenshot.
2. Check the provider dashboard if internet is available.
3. Check the system bill and payment records.
4. Do not record a second payment until the first is resolved.
5. Mark the payment as pending in the manual log if the system cannot express the state.
6. Escalate to Mona before checkout.

**Checkout rule:** An unclear payment is not the same as a successful payment.

### C10: Wrong room, wrong guest, or wrong amount

**Procedure:**

1. Stop the workflow.
2. Do not delete the historical record.
3. Record what is wrong and when it was noticed.
4. Ask Mona to approve the correction path.
5. Use the appropriate correction, refund, transfer, or ledger action supported by the API.
6. Add a note to the shift log with original and corrected references.
7. Verify the final bill and guest portal access.

### C11: Operator terminal is lost, stolen, or exposed

Because Family App is currently unauthenticated, treat physical access to the terminal as operational access.

1. Disconnect the device from the network.
2. Inform Mona immediately.
3. Move operations to the backup device.
4. Change network credentials if the device stored them.
5. Review recent operational activity.
6. Rotate guest tokens if guest data may have been exposed.
7. Plan authentication before returning the device to service.

### C12: Guest data or token is sent to the wrong person

1. Do not attempt to hide the incident.
2. Record the guest, token, time, recipient, and channel.
3. Ask the unintended recipient to delete the message if appropriate.
4. Invalidate or replace the token if possible.
5. Inform Mona/property management.
6. Review whether other guest information was included.
7. Document corrective action.

## 9. Reconciliation Procedures

### 9.1 Manual-to-system reconciliation

For each manual reference:

1. Find the corresponding system record.
2. Compare guest/customer, room/table, amount, items, time, and operator.
3. Record the system ID on the paper form.
4. Mark the paper form reconciled.
5. Have a second person review payments and checkouts.

### 9.2 End-of-day reconciliation table

```text
Category              Manual count   System count   Difference   Owner   Resolved?
Check-ins             __________     __________     __________   _____   _________
Guest orders          __________     __________     __________   _____   _________
Cafe orders           __________     __________     __________   _____   _________
Payments              __________     __________     __________   _____   _________
Checkouts             __________     __________     __________   _____   _________
Inventory movements   __________     __________     __________   _____   _________
```

### 9.3 Financial discrepancies

Classify each difference as:

- Timing difference.
- Missing system entry.
- Duplicate system entry.
- Wrong amount.
- Wrong payment method.
- Unverified provider payment.
- Refund/void pending approval.
- Unknown.

Unknown differences remain open until resolved. Do not make an unexplained adjustment simply to make totals match.

## 10. Backup and Recovery Schedule

### Daily

- Confirm the scheduled backup completed.
- Confirm the backup file exists.
- Record backup timestamp in the shift log.
- Keep at least one copy on a different physical device when possible.

### Weekly

- Test opening a recent backup on a non-production machine.
- Check disk space.
- Check service restart behavior.
- Review open incidents and recurring failures.

### Monthly

- Perform a full restore drill.
- Confirm the restored database has expected tables and sample records.
- Review operator access and physical device access.
- Review payment and guest-token handling.
- Confirm the manual fallback forms are still current.
- Review whether new app features need to be reflected in this playbook.

### Recovery drill

Run this outside service hours:

1. Stop the test service.
2. Restore the latest backup to a separate path.
3. Start a test Uvicorn process with `SP_DB_PATH` pointing to the restored copy.
4. Open `/health`.
5. Check a guest, order, bill, inventory item, and portal token.
6. Record how long recovery took.
7. Record any missing files or configuration.

Target recovery times:

| Scenario | Initial target |
|---|---:|
| Browser/device replacement | 15 minutes |
| Uvicorn restart | 5 minutes |
| Router restart | 10 minutes |
| Restore from local backup | 30 minutes |
| Restore after server replacement | 2 hours |

## 11. Security and Privacy Plan

### Before pilot

- Put the server on a private property network.
- Use a strong Wi-Fi password.
- Do not port-forward the server.
- Restrict physical access to the server and database.
- Keep `.env`, database files, backup files, and tokens private.
- Create a written incident contact list.

### Before full production

- Restore Family App authentication or place it behind a trusted authenticated network boundary.
- Add authorization by role for payments, checkout, inventory corrections, and staff management.
- Restrict CORS.
- Use HTTPS if traffic leaves the trusted LAN.
- Protect API documentation if externally reachable.
- Add audit logs for sensitive operations.
- Define guest data retention and deletion rules.
- Define who may access database backups.

### Sensitive data handling

Treat these as sensitive:

- Guest names and phone numbers.
- Stay details.
- Guest portal tokens and QR codes.
- Payment references.
- Staff PIN data.
- Database and backup files.

Do not put these in Git commits, screenshots, public issue trackers, or shared chat groups.

## 12. Monitoring and Health Checks

### Minimum daily checks

- `/health` returns `ok`.
- Server process is running.
- Disk has free space.
- Database is writable.
- Latest backup exists.
- Frontend URLs load.
- API requests are not returning repeated 500 errors.

### Useful Linux commands

```bash
curl -s http://127.0.0.1:8000/health
df -h
free -h
systemctl status starsandpines-web
systemctl status starsandpines-backup.timer
journalctl -u starsandpines-web -n 50 --no-pager
journalctl -u starsandpines-backup -n 50 --no-pager
```

### Alert conditions

Escalate when:

- Health check fails twice.
- Backup has not completed by the next opening check.
- Disk space is below the agreed threshold.
- The same order is duplicated.
- A payment cannot be verified.
- Guest tokens are exposed.
- Database integrity check fails.
- The server restarts unexpectedly.
- Manual fallback was used for more than one critical workflow.

## 13. Incident Log

Use one incident record per issue.

```text
Incident ID: SP-YYYYMMDD-###
Date/time discovered:
Discovered by:
System: Server / Network / Guest Entry / Portal / Family / Cafe / Payment / Database

What happened:

Guest/order/payment impact:

Immediate workaround:

Manual references created:

Who was informed:

Root cause, if known:

Recovery completed at:

Records reconciled by:

Permanent fix required:

Owner and due date:
```

Review incidents weekly. Repeated “operator confusion” is a product usability problem, not a staff failure.

## 14. First 30 Days Action Plan

### Days 1-2: Prepare

- Assign Amrit, Raman, and Mona's actual responsibilities.
- Choose the server and backup device.
- Print fallback forms.
- Configure the private LAN.
- Install the application on the actual operations machine.
- Replace sample property data with reviewed data.
- Verify prices and payment methods.

### Days 3-4: Technical verification

- Run the full automated test suite.
- Complete check-in through QR access.
- Complete guest order through kitchen status.
- Complete inventory movement.
- Complete payment and checkout.
- Run the backup and restore drill.
- Test all workflows from a second device.

### Days 5-7: Shadow operation

- Use the system alongside current processes.
- Record every discrepancy.
- Measure time to check in a guest.
- Measure time to find and complete a kitchen order.
- Measure time to reconcile a checkout.
- Fix only critical workflow blockers.

### Week 2: Limited real usage

- Use the system for selected arrivals and low-risk orders.
- Keep paper fallback active.
- Review all payments twice daily.
- Hold a 15-minute closing review.

### Week 3: Expand

- Move more rooms/orders onto the system.
- Add cafe flow if it passed separate testing.
- Introduce inventory tracking as the normal process.
- Run a second restore drill.

### Week 4: Go/no-go review

Approve full daily dependence only if:

- No unresolved financial discrepancies remain.
- The team can recover from a server/network outage.
- Backups and restores have been proven.
- Guest tokens are handled privately.
- The no-auth boundary is accepted and technically restricted.
- Outstanding incidents have owners and dates.

## 15. Weekly Operating Review

Hold a 30-minute review with the operators.

Discuss:

- What failed this week?
- What was confusing?
- Which manual fallback was used?
- Were any payments unclear?
- Were any orders duplicated or delayed?
- Did stock counts match?
- Did backups complete?
- Did any guest receive the wrong information?
- Which fix would save the most staff time?

Record decisions as tasks with an owner and due date. Do not turn every complaint into an emergency code change during service.

## 16. Change Management

### Safe change window

Make application, schema, nginx, or service changes outside active check-in, kitchen, and checkout periods.

### Before a change

1. Write the purpose of the change.
2. Take a database backup.
3. Confirm the current commit/version.
4. Confirm the rollback procedure.
5. Tell the operators what will change.

### After a change

1. Check `/health`.
2. Open all application URLs.
3. Test one safe read from each app.
4. Test one non-financial write in a test/staging database.
5. Verify the production database is unchanged unless intended.
6. Record the change and result.

### Rollback rule

If the application cannot safely process check-in, orders, payments, or checkout after a change, revert the application code or return to the last verified version and use the manual fallback. Do not debug a risky migration during a guest-facing incident.

## 17. Launch Readiness Checklist

### People

- [ ] Amrit knows check-in and guest support.
- [ ] Raman knows kitchen and inventory.
- [ ] Mona knows approval, reconciliation, and recovery.
- [ ] At least two people can start the server.
- [ ] At least two people can use the manual forms.
- [ ] Everyone knows the server address.

### Product

- [ ] Real rooms and beds loaded.
- [ ] Real menu/prices reviewed.
- [ ] Actual payment methods documented.
- [ ] Guest token handoff procedure approved.
- [ ] Family App no-auth boundary accepted for the private LAN only.

### Technical

- [ ] Server starts after reboot.
- [ ] `/health` works.
- [ ] All app URLs work.
- [ ] Backup works.
- [ ] Restore works.
- [ ] Disk monitoring exists.
- [ ] Logs can be read.
- [ ] Nginx/Uvicorn architecture is documented and tested.
- [ ] Legacy provisioning routes have been corrected or explicitly not used.

### Operational

- [ ] Opening checklist printed.
- [ ] Closing checklist printed.
- [ ] Check-in form printed.
- [ ] Order form printed.
- [ ] Payment form printed.
- [ ] Inventory form printed.
- [ ] Incident log ready.
- [ ] Shift handover routine agreed.
- [ ] First recovery drill completed.

## 18. Immediate Next Actions

Complete these in order:

1. Assign the actual server machine and backup device.
2. Decide who owns technical recovery.
3. Correct the production deployment path so nginx/Uvicorn/current URLs agree.
4. Install the current repository on the server.
5. Load reviewed property, menu, inventory, and contact data.
6. Run the full lifecycle test with fake guest data.
7. Print and test the manual fallback forms.
8. Run a power/network/server failure drill.
9. Run a database restore drill.
10. Start the 3-to-7-day shadow pilot.
11. Review pilot metrics and incidents.
12. Approve or postpone controlled go-live.
13. Schedule authentication and authorization hardening before any wider network exposure.

## 19. Definition of “Working Practically”

Stars & Pines V2 is working practically when:

- A new guest can be checked in in one sitting without developer help.
- The guest can access the correct stay portal.
- An order reaches the right kitchen workflow.
- Staff can identify what is pending, preparing, served, or cancelled.
- Inventory changes are recorded when they happen.
- A bill can be explained line by line.
- Payments are not double-counted.
- Checkout invalidates guest access.
- A server or network failure results in an orderly paper fallback, not lost work.
- The team can restore the database without guessing.
- The end-of-day totals can be reconciled by someone other than the person who entered them.
- The system's limitations are visible and managed instead of being mistaken for completed features.
