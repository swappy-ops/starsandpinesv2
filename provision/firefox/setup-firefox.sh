#!/bin/bash
# ─────────────────────────────────────────────────────────
# Stars & Pines — Firefox Profile Setup
# ─────────────────────────────────────────────────────────
set -e

TARGET_USER="${SUDO_USER:-$USER}"
HOME_DIR=$(getent passwd "$TARGET_USER" | cut -d: -f6)
FIREFOX_PROF_DIR="$HOME_DIR/.mozilla/firefox"
PROF_NAME="StarsAndPines"
PROF_DIR="$FIREFOX_PROF_DIR/$PROF_NAME.default-release"

echo "[FIREFOX] Setting up Firefox profile: $PROF_NAME"

mkdir -p "$PROF_DIR"

# ── Create prefs.js with homepage + settings ──
cat > "$PROF_DIR/prefs.js" << 'PREFS'
user_pref("browser.startup.homepage", "http://localhost");
user_pref("browser.startup.homepage.override", "http://localhost");
user_pref("browser.startup.page", 1);
user_pref("browser.sessionstore.resume_from_crash", true);
user_pref("browser.sessionstore.max_tabs_undo", 10);
user_pref("browser.showQuitWarning", false);
user_pref("browser.tabs.warnOnClose", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.bookmarks.autoExportHTML", false);
user_pref("browser.toolbars.bookmarks.visibility", "toolbar");
user_pref("browser.uidensity", 0);
user_pref("browser.download.improvements_to_download_panel", true);
user_pref("browser.download.open_pdf_containing_links", true);
user_pref("network.cookie.cookieBehavior", 1);
user_pref("privacy.trackingprotection.enabled", false);
user_pref("signon.rememberSignons", true);
user_pref("datareporting.healthreport.service.enabled", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("browser.laterrun.bookmarks.enabled", false);
user_pref("browser.messaging-system.pioneerStudy.enrollByDate", "");
user_pref("app.normandy.enabled", false);
PREFS

# ── Create bookmarks.html ──
cat > "$PROF_DIR/bookmarks.html" << 'BOOKMARKS'
<!DOCTYPE NETSCAPE-Bookmarks-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1 LAST_MODIFIED="202506150000">Bookmarks</H1>
<DL><p>
    <DT><H3 PERSONAL_TOOLBAR_FOLDER="true" BOOKMARK_FOLDER="Bookmarks Toolbar">Bookmarks Toolbar</H3>
    <DL><p>
        <DT><A HREF="http://localhost/portal" ICON="data:image/png;base64,">Guest Portal</A></DT>
        <DT><A HREF="http://localhost/dashboard" ICON="data:image/png;base64,">Operations Dashboard</A></DT>
        <DT><A HREF="http://localhost/staff" ICON="data:image/png;base64,">Staff App</A></DT>
        <DT><A HREF="https://wa.me/917982523582" ICON="data:image/png;base64,">WhatsApp Web</A></DT>
        <DT><A HREF="https://mail.google.com" ICON="data:image/png;base64,">Gmail</A></DT>
        <DT><A HREF="https://drive.google.com" ICON="data:image/png;base64,">Google Drive</A></DT>
        <DT><A HREF="https://console.firebase.google.com" ICON="data:image/png;base64,">Firebase Console</A></DT>
        <DT><A HREF="http://localhost" ICON="data:image/png;base64,">Property Website</A></DT>
        <DT><A HREF="http://localhost/entry" ICON="data:image/png;base64,">Guest Entry</A></DT>
    </DL><p>
    <DT><H3>Folders</H3>
    <DL><p>
        <DT><H3>Property Management</H3>
        <DL><p>
            <DT><A HREF="http://localhost/dashboard">Operations Dashboard</A></DT>
            <DT><A HREF="http://localhost/portal">Guest Portal</A></DT>
            <DT><A HREF="http://localhost/staff">Employee App</A></DT>
            <DT><A HREF="http://localhost/entry">Guest Check-In</A></DT>
        </DL><p>
        <DT><H3>Documents</H3>
        <DL><p>
            <DT><A HREF="file://$HOME/StarsAndPines/Documents">Property Documents</A></DT>
            <DT><A HREF="file://$HOME/StarsAndPines/Operations/logs">Operations Logs</A></DT>
            <DT><A HREF="file://$HOME/StarsAndPines/Reports">Reports</A></DT>
        </DL><p>
        <DT><H3>Vendor Contacts</H3>
        <DL><p>
            <DT><A HREF="tel:+919412012345">Tewari Cab Service</A></DT>
            <DT><A HREF="https://himachaltourism.gov.in/helicopter-service/">Helicopter Booking</A></DT>
        </DL><p>
    </DL><p>
</DL><p>
BOOKMARKS

# ── Create user.js overrides ──
cat >> "$PROF_DIR/prefs.js" << 'USERJS'
user_pref("browser.shell.default-browser-check-enabled", false);
user_pref("browser.ping-centre.telemetry", false);
user_pref("browser.tabs.loadInBackground", true);
user_pref("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36");
USERJS

# ── Create profiles.ini ──
PROF_INI="$FIREFOX_PROF_DIR/../profiles.ini"
if ! grep -q "$PROF_NAME" "$PROF_INI" 2>/dev/null; then
    cat >> "$PROF_INI" << 'PROFINI'
[Profile1]
Name=StarsAndPines
IsRelative=1
Path=StarsAndPines.default-release
Default=1
PROFINI
fi

# ── Set permissions ──
chown -R "$TARGET_USER:$TARGET_USER" "$HOME_DIR/.mozilla"
chmod -R 700 "$HOME_DIR/.mozilla"

echo "[FIREFOX] Profile created at $PROF_DIR"
echo "[FIREFOX] To open: firefox -P StarsAndPines"