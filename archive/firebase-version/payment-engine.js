/**
 * Stars & Pines — Payment Engine
 * Handles Razorpay integration, QR code payments, and pay-later flow.
 */

var PaymentEngine = (function() {
  'use strict';

  var syncEngine = null;
  var utils = null;

  // Razorpay configuration
  var RAZORPAY_CONFIG = {
    keyId: 'REPLACE_WITH_RAZORPAY_KEY_ID',
    currency: 'INR',
    name: 'Stars & Pines',
    description: 'Stay Payment',
    theme: { color: '#1f2f1d' }
  };

  function init(se, u) {
    syncEngine = se;
    utils = u;
  }

  // ─── Payment Record Creation ─────────────────────────────────────

  function createPaymentRecord(bookingId, guestId, amount, method, status) {
    var payment = {
      paymentId: utils.generateId('pay'),
      bookingId: bookingId,
      guestId: guestId,
      amount: amount,
      method: method,          // 'razorpay', 'qr', 'cash', 'pay_later'
      status: status || 'pending', // 'pending', 'confirmed', 'failed', 'refunded'
      razorpayPaymentId: null,
      razorpayOrderId: null,
      qrReference: null,
      notes: '',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      syncStatus: 'pending'
    };
    return payment;
  }

  // ─── Razorpay Payment ────────────────────────────────────────────

  function payWithRazorpay(bookingId, guestId, amount, guestName, phone, onSuccess, onError) {
    if (typeof Razorpay === 'undefined') {
      // Razorpay SDK not loaded — fallback to manual
      if (onError) onError(new Error('Razorpay SDK not loaded'));
      return;
    }

    var options = {
      key: RAZORPAY_CONFIG.keyId,
      amount: amount * 100, // Razorpay expects paise
      currency: RAZORPAY_CONFIG.currency,
      name: RAZORPAY_CONFIG.name,
      description: RAZORPAY_CONFIG.description + ' — ' + bookingId,
      image: '',
      handler: function(response) {
        // Payment successful
        var payment = createPaymentRecord(bookingId, guestId, amount, 'razorpay', 'confirmed');
        payment.razorpayPaymentId = response.razorpay_payment_id;
        payment.razorpayOrderId = response.razorpay_order_id;
        payment.razorpaySignature = response.razorpay_signature;
        payment.updatedAt = Date.now();

        syncEngine.create('payments', payment, 1).then(function() {
          utils.logActivity(syncEngine, 'payment_confirmed', 'guest', payment.paymentId,
            'Razorpay payment of ' + utils.formatCurrency(amount) + ' for ' + bookingId);
          if (onSuccess) onSuccess(payment);
        }).catch(function(err) {
          if (onError) onError(err);
        });
      },
      prefill: {
        name: guestName || '',
        contact: phone || '',
        email: ''
      },
      theme: RAZORPAY_CONFIG.theme,
      modal: {
        ondismiss: function() {
          if (onError) onError(new Error('Payment dismissed'));
        }
      }
    };

    var rzp = new Razorpay(options);
    rzp.open();
  }

  // ─── QR Code Payment ─────────────────────────────────────────────

  function initiateQRPayment(bookingId, guestId, amount, staffName) {
    var payment = createPaymentRecord(bookingId, guestId, amount, 'qr', 'pending');
    payment.qrReference = 'QR-' + Date.now().toString(36).toUpperCase();
    payment.notes = 'Initiated by ' + (staffName || 'staff');

    return syncEngine.create('payments', payment, 1).then(function() {
      utils.logActivity(syncEngine, 'payment_qr_initiated', 'staff', payment.paymentId,
        'QR payment of ' + utils.formatCurrency(amount) + ' for ' + bookingId);
      return payment;
    });
  }

  function confirmQRPayment(paymentId, staffName) {
    return syncEngine.update('payments', paymentId, {
      status: 'confirmed',
      confirmedBy: staffName || 'staff',
      confirmedAt: Date.now(),
      updatedAt: Date.now()
    }, 1).then(function(payment) {
      utils.logActivity(syncEngine, 'payment_confirmed', 'staff', paymentId,
        'QR payment confirmed by ' + (staffName || 'staff'));
      return payment;
    });
  }

  // ─── Pay Later ───────────────────────────────────────────────────

  function createPayLater(bookingId, guestId, amount, staffName) {
    var payment = createPaymentRecord(bookingId, guestId, amount, 'pay_later', 'pending');
    payment.notes = 'Pay later — recorded by ' + (staffName || 'staff');

    return syncEngine.create('payments', payment, 2).then(function() {
      // Create notification for dashboard
      var notification = {
        notificationId: utils.generateId('notif'),
        type: 'outstanding_payment',
        guestId: guestId,
        bookingId: bookingId,
        message: 'Outstanding payment: ' + utils.formatCurrency(amount) + ' for ' + bookingId,
        amount: amount,
        priority: 'high',
        read: false,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        syncStatus: 'pending'
      };
      return syncEngine.create('notifications', notification, 3).then(function() {
        utils.logActivity(syncEngine, 'payment_pay_later', 'staff', payment.paymentId,
          'Pay later: ' + utils.formatCurrency(amount) + ' for ' + bookingId);
        return payment;
      });
    });
  }

  // ─── Cash Payment ────────────────────────────────────────────────

  function recordCashPayment(bookingId, guestId, amount, staffName, notes) {
    var payment = createPaymentRecord(bookingId, guestId, amount, 'cash', 'confirmed');
    payment.confirmedBy = staffName || 'staff';
    payment.confirmedAt = Date.now();
    payment.notes = notes || 'Cash payment';

    return syncEngine.create('payments', payment, 1).then(function() {
      utils.logActivity(syncEngine, 'payment_confirmed', 'staff', payment.paymentId,
        'Cash payment of ' + utils.formatCurrency(amount) + ' for ' + bookingId);
      return payment;
    });
  }

  // ─── Payment Queries ─────────────────────────────────────────────

  function getPaymentsForBooking(bookingId) {
    return syncEngine.getByIndex('payments', 'bookingId', bookingId).then(function(payments) {
      return payments.sort(function(a, b) { return b.createdAt - a.createdAt; });
    });
  }

  function getPaymentsForGuest(guestId) {
    return syncEngine.getByIndex('payments', 'guestId', guestId).then(function(payments) {
      return payments.sort(function(a, b) { return b.createdAt - a.createdAt; });
    });
  }

  function getTotalPaid(bookingId) {
    return getPaymentsForBooking(bookingId).then(function(payments) {
      var total = 0;
      payments.forEach(function(p) {
        if (p.status === 'confirmed') total += p.amount;
      });
      return total;
    });
  }

  function getOutstandingPayments() {
    return syncEngine.getAll('payments').then(function(payments) {
      return payments.filter(function(p) {
        return p.status === 'pending' && p.method !== 'pay_later';
      }).sort(function(a, b) { return b.createdAt - a.createdAt; });
    });
  }

  function getPayLaterRecords() {
    return syncEngine.getAll('payments').then(function(payments) {
      return payments.filter(function(p) {
        return p.method === 'pay_later' && p.status === 'pending';
      }).sort(function(a, b) { return b.createdAt - a.createdAt; });
    });
  }

  // ─── Financial Summary ───────────────────────────────────────────

  function getFinancialSummary() {
    return syncEngine.getAll('payments').then(function(payments) {
      var todayStart = utils.todayStart();
      var monthStart = utils.monthStart();

      var summary = {
        revenueToday: 0,
        revenueThisMonth: 0,
        totalOutstanding: 0,
        totalDeposits: 0,
        totalPaid: 0,
        pendingPayments: 0,
        payLaterCount: 0
      };

      payments.forEach(function(p) {
        if (p.status === 'confirmed') {
          summary.totalPaid += p.amount;
          if (p.createdAt >= todayStart) summary.revenueToday += p.amount;
          if (p.createdAt >= monthStart) summary.revenueThisMonth += p.amount;
          if (p.method === 'razorpay' || p.method === 'qr' || p.method === 'cash') {
            if (p.notes && p.notes.toLowerCase().indexOf('deposit') >= 0) {
              summary.totalDeposits += p.amount;
            }
          }
        } else if (p.status === 'pending') {
          summary.totalOutstanding += p.amount;
          summary.pendingPayments++;
          if (p.method === 'pay_later') summary.payLaterCount++;
        }
      });

      return summary;
    });
  }

  // ─── Export ──────────────────────────────────────────────────────

  return {
    init: init,
    createPaymentRecord: createPaymentRecord,
    payWithRazorpay: payWithRazorpay,
    initiateQRPayment: initiateQRPayment,
    confirmQRPayment: confirmQRPayment,
    createPayLater: createPayLater,
    recordCashPayment: recordCashPayment,
    getPaymentsForBooking: getPaymentsForBooking,
    getPaymentsForGuest: getPaymentsForGuest,
    getTotalPaid: getTotalPaid,
    getOutstandingPayments: getOutstandingPayments,
    getPayLaterRecords: getPayLaterRecords,
    getFinancialSummary: getFinancialSummary
  };
})();
