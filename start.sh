#!/usr/bin/env bash
# Stars & Pines V2 — Start Server
# Run: bash start.sh

set -e

if [[ ! -d "venv" ]]; then
    echo "Virtual environment not found. Run setup.sh first."
    exit 1
fi

source venv/bin/activate

echo "╔══════════════════════════════════════════╗"
echo "║   Stars & Pines V2 — Starting Server    ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Apps:"
echo "  Guest Entry:  http://localhost:8000/guest-entry/"
echo "  Guest Portal: http://localhost:8000/guest-portal/"
echo "  Family App:   http://localhost:8000/family-app/"
echo "  API Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
