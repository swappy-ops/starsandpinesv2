/**
 * Stars & Pines — Local Database (IndexedDB)
 * Local-first operational store. All writes go here first.
 *
 * Stores: guests, bookings, rooms, payments, menu_orders,
 *         service_requests, notifications, grievances,
 *         activity_feed, checkout_records, sync_queue
 */

var LocalDB = (function() {
  'use strict';

  var DB_NAME = 'stars-pines-db';
  var DB_VERSION = 1;
  var db = null;

  var STORES = [
    { name: 'guests', keyPath: 'guestId', indexes: [
      { name: 'accessCode', keyPath: 'accessCode' },
      { name: 'phone', keyPath: 'phone' },
      { name: 'syncStatus', keyPath: 'syncStatus' }
    ]},
    { name: 'bookings', keyPath: 'bookingId', indexes: [
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'room', keyPath: 'room' },
      { name: 'status', keyPath: 'status' },
      { name: 'syncStatus', keyPath: 'syncStatus' },
      { name: 'checkInDate', keyPath: 'checkInDate' },
      { name: 'checkOutDate', keyPath: 'checkOutDate' }
    ]},
    { name: 'rooms', keyPath: 'roomId', indexes: [
      { name: 'type', keyPath: 'type' },
      { name: 'status', keyPath: 'status' }
    ]},
    { name: 'payments', keyPath: 'paymentId', indexes: [
      { name: 'bookingId', keyPath: 'bookingId' },
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'status', keyPath: 'status' },
      { name: 'syncStatus', keyPath: 'syncStatus' }
    ]},
    { name: 'menu_orders', keyPath: 'orderId', indexes: [
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'room', keyPath: 'room' },
      { name: 'status', keyPath: 'status' },
      { name: 'syncStatus', keyPath: 'syncStatus' },
      { name: 'createdAt', keyPath: 'createdAt' }
    ]},
    { name: 'service_requests', keyPath: 'requestId', indexes: [
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'type', keyPath: 'type' },
      { name: 'status', keyPath: 'status' },
      { name: 'syncStatus', keyPath: 'syncStatus' }
    ]},
    { name: 'notifications', keyPath: 'notificationId', indexes: [
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'read', keyPath: 'read' },
      { name: 'syncStatus', keyPath: 'syncStatus' },
      { name: 'createdAt', keyPath: 'createdAt' }
    ]},
    { name: 'grievances', keyPath: 'grievanceId', indexes: [
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'status', keyPath: 'status' },
      { name: 'syncStatus', keyPath: 'syncStatus' },
      { name: 'createdAt', keyPath: 'createdAt' }
    ]},
    { name: 'activity_feed', keyPath: 'activityId', indexes: [
      { name: 'type', keyPath: 'type' },
      { name: 'timestamp', keyPath: 'timestamp' }
    ]},
    { name: 'checkout_records', keyPath: 'checkoutId', indexes: [
      { name: 'guestId', keyPath: 'guestId' },
      { name: 'status', keyPath: 'status' },
      { name: 'syncStatus', keyPath: 'syncStatus' }
    ]},
    { name: 'sync_queue', keyPath: 'queueId', indexes: [
      { name: 'status', keyPath: 'status' },
      { name: 'priority', keyPath: 'priority' },
      { name: 'createdAt', keyPath: 'createdAt' }
    ]}
  ];

  function open() {
    return new Promise(function(resolve, reject) {
      if (db) { resolve(db); return; }

      var request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = function(e) {
        var database = e.target.result;
        STORES.forEach(function(store) {
          if (!database.objectStoreNames.contains(store.name)) {
            var os = database.createObjectStore(store.name, { keyPath: store.keyPath });
            store.indexes.forEach(function(idx) {
              os.createIndex(idx.name, idx.keyPath, { unique: false });
            });
          }
        });
      };

      request.onsuccess = function(e) {
        db = e.target.result;
        resolve(db);
      };

      request.onerror = function(e) {
        reject(e.target.error);
      };
    });
  }

  function tx(storeName, mode) {
    return open().then(function(database) {
      return database.transaction(storeName, mode);
    });
  }

  function store(storeName, mode) {
    return tx(storeName, mode).then(function(transaction) {
      return transaction.objectStore(storeName);
    });
  }

  // ─── CRUD Operations ─────────────────────────────────────────────

  function put(storeName, record) {
    return store(storeName, 'readwrite').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.put(record);
        req.onsuccess = function() { resolve(req.result); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function add(storeName, record) {
    return store(storeName, 'readwrite').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.add(record);
        req.onsuccess = function() { resolve(req.result); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function get(storeName, key) {
    return store(storeName, 'readonly').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.get(key);
        req.onsuccess = function() { resolve(req.result); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function getAll(storeName) {
    return store(storeName, 'readonly').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.getAll();
        req.onsuccess = function() { resolve(req.result || []); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function getByIndex(storeName, indexName, value) {
    return tx(storeName, 'readonly').then(function(transaction) {
      var s = transaction.objectStore(storeName);
      var index = s.index(indexName);
      return new Promise(function(resolve, reject) {
        var req = index.getAll(value);
        req.onsuccess = function() { resolve(req.result || []); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function deleteRecord(storeName, key) {
    return store(storeName, 'readwrite').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.delete(key);
        req.onsuccess = function() { resolve(); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function clear(storeName) {
    return store(storeName, 'readwrite').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.clear();
        req.onsuccess = function() { resolve(); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  // ─── Query Helpers ───────────────────────────────────────────────

  function query(storeName, indexName, range) {
    return tx(storeName, 'readonly').then(function(transaction) {
      var s = transaction.objectStore(storeName);
      var index = s.index(indexName);
      return new Promise(function(resolve, reject) {
        var req = index.getAll(range);
        req.onsuccess = function() { resolve(req.result || []); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  function count(storeName) {
    return store(storeName, 'readonly').then(function(s) {
      return new Promise(function(resolve, reject) {
        var req = s.count();
        req.onsuccess = function() { resolve(req.result); };
        req.onerror = function() { reject(req.error); };
      });
    });
  }

  // ─── Bulk Operations ─────────────────────────────────────────────

  function putBatch(storeName, records) {
    return tx(storeName, 'readwrite').then(function(transaction) {
      var s = transaction.objectStore(storeName);
      return new Promise(function(resolve, reject) {
        var errors = [];
        records.forEach(function(record) {
          var req = s.put(record);
          req.onerror = function() { errors.push(req.error); };
        });
        transaction.oncomplete = function() {
          if (errors.length) reject(errors);
          else resolve();
        };
        transaction.onerror = function() { reject(transaction.error); };
      });
    });
  }

  // ─── Sync Queue Helpers ──────────────────────────────────────────

  function enqueueSync(operation, data, priority) {
    var item = {
      queueId: 'sq_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
      operation: operation,    // 'create', 'update', 'delete'
      storeName: data._storeName || operation.split(':')[0],
      data: data,
      priority: priority || 3, // 1=highest (payments), 2=high (bookings), 3=normal, 4=low
      status: 'pending',
      attempts: 0,
      maxAttempts: 10,
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    return add('sync_queue', item);
  }

  function getPendingSync() {
    return query('sync_queue', 'status', 'pending').then(function(items) {
      return items.sort(function(a, b) {
        if (a.priority !== b.priority) return a.priority - b.priority;
        return a.createdAt - b.createdAt;
      });
    });
  }

  function markSyncComplete(queueId) {
    return get('sync_queue', queueId).then(function(item) {
      if (!item) return;
      item.status = 'completed';
      item.updatedAt = Date.now();
      return put('sync_queue', item);
    });
  }

  function markSyncFailed(queueId, error) {
    return get('sync_queue', queueId).then(function(item) {
      if (!item) return;
      item.status = 'failed';
      item.error = error;
      item.attempts = (item.attempts || 0) + 1;
      item.updatedAt = Date.now();
      if (item.attempts >= item.maxAttempts) {
        item.status = 'abandoned';
      }
      return put('sync_queue', item);
    });
  }

  function markSyncInProgress(queueId) {
    return get('sync_queue', queueId).then(function(item) {
      if (!item) return;
      item.status = 'syncing';
      item.attempts = (item.attempts || 0) + 1;
      item.updatedAt = Date.now();
      return put('sync_queue', item);
    });
  }

  function getSyncStats() {
    return getAll('sync_queue').then(function(items) {
      var stats = { pending: 0, syncing: 0, completed: 0, failed: 0, abandoned: 0, total: items.length };
      items.forEach(function(item) {
        if (stats[item.status] !== undefined) stats[item.status]++;
      });
      return stats;
    });
  }

  function clearCompletedSync() {
    return getAll('sync_queue').then(function(items) {
      var toDelete = items.filter(function(i) { return i.status === 'completed' || i.status === 'abandoned'; });
      var promises = toDelete.map(function(i) { return deleteRecord('sync_queue', i.queueId); });
      return Promise.all(promises);
    });
  }

  // ─── Initialize Default Rooms ────────────────────────────────────

  function seedRooms() {
    return count('rooms').then(function(c) {
      if (c > 0) return; // Already seeded

      var rooms = [
        { roomId: 'dorm-a', name: 'Dorm A', type: 'dorm', beds: 10, occupied: 0, status: 'available', cleaningStatus: 'clean', createdAt: Date.now(), updatedAt: Date.now() },
        { roomId: 'dorm-b', name: 'Dorm B', type: 'dorm', beds: 10, occupied: 0, status: 'available', cleaningStatus: 'clean', createdAt: Date.now(), updatedAt: Date.now() },
        { roomId: 'dorm-c', name: 'Dorm C', type: 'dorm', beds: 6, occupied: 0, status: 'available', cleaningStatus: 'clean', createdAt: Date.now(), updatedAt: Date.now() },
        { roomId: 'mountain-double', name: 'Mountain Double', type: 'private', beds: 1, occupied: 0, status: 'available', cleaningStatus: 'clean', pricePerNight: 4200, createdAt: Date.now(), updatedAt: Date.now() },
        { roomId: 'deluxe-twin', name: 'Deluxe Twin', type: 'private', beds: 1, occupied: 0, status: 'available', cleaningStatus: 'clean', pricePerNight: 5800, createdAt: Date.now(), updatedAt: Date.now() }
      ];
      return putBatch('rooms', rooms);
    });
  }

  // ─── Export ──────────────────────────────────────────────────────

  return {
    open: open,
    put: put,
    add: add,
    get: get,
    getAll: getAll,
    getByIndex: getByIndex,
    delete: deleteRecord,
    clear: clear,
    query: query,
    count: count,
    putBatch: putBatch,
    enqueueSync: enqueueSync,
    getPendingSync: getPendingSync,
    markSyncComplete: markSyncComplete,
    markSyncFailed: markSyncFailed,
    markSyncInProgress: markSyncInProgress,
    getSyncStats: getSyncStats,
    clearCompletedSync: clearCompletedSync,
    seedRooms: seedRooms
  };
})();
