#!/bin/bash
# ─────────────────────────────────────────────────────────
# Stars & Pines — Daily Backup Script
# Called by systemd service — do not run standalone
# ─────────────────────────────────────────────────────────
set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/StarsAndPines/Backups/daily"
RETENTION_DAYS=7

# Create backup dir
mkdir -p "$BACKUP_DIR"

# Files to backup
SRC_WEB="/var/www/starsandpines"
SRC_DB="$HOME/StarsAndPines"
BACKUP_NAME="starsandpines_backup_${TIMESTAMP}.tar.gz"

echo "[BACKUP] Starting backup: $BACKUP_NAME"

# Backup web files
if [ -d "$SRC_WEB" ]; then
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
        -C "$SRC_WEB" . \
        2>/dev/null || true
    echo "[BACKUP] Web files backed up"
fi

# Backup operations data
OPS_BACKUP="$BACKUP_DIR/operations_${TIMESTAMP}.tar.gz"
tar -czf "$OPS_BACKUP" \
    -C "$SRC_DB" . \
    --exclude='Backups' \
    --exclude='Media' \
    --exclude='cache' \
    --exclude='temp' \
    2>/dev/null || true

# Copy firebase config separately (encrypted ideally)
if [ -f "$SRC_WEB/js/firebase-config.js" ]; then
    cp "$SRC_WEB/js/firebase-config.js" "$BACKUP_DIR/firebase_config_${TIMESTAMP}.js.bak"
fi

# Cleanup old backups
find "$BACKUP_DIR" -name "starsandpines_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "operations_*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "firebase_config_*.js.bak" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true

# Log
echo "[BACKUP] Completed: $(date)" >> "$HOME/StarsAndPines/Operations/logs/backup.log"

echo "[BACKUP] Done. Backup stored at $BACKUP_DIR/$BACKUP_NAME"