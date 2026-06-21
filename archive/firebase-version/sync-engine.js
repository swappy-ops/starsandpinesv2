/**
 * Stars & Pines — Sync Engine
 * Local-first synchronization between IndexedDB and Firebase.
 *
 * Flow: Write → IndexedDB (immediate) → Queue → Firebase (async)
 * Retry: Exponential backoff, max 10 attempts
 * Priority: Payments > Bookings > Orders > Notifications
 */

var SyncEngine = (function() {
  'use strict';

  var db = null;
  var firebaseDb = null;
  var isSyncing = false;
  var syncInterval = null;
  var heartbeatInterval = null;
  var online = navigator.onLine;
  var listeners = [];
  var onStatusChange = null;

  // Firebase path mapping: local store → Firebase path
  var PATH_MAP = {
    guests: 'guests',
    bookings: 'bookings',
    payments: 'payments',
    menu_orders: 'orders',
    service_requests: 'service_requests',
    notifications: 'notifications',
    grievances: 'grievances',
    activity_feed: 'activity_feed',
    checkout_records: 'checkout_records'
  };

  // Firebase key mapping: local key → Firebase key
  var KEY_MAP = {
    guests: 'guestId',
    bookings: 'bookingId',
    payments: 'paymentId',
    menu_orders: 'id',
    service_requests: 'requestId',
    notifications: 'notificationId',
    grievances: 'grievanceId',
    activity_feed: 'activityId',
    checkout_records: 'checkoutId'
  };

  function init(localDb, firebaseDatabase) {
    db = localDb;
    firebaseDb = firebaseDatabase;

    // Listen for connectivity changes
    window.addEventListener('online', function() {
      online = true;
      if (onStatusChange) onStatusChange('online');
      processQueue();
    });

    window.addEventListener('offline', function() {
      online = false;
      if (onStatusChange) onStatusChange('offline');
    });

    // Start periodic sync
    syncInterval = setInterval(function() {
      if (online && !isSyncing) processQueue();
    }, 15000); // Every 15 seconds

    // Heartbeat check
    heartbeatInterval = setInterval(function() {
      var wasOnline = online;
      online = navigator.onLine;
      if (online && !wasOnline && onStatusChange) {
        onStatusChange('online');
        processQueue();
      } else if (!online && wasOnline && onStatusChange) {
        onStatusChange('offline');
      }
    }, 5000);

    // Seed default rooms
    db.seedRooms().catch(function() {});

    return db.open();
  }

  function onStatusChangeCallback(callback) {
    onStatusChange = callback;
  }

  // ─── Write Operations (Local-First) ──────────────────────────────

  function create(storeName, record, priority) {
    record.createdAt = record.createdAt || Date.now();
    record.updatedAt = Date.now();
    record.syncStatus = 'pending';

    return db.put(storeName, record).then(function() {
      // Enqueue for Firebase sync
      return db.enqueueSync('create', record, priority || 3);
    }).then(function() {
      // Try immediate sync if online
      if (online) processQueue();
      return record;
    });
  }

  function update(storeName, key, updates, priority) {
    return db.get(storeName, key).then(function(record) {
      if (!record) throw new Error('Record not found: ' + key);
      for (var k in updates) {
        if (updates.hasOwnProperty(k)) record[k] = updates[k];
      }
      record.updatedAt = Date.now();
      record.syncStatus = 'pending';
      return db.put(storeName, record).then(function() {
        return db.enqueueSync('update', record, priority || 3);
      }).then(function() {
        if (online) processQueue();
        return record;
      });
    });
  }

  function remove(storeName, key, priority) {
    return db.get(storeName, key).then(function(record) {
      if (!record) return;
      record.syncStatus = 'pending';
      return db.enqueueSync('delete', { _storeName: storeName, _key: key }, priority || 3)
        .then(function() {
          return db.delete(storeName, key);
        }).then(function() {
          if (online) processQueue();
        });
    });
  }

  // ─── Read Operations (Local-First) ───────────────────────────────

  function get(storeName, key) {
    return db.get(storeName, key);
  }

  function getAll(storeName) {
    return db.getAll(storeName);
  }

  function getByIndex(storeName, indexName, value) {
    return db.getByIndex(storeName, indexName, value);
  }

  function query(storeName, indexName, range) {
    return db.query(storeName, indexName, range);
  }

  // ─── Sync Queue Processing ───────────────────────────────────────

  function processQueue() {
    if (isSyncing || !online) return Promise.resolve();
    isSyncing = true;
    if (onStatusChange) onStatusChange('syncing');

    return db.getPendingSync().then(function(items) {
      if (items.length === 0) {
        isSyncing = false;
        if (onStatusChange) onStatusChange('online');
        return;
      }

      // Process items sequentially to avoid race conditions
      return processItems(items, 0);
    }).catch(function(err) {
      console.error('Sync queue error:', err);
      isSyncing = false;
      if (onStatusChange) onStatusChange('error');
    });
  }

  function processItems(items, index) {
    if (index >= items.length) {
      isSyncing = false;
      if (onStatusChange) onStatusChange('online');
      // Clean up completed items
      db.clearCompletedSync().catch(function() {});
      return Promise.resolve();
    }

    var item = items[index];
    return db.markSyncInProgress(item.queueId).then(function() {
      return syncItem(item);
    }).then(function() {
      return db.markSyncComplete(item.queueId);
    }).then(function() {
      return processItems(items, index + 1);
    }).catch(function(err) {
      console.error('Sync item failed:', item.queueId, err);
      return db.markSyncFailed(item.queueId, err.message).then(function() {
        return processItems(items, index + 1);
      });
    });
  }

  function syncItem(item) {
    var storeName = item.data._storeName || item.storeName;
    var fbPath = PATH_MAP[storeName];
    if (!fbPath) return Promise.reject(new Error('Unknown store: ' + storeName));

    var ref = firebaseDb.ref(fbPath);

    if (item.operation === 'create' || item.operation === 'update') {
      var fbKey = item.data[KEY_MAP[storeName]] || item.data.id;
      if (!fbKey) return Promise.reject(new Error('No key for sync'));

      // Clean record for Firebase (remove local-only fields)
      var fbData = Object.assign({}, item.data);
      fbData.syncStatus = 'synced';
      fbData.updatedAt = Date.now();

      return new Promise(function(resolve, reject) {
        ref.child(fbKey).set(fbData, function(err) {
          if (err) reject(err);
          else resolve();
        });
      });
    }

    if (item.operation === 'delete') {
      var delKey = item.data._key;
      return new Promise(function(resolve, reject) {
        ref.child(delKey).remove(function(err) {
          if (err) reject(err);
          else resolve();
        });
      });
    }

    return Promise.reject(new Error('Unknown operation: ' + item.operation));
  }

  // ─── Firebase Listeners (Read-Through Cache) ─────────────────────

  function listen(storeName, callback) {
    var fbPath = PATH_MAP[storeName];
    if (!fbPath) return null;

    var ref = firebaseDb.ref(fbPath);
    var listener = function(snapshot) {
      var data = snapshot.val();
      if (!data) return;

      // Update local cache
      var promises = [];
      var keyField = KEY_MAP[storeName];
      for (var k in data) {
        if (data.hasOwnProperty(k)) {
          var record = data[k];
          if (keyField) record[keyField] = k;
          record.syncStatus = 'synced';
          promises.push(db.put(storeName, record));
        }
      }
      Promise.all(promises).then(function() {
        if (callback) callback(data);
      }).catch(function() {});
    };

    ref.on('value', listener);
    listeners.push({ storeName: storeName, ref: ref, listener: listener });
    return listener;
  }

  function stopListening(storeName) {
    for (var i = listeners.length - 1; i >= 0; i--) {
      if (listeners[i].storeName === storeName) {
        listeners[i].ref.off('value', listeners[i].listener);
        listeners.splice(i, 1);
      }
    }
  }

  function stopAllListeners() {
    listeners.forEach(function(l) {
      l.ref.off('value', l.listener);
    });
    listeners = [];
  }

  // ─── Sync Status ─────────────────────────────────────────────────

  function getSyncStatus() {
    return db.getSyncStats().then(function(stats) {
      return {
        online: online,
        syncing: isSyncing,
        pending: stats.pending,
        failed: stats.failed,
        total: stats.total
      };
    });
  }

  function forceSync() {
    return processQueue();
  }

  // ─── Cleanup ─────────────────────────────────────────────────────

  function destroy() {
    if (syncInterval) clearInterval(syncInterval);
    if (heartbeatInterval) clearInterval(heartbeatInterval);
    stopAllListeners();
    isSyncing = false;
  }

  // ─── Export ──────────────────────────────────────────────────────

  return {
    init: init,
    onStatusChange: onStatusChangeCallback,
    create: create,
    update: update,
    remove: remove,
    get: get,
    getAll: getAll,
    getByIndex: getByIndex,
    query: query,
    listen: listen,
    stopListening: stopListening,
    stopAllListeners: stopAllListeners,
    getSyncStatus: getSyncStatus,
    forceSync: forceSync,
    processQueue: processQueue,
    destroy: destroy
  };
})();
