/**
 * Stars & Pines V2 — Shared API Client
 * Single fetch wrapper used by all three apps.
 *
 * API_BASE resolution order:
 *   1. window.__API_URL__ (set by server template or inline script)
 *   2. VITE_API_URL (for future Vite builds)
 *   3. http://localhost:8000 (local dev default)
 */

const API_BASE =
  (typeof window !== 'undefined' && window.__API_URL__) ||
  "http://localhost:8000";

const API = {
  BASE: API_BASE,

  async request(method, path, body = null) {
    const opts = {
      method,
      headers: { "Content-Type": "application/json" },
    };
    if (body) opts.body = JSON.stringify(body);

    const url = `${this.BASE}${path}`;
    const res = await fetch(url, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `${res.status} ${res.statusText}`);
    }
    return res.json();
  },

  get(path) { return this.request("GET", path); },
  post(path, body) { return this.request("POST", path, body); },

  // ─── Staff Auth ───
  staffLogin(staffId, pin) {
    return this.post("/api/staff/login", { staff_id: staffId, pin });
  },
  listStaff() { return this.get("/api/staff/list"); },

  // ─── Guest Entry ───
  checkin(data) {
    return this.post("/api/checkin", data);
  },
  checkout(stayId, staffName) {
    return this.post("/api/checkout", { stay_id: stayId, staff_name: staffName });
  },
  searchGuests(q) { return this.get(`/api/guests/search?q=${encodeURIComponent(q)}`); },
  getGuest(id) { return this.get(`/api/guests/${id}`); },

  // ─── Rooms & Beds ───
  getRooms() { return this.get("/api/rooms"); },
  getAvailableRooms() { return this.get("/api/rooms/available"); },
  getRoomBeds(roomId) { return this.get(`/api/rooms/${roomId}/beds`); },
  getAvailableBeds() { return this.get("/api/beds/available"); },

  // ─── Guest Portal ───
  validateToken(token) { return this.get(`/api/portal/validate?token=${encodeURIComponent(token)}`); },
  getPortalBill(token) { return this.get(`/api/portal/${encodeURIComponent(token)}/bill`); },
  getPortalOrders(token) { return this.get(`/api/portal/${encodeURIComponent(token)}/orders`); },

  // ─── Menu ───
  getMenu() { return this.get("/api/menu"); },
  getAvailableMenu() { return this.get("/api/menu/available"); },

  // ─── Orders ───
  createOrder(data) { return this.post("/api/orders", data); },
  updateOrderStatus(orderId, status, staffName) {
    return this.post(`/api/orders/${orderId}/status`, { status, staff_name: staffName });
  },

  // ─── Kitchen ───
  getKitchenQueue() { return this.get("/api/kitchen/queue"); },
  getKitchenStats() { return this.get("/api/kitchen/stats"); },

  // ─── Dashboard ───
  getDashboard() { return this.get("/api/dashboard"); },
  getOccupancy() { return this.get("/api/dashboard/occupancy"); },
  getArrivals() { return this.get("/api/dashboard/arrivals"); },
  getDepartures() { return this.get("/api/dashboard/departures"); },
  getRevenue() { return this.get("/api/dashboard/revenue"); },

  // ─── Billing ───
  getBill(stayId) { return this.get(`/api/bill/${stayId}`); },
  recordPayment(data) { return this.post("/api/payment", data); },

  // ─── Cleaning ───
  createCleaning(data) { return this.post("/api/cleaning", data); },
  getPendingCleaning() { return this.get("/api/cleaning/pending"); },
  getCleaningByStay(stayId) { return this.get(`/api/cleaning/stay/${stayId}`); },
  updateCleaningStatus(id, status) {
    return this.post(`/api/cleaning/${id}/status`, { status });
  },

  // ─── Inventory ───
  getInventory() { return this.get("/api/inventory"); },
  restockItem(data) { return this.post("/api/inventory/restock", data); },
  consumeItem(data) { return this.post("/api/inventory/consume", data); },

  // ─── Grievances ───
  createGrievance(data) { return this.post("/api/grievances", data); },
  getGrievances(stayId) { return this.get(`/api/grievances?stay_id=${encodeURIComponent(stayId)}`); },
  updateGrievanceStatus(id, status, staffName) {
    return this.post(`/api/grievances/${id}/status?status=${encodeURIComponent(status)}&staff_name=${encodeURIComponent(staffName || '')}`, {});
  },

  // ─── Notifications ───
  getNotifications(stayId) { return this.get(`/api/notifications?stay_id=${encodeURIComponent(stayId)}`); },
  markNotificationRead(id) { return this.post(`/api/notifications/${id}/read`, {}); },
  markAllNotificationsRead(stayId) { return this.post(`/api/notifications/read-all?stay_id=${encodeURIComponent(stayId)}`, {}); },

  // ─── Service Requests (Experiences + Concierge) ───
  createServiceRequest(data) { return this.post("/api/service-requests", data); },
  getServiceRequests(stayId, type) {
    const url = type
      ? `/api/service-requests?stay_id=${encodeURIComponent(stayId)}&request_type=${encodeURIComponent(type)}`
      : `/api/service-requests?stay_id=${encodeURIComponent(stayId)}`;
    return this.get(url);
  },
  updateServiceRequestStatus(id, status) {
    return this.post(`/api/service-requests/${id}/status?status=${encodeURIComponent(status)}`, {});
  },

  // ─── Portal Payment ───
  portalPayment(token, data) { return this.post(`/api/portal/${encodeURIComponent(token)}/payment`, data); },
};
