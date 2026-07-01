#!/bin/bash
# ─────────────────────────────────────────────────────────
# Stars & Pines — Directory Structure Creator
# Run by install-stars-pines.sh — not standalone
# ─────────────────────────────────────────────────────────
set -e

TARGET_USER="${SUDO_USER:-$USER}"
HOME_DIR=$(getent passwd "$TARGET_USER" | cut -d: -f6)

echo "[DIRS] Creating StarsAndPines directory structure..."

SP_HOME="$HOME_DIR/StarsAndPines"

mkdir -p "$SP_HOME"/{Operations,Reservations,Guests,Reports,Finance,Vendors,Media,Marketing,Backups,Documents,Templates}
mkdir -p "$SP_HOME/Operations"/{logs,cache,temp}
mkdir -p "$SP_HOME/Backups"/{daily,weekly,monthly}
mkdir -p "$SP_HOME/Documents"/{manuals,policies,contacts}
mkdir -p "$SP_HOME/Media"/{photos,videos,promo}
mkdir -p "$SP_HOME/Templates"/{letters,invoices,reports}

# Set permissions
chown -R "$TARGET_USER:$TARGET_USER" "$SP_HOME"
chmod -R 755 "$SP_HOME"

echo "[DIRS] Directory structure created at $SP_HOME"
echo "[DIRS] Contents:"
find "$SP_HOME" -type d | sed "s|$SP_HOME||" | sort | while read d; do echo "  $d/"; done