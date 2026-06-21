@echo off
REM Stars & Pines V2 — Start Server
REM Run: start.bat

if not exist "venv" (
    echo Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo ╔══════════════════════════════════════════╗
echo ║   Stars ^& Pines V2 — Starting Server    ║
echo ╚══════════════════════════════════════════╝
echo.
echo Apps:
echo   Guest Entry:  http://localhost:8000/guest-entry/
echo   Guest Portal: http://localhost:8000/guest-portal/
echo   Family App:   http://localhost:8000/family-app/
echo   API Docs:     http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
