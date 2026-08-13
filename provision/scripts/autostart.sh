#!/bin/bash
# ─────────────────────────────────────────────────────────
# Stars & Pines — Autostart Configuration
# Sets up startup applications for Reception user
# ─────────────────────────────────────────────────────────
set -e

TARGET_USER="${SUDO_USER:-$USER}"
HOME_DIR=$(getent passwd "$TARGET_USER" | cut -d: -f6)
AUTOSTART_DIR="$HOME_DIR/.config/autostart"

echo "[AUTOSTART] Configuring startup applications..."

mkdir -p "$AUTOSTART_DIR"

# ── Web server + Firefox autostart ──
cat > "$AUTOSTART_DIR/starsandpines-web.desktop" << 'AUTOSTART'
[Desktop Entry]
Type=Application
Name=Stars & Pines Web Server
Exec=sudo systemctl start starsandpines-web || true
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
AUTOSTART

cat > "$AUTOSTART_DIR/starsandpines-dashboard.desktop" << 'AUTOSTART'
[Desktop Entry]
Type=Application
Name=Stars & Pines Dashboard
Exec=firefox --class "StarsPinesDash" --new-window "http://localhost/dashboard"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
StartupNotify=true
AUTOSTART

cat > "$AUTOSTART_DIR/starsandpines-backup-check.desktop" << 'AUTOSTART'
[Desktop Entry]
Type=Application
Name=Stars & Pines Backup Check
Exec=/usr/local/bin/starsandpines-backup.sh
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
AUTOSTART

chown -R "$TARGET_USER:$TARGET_USER" "$AUTOSTART_DIR"
chmod 644 "$AUTOSTART_DIR"/*.desktop

echo "[AUTOSTART] Autostart configured:"
ls "$AUTOSTART_DIR"