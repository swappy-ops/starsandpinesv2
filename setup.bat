@echo off
REM Stars & Pines V2 — One-Touch Setup (Windows)
REM Run: setup.bat

echo ╔══════════════════════════════════════════╗
echo ║   Stars ^& Pines V2 — One-Touch Setup    ║
echo ╚══════════════════════════════════════════╝
echo.

REM ─── Step 1: Check Python ───
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found!
    echo.
    echo Please install Python 3.10+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PY_VER=%%i
echo [✓] Python %PY_VER% found

REM ─── Step 2: Create virtual environment ───
if not exist "venv" (
    echo [!] Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated

REM ─── Step 3: Install dependencies ───
echo [!] Installing Python dependencies...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
echo [✓] Dependencies installed

REM ─── Step 4: Setup .env ───
if not exist ".env" (
    copy .env.example .env >nul
    echo [✓] Created .env from .env.example
) else (
    echo [✓] .env already exists
)

REM ─── Step 5: Initialize database ───
echo [!] Initializing database...
python -c "from api.db import init_db; init_db()"
echo [✓] Database initialized

REM ─── Step 6: Seed data ───
echo [!] Seeding database...
python scripts\seed.py
echo [✓] Database seeded

REM ─── Step 7: Create directories ───
if not exist "assets" mkdir assets
if not exist "backups" mkdir backups
echo [✓] Directories created

echo.
echo ╔══════════════════════════════════════════╗
echo ║          Setup Complete! 🌲              ║
echo ╚══════════════════════════════════════════╝
echo.
echo To start the server:
echo   venv\Scripts\activate
echo   uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
echo.
echo Or run the launcher:
echo   start.bat
echo.
echo Access the apps:
echo   Guest Entry:  http://localhost:8000/guest-entry/
echo   Guest Portal: http://localhost:8000/guest-portal/
echo   Family App:   http://localhost:8000/family-app/
echo   API Docs:     http://localhost:8000/docs
echo.
pause
