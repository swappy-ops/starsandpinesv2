/**
 * Stars & Pines — Shared Firebase Configuration
 * Single source of truth for all apps.
 *
 * Usage: <script src="js/firebase-config.js"></script>
 * Exposes: SP_CONFIG (object), SP_DB (Firebase database ref)
 */

var SP_CONFIG = {
  whatsappNumber: '917982523582',
  firebaseConfig: {
    apiKey: 'AIzaSyAJtVjg6zv1KK2puu57NICrW8mU7OTybUA',
    authDomain: 'stars-and-pines-ridge.firebaseapp.com',
    databaseURL: 'https://stars-and-pines-ridge-default-rtdb.asia-southeast1.firebasedatabase.app',
    projectId: 'stars-and-pines-ridge',
    storageBucket: 'stars-and-pines-ridge.firebasestorage.app',
    messagingSenderId: '8285256236',
    appId: '1:8285256236:web:e03af2dff72e80eed26f89'
  }
};

// Initialize Firebase if not already initialized
(function() {
  if (typeof firebase === 'undefined') return;
  if (!firebase.apps || firebase.apps.length === 0) {
    firebase.initializeApp(SP_CONFIG.firebaseConfig);
  }
  window.SP_DB = firebase.database();
})();

// Activity feed helper — every major event writes here
function spLogActivity(type, actor, target, details) {
  if (!window.SP_DB) return;
  window.SP_DB.ref('activity_feed').push({
    type: type,
    actor: actor || 'system',
    target: target || '',
    details: details || '',
    timestamp: Date.now()
  });
}

// Notification helper — writes to /notifications
function spNotify(type, message, priority, target) {
  if (!window.SP_DB) return;
  window.SP_DB.ref('notifications').push({
    type: type,
    message: message,
    priority: priority || 'normal',
    target: target || 'all',
    read: false,
    createdAt: Date.now()
  });
}
