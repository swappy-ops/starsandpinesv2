/**
 * Stars & Pines — Shared Utilities
 * Common functions used across all apps.
 */

var SP_UTILS = (function() {
  'use strict';

  // ─── ID Generation ───────────────────────────────────────────────
  function generateId(prefix) {
    return (prefix || 'sp') + '_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
  }

  function generateBookingId() {
    var now = new Date();
    var year = now.getFullYear();
    var seq = String(Math.floor(Math.random() * 9000) + 1000);
    return 'SP-' + year + '-' + seq;
  }

  function generateGuestId() {
    return 'SP-G-' + Math.random().toString(36).substr(2, 6).toUpperCase();
  }

  // 6-char alphanumeric access code (no ambiguous chars)
  function generateAccessCode() {
    var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    var code = '';
    for (var i = 0; i < 6; i++) {
      code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
  }

  // ─── Date/Time ───────────────────────────────────────────────────
  function now() {
    return Date.now();
  }

  function formatDate(ts) {
    if (!ts) return '';
    var d = new Date(ts);
    return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
  }

  function formatTime(ts) {
    if (!ts) return '';
    var d = new Date(ts);
    return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  }

  function formatDateTime(ts) {
    return formatDate(ts) + ' ' + formatTime(ts);
  }

  function daysBetween(ts1, ts2) {
    var msPerDay = 86400000;
    return Math.ceil((ts2 - ts1) / msPerDay);
  }

  function todayStart() {
    var d = new Date();
    d.setHours(0, 0, 0, 0);
    return d.getTime();
  }

  function todayEnd() {
    var d = new Date();
    d.setHours(23, 59, 59, 999);
    return d.getTime();
  }

  function monthStart() {
    var d = new Date();
    d.setDate(1);
    d.setHours(0, 0, 0, 0);
    return d.getTime();
  }

  // ─── Currency ────────────────────────────────────────────────────
  function formatCurrency(amount) {
    if (amount == null || isNaN(amount)) return '₹0';
    return '₹' + Number(amount).toLocaleString('en-IN');
  }

  // ─── Phone ───────────────────────────────────────────────────────
  function normalizePhone(phone) {
    if (!phone) return '';
    return phone.replace(/[\s\-\(\)]/g, '');
  }

  function lastFourDigits(phone) {
    var cleaned = normalizePhone(phone);
    return cleaned.slice(-4);
  }

  function formatWhatsAppUrl(phone, message) {
    var num = normalizePhone(phone);
    if (!num.startsWith('91')) num = '91' + num;
    return 'https://wa.me/' + num + '?text=' + encodeURIComponent(message);
  }

  // ─── Status Colors ───────────────────────────────────────────────
  var STATUS_COLORS = {
    paid: '#4a8a62',
    pending: '#d4b880',
    overdue: '#c45a5a',
    checked_in: '#4a8a62',
    checked_out: '#888',
    awaiting_checkout: '#d4885a',
    confirmed: '#4a8a62',
    cancelled: '#c45a5a',
    open: '#c45a5a',
    acknowledged: '#d4b880',
    resolved: '#4a8a62',
    escalated: '#c45a5a',
    preparing: '#d4b880',
    ready: '#4a8a62',
    delivered: '#4a8a62',
    syncing: '#d4b880',
    synced: '#4a8a62',
    failed: '#c45a5a'
  };

  function statusColor(status) {
    return STATUS_COLORS[status] || '#888';
  }

  // ─── Connectivity ────────────────────────────────────────────────
  function isOnline() {
    return navigator.onLine;
  }

  function onConnectivityChange(callback) {
    window.addEventListener('online', function() { callback(true); });
    window.addEventListener('offline', function() { callback(false); });
  }

  // ─── Toast Notifications ─────────────────────────────────────────
  function showToast(message, duration, color) {
    var existing = document.querySelector('.sp-toast');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.className = 'sp-toast';
    toast.textContent = message;
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);' +
      'background:' + (color || '#1f2f1d') + ';color:#f6f1ea;padding:12px 24px;border-radius:8px;' +
      'font-size:14px;z-index:10000;box-shadow:0 4px 12px rgba(0,0,0,0.3);' +
      'animation:spToastIn 0.3s ease;max-width:90vw;text-align:center;';

    document.body.appendChild(toast);
    setTimeout(function() {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s';
      setTimeout(function() { toast.remove(); }, 300);
    }, duration || 2500);
  }

  // ─── Activity Logging ────────────────────────────────────────────
  function logActivity(localDb, type, actor, target, details) {
    var entry = {
      activityId: generateId('act'),
      type: type,
      actor: actor || 'system',
      target: target || '',
      details: details || '',
      timestamp: now(),
      createdAt: now(),
      updatedAt: now(),
      syncStatus: 'pending'
    };
    if (localDb) {
      localDb.put('activity_feed', entry).catch(function() {});
    }
    return entry;
  }

  // ─── Sync Status Badge ───────────────────────────────────────────
  function createSyncBadge(container) {
    var badge = document.createElement('div');
    badge.id = 'sp-sync-badge';
    badge.style.cssText = 'position:fixed;top:12px;right:12px;z-index:9999;' +
      'display:flex;align-items:center;gap:6px;padding:6px 12px;border-radius:20px;' +
      'background:rgba(19,26,18,0.9);font-size:12px;color:#f6f1ea;' +
      'backdrop-filter:blur(8px);border:1px solid rgba(212,184,128,0.2);';

    var dot = document.createElement('span');
    dot.id = 'sp-sync-dot';
    dot.style.cssText = 'width:8px;height:8px;border-radius:50%;background:#4a8a62;';

    var label = document.createElement('span');
    label.id = 'sp-sync-label';
    label.textContent = 'Synced';

    badge.appendChild(dot);
    badge.appendChild(label);

    if (container) {
      container.appendChild(badge);
    } else {
      document.body.appendChild(badge);
    }

    return badge;
  }

  function updateSyncBadge(status) {
    var dot = document.getElementById('sp-sync-dot');
    var label = document.getElementById('sp-sync-label');
    if (!dot || !label) return;

    var colors = { online: '#4a8a62', syncing: '#d4b880', offline: '#c45a5a', error: '#c45a5a' };
    var labels = { online: 'Synced', syncing: 'Syncing...', offline: 'Offline', error: 'Sync Error' };

    dot.style.background = colors[status] || colors.online;
    label.textContent = labels[status] || labels.online;
  }

  // ─── Modal ───────────────────────────────────────────────────────
  function showModal(title, contentHtml, onConfirm, onCancel) {
    var existing = document.querySelector('.sp-modal-overlay');
    if (existing) existing.remove();

    var overlay = document.createElement('div');
    overlay.className = 'sp-modal-overlay';
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);' +
      'z-index:10000;display:flex;align-items:flex-end;justify-content:center;' +
      'animation:spFadeIn 0.2s ease;';

    var modal = document.createElement('div');
    modal.className = 'sp-modal';
    modal.style.cssText = 'background:#1f2f1d;border-radius:16px 16px 0 0;width:100%;max-width:480px;' +
      'max-height:85vh;overflow-y:auto;padding:24px;animation:spSlideUp 0.3s ease;';

    var header = document.createElement('div');
    header.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;';

    var h2 = document.createElement('h2');
    h2.textContent = title;
    h2.style.cssText = 'font-family:"Playfair Display",serif;font-size:20px;color:#f6f1ea;margin:0;';

    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = 'background:none;border:none;color:#d4b880;font-size:28px;cursor:pointer;padding:0 8px;';
    closeBtn.onclick = function() { overlay.remove(); if (onCancel) onCancel(); };

    header.appendChild(h2);
    header.appendChild(closeBtn);
    modal.appendChild(header);

    var content = document.createElement('div');
    content.innerHTML = contentHtml;
    modal.appendChild(content);

    if (onConfirm) {
      var actions = document.createElement('div');
      actions.style.cssText = 'display:flex;gap:12px;margin-top:20px;';

      var cancelBtn = document.createElement('button');
      cancelBtn.textContent = 'Cancel';
      cancelBtn.style.cssText = 'flex:1;padding:12px;border-radius:8px;border:1px solid #d4b880;' +
        'background:transparent;color:#d4b880;font-size:14px;cursor:pointer;';
      cancelBtn.onclick = function() { overlay.remove(); if (onCancel) onCancel(); };

      var confirmBtn = document.createElement('button');
      confirmBtn.textContent = 'Confirm';
      confirmBtn.style.cssText = 'flex:1;padding:12px;border-radius:8px;border:none;' +
        'background:#d4b880;color:#131a12;font-size:14px;font-weight:600;cursor:pointer;';
      confirmBtn.onclick = function() { onConfirm(); overlay.remove(); };

      actions.appendChild(cancelBtn);
      actions.appendChild(confirmBtn);
      modal.appendChild(actions);
    }

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) { overlay.remove(); if (onCancel) onCancel(); }
    });

    return overlay;
  }

  // ─── Form Helpers ────────────────────────────────────────────────
  function getFormValue(form, id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  function setFormValue(id, value) {
    var el = document.getElementById(id);
    if (el) el.value = value;
  }

  // ─── QR Code Generator (uses qrcode.js CDN) ──────────────────────
  function generateQR(canvas, text, size) {
    if (typeof QRCode === 'undefined') {
      console.error('QRCode library not loaded');
      return;
    }
    new QRCode(canvas, {
      text: text,
      width: size || 200,
      height: size || 200,
      colorDark: '#131a12',
      colorLight: '#f6f1ea',
      correctLevel: QRCode.CorrectLevel.M
    });
  }

  // ─── Export ──────────────────────────────────────────────────────
  return {
    generateId: generateId,
    generateBookingId: generateBookingId,
    generateGuestId: generateGuestId,
    generateAccessCode: generateAccessCode,
    now: now,
    formatDate: formatDate,
    formatTime: formatTime,
    formatDateTime: formatDateTime,
    daysBetween: daysBetween,
    todayStart: todayStart,
    todayEnd: todayEnd,
    monthStart: monthStart,
    formatCurrency: formatCurrency,
    normalizePhone: normalizePhone,
    lastFourDigits: lastFourDigits,
    formatWhatsAppUrl: formatWhatsAppUrl,
    statusColor: statusColor,
    isOnline: isOnline,
    onConnectivityChange: onConnectivityChange,
    showToast: showToast,
    logActivity: logActivity,
    createSyncBadge: createSyncBadge,
    updateSyncBadge: updateSyncBadge,
    showModal: showModal,
    getFormValue: getFormValue,
    setFormValue: setFormValue,
    generateQR: generateQR
  };
})();
