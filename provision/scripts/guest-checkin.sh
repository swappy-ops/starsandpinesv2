#!/bin/bash
# ─────────────────────────────────────────────────────────
# Stars & Pines — Guest Check-In & WhatsApp Launcher
# Usage: ./guest-checkin.sh
# ─────────────────────────────────────────────────────────
set -e

WHATSAPP_NUM="917982523582"
WHATSAPP_URL="https://wa.me/$WHATSAPP_NUM"
FIREFOX_BIN="${FIREFOX_BIN:-firefox}"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   Stars & Pines — Guest Check-In             ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

read -rp "Guest Name: " GUEST_NAME
read -rp "Phone Number (10 digits): " PHONE
read -rp "Room: " ROOM
read -rp "Access Code (6 digits): " ACCESS_CODE

# Validate
if [ -z "$GUEST_NAME" ] || [ -z "$PHONE" ] || [ -z "$ROOM" ] || [ -z "$ACCESS_CODE" ]; then
    echo "Error: All fields required."
    exit 1
fi

# Generate message
MESSAGE="Namaste $GUEST_NAME! Welcome to Stars & Pines, Crank's Ridge."
MESSAGE+="%0A%0AYour details:"
MESSAGE+="%0A• Room: $ROOM"
MESSAGE+="%0A• Access Code: $ACCESS_CODE"
MESSAGE+="%0A%0AGuest Portal: http://starsandpines.in/portal"
MESSAGE+="%0A%0APlease enter your Access Code and last 4 digits of your phone to login."
MESSAGE+="%0A%0AWe look forward to hosting you! — Stars & Pines Team"

# Open WhatsApp with pre-filled message
WHATSAPP_FULL="https://wa.me/$WHATSAPP_NUM?text=$MESSAGE"

echo ""
echo "Opening WhatsApp with pre-filled message..."
echo ""
echo "Message preview:"
echo "$GUEST_NAME | $ROOM | Code: $ACCESS_CODE"
echo ""

$FIREFOX_BIN --new-window "$WHATSAPP_FULL" 2>/dev/null || xdg-open "$WHATSAPP_FULL" 2>/dev/null || echo "Please open manually: $WHATSAPP_FULL"

echo ""
echo "Done!"