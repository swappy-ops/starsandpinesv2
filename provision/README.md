# Stars & Pines — Provisioning System

This directory contains all configuration files and scripts needed to provision a fresh MX Linux installation into a dedicated Stars & Pines Operations Terminal.

## Contents

```
provision/
├── nginx/
│   └── starsandpines          # Nginx vhost config
├── systemd/
│   ├── starsandpines-web.service    # Web server service
│   ├── starsandpines-backup.service # Backup service
│   └── starsandpines-backup.timer   # Daily backup timer
├── backup/
│   └── starsandpines-backup.sh      # Backup script
├── firefox/
│   └── setup-firefox.sh             # Firefox profile setup
├── launchers/
│   ├── starsandpines-dashboard.desktop
│   ├── starsandpines-reservations.desktop
│   ├── starsandpines-checkin.desktop
│   ├── starsandpines-portal.desktop
│   ├── starsandpines-staff.desktop
│   └── starsandpines-website.desktop
├── scripts/
│   ├── create-dirs.sh               # Directory structure creator
│   ├── guest-checkin.sh             # Guest check-in + WhatsApp
│   └── autostart.sh                 # Autostart configuration
├── branding/
│   └── wallpaper-spec.md            # Wallpaper + branding spec
└── docs/
    └── (documentation)
```

## Quick Start

```bash
# On a fresh MX Linux install:
sudo ./install-stars-pines.sh
```

## What Gets Installed

### Web Server
- Nginx configured with URL rewrites for all 5 apps
- Auto-starts on boot via systemd
- Serves `/var/www/starsandpines`

### System Services
- `starsandpines-web` — Nginx web server
- `starsandpines-backup.timer` — Daily backup at 3am
- Backup script runs daily, keeps 7 days of daily backups

### User Environment
- `~/StarsAndPines/` directory with full structure
- Desktop launchers for all apps
- Firefox profile "StarsAndPines" with bookmarks toolbar
- Autostart: web server + Firefox dashboard on login

### Branding
- Wallpaper specification with download links
- GTK theme configuration (Adwaita dark)
- LightDM greeter wallpaper hint

## User Accounts

The installer targets the user running `sudo`. The primary operator account should be:
- **Reception** (default login) — daily operations
- **Manager** — overview and reports
- **Guest Services** — guest interactions

Create additional accounts after installation:
```bash
sudo adduser reception
sudo adduser manager
sudo adduser guestservices
```

## Operations Directory Structure

```
~/StarsAndPines/
├── Operations/
│   ├── logs/          # System + backup logs
│   ├── cache/         # Temp files
│   └── temp/          # Working files
├── Reservations/      # Booking records
├── Guests/            # Guest information
├── Reports/           # Daily + monthly reports
├── Finance/           # Financial records
├── Vendors/           # Vendor contacts + invoices
├── Media/             # Photos, videos, wallpapers
├── Marketing/         # Promo materials
├── Backups/           # Backup storage (daily/weekly/monthly)
├── Documents/         # Policies, manuals, contacts
└── Templates/         # Letter, invoice, report templates
```

## Firebase Configuration

Firebase credentials are stored in `js/firebase-config.js`. To update:
```bash
sudo nano /var/www/starsandpines/js/firebase-config.js
sudo systemctl restart starsandpines-web
```

## Backup Schedule

- **Daily:** 3:00 AM — all operations data
- **Retention:** 7 days for daily, 4 weeks for weekly, 12 months for monthly
- **Location:** `~/StarsAndPines/Backups/`
- **Manual backup:** `sudo /usr/local/bin/starsandpines-backup.sh`

## Troubleshooting

### Web server won't start
```bash
sudo nginx -t
sudo systemctl status nginx
sudo journalctl -u nginx -n 20
```

### Backup not running
```bash
sudo systemctl status starsandpines-backup.timer
sudo journalctl -u starsandpines-backup -n 20
```

### Firefox profile not loading
```bash
firefox -P StarsAndPines
# Select profile manually if default doesn't work
```

### Change wallpaper
```bash
# Download recommended wallpaper
wget -O ~/StarsAndPines/Media/wallpapers/desktop.png \
  "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80"

# Set in MX Linux settings → Desktop → Background
```