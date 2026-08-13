#!/usr/bin/env bash
# Stars & Pines V2 — One-Touch Setup
# For fresh PCs with nothing installed (Linux only)
# Run: curl -sL <url> | bash  OR  bash setup.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err() { echo -e "${RED}[✗]${NC} $1"; }

echo "╔══════════════════════════════════════════╗"
echo "║   Stars & Pines V2 — One-Touch Setup    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ─── Detect OS ───
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    err "Unsupported OS: $OSTYPE"
    exit 1
fi

log "Detected OS: $OS"

# ─── Step 1: Install Python 3.10+ ───
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    log "Python $PY_VER already installed"
else
    warn "Python 3 not found — installing..."
    if [[ "$OS" == "linux" ]]; then
        if command -v apt-get &>/dev/null; then
            sudo apt-get update -qq
            sudo apt-get install -y python3 python3-pip python3-venv sqlite3
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3 python3-pip sqlite
        elif command -v pacman &>/dev/null; then
            sudo pacman -S --noconfirm python python-pip sqlite
        else
            err "No supported package manager found. Install Python 3.10+ manually."
            exit 1
        fi
    elif [[ "$OS" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            brew install python sqlite
        else
            err "Homebrew not found. Install it first: https://brew.sh"
            exit 1
        fi
    fi
    log "Python installed"
fi

# ─── Step 2: Verify Python version ───
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo $PY_VER | cut -d. -f1)
PY_MINOR=$(echo $PY_VER | cut -d. -f2)

if [[ $PY_MAJOR -lt 3 ]] || [[ $PY_MAJOR -eq 3 && $PY_MINOR -lt 10 ]]; then
    err "Python 3.10+ required, found $PY_VER"
    exit 1
fi
log "Python $PY_VER OK"

# ─── Step 3: Create virtual environment ───
if [[ ! -d "venv" ]]; then
    log "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
log "Virtual environment activated"

# ─── Step 4: Install dependencies ───
log "Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
log "Dependencies installed"

# ─── Step 5: Setup .env ───
if [[ ! -f ".env" ]]; then
    cp .env.example .env
    log "Created .env from .env.example"
else
    log ".env already exists"
fi

# ─── Step 6: Initialize database ───
log "Initializing database..."
python3 -c "from api.db import init_db; init_db()"
log "Database initialized"

# ─── Step 7: Seed data ───
log "Seeding database with rooms, beds, menu, staff, inventory..."
python3 scripts/seed.py
log "Database seeded"

# ─── Step 8: Create directories ───
mkdir -p assets backups
log "Directories created"

# ─── Done ───
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║          Setup Complete! 🌲              ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "Or run the launcher:"
echo "  bash start.sh"
echo ""
echo "Access the apps:"
echo "  Guest Entry:  http://localhost:8000/guest-entry/"
echo "  Guest Portal: http://localhost:8000/guest-portal/"
echo "  Family App:   http://localhost:8000/family-app/"
echo "  API Docs:     http://localhost:8000/docs"
echo ""
