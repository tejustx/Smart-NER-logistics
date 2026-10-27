@echo off
setlocal enabledelayedexpansion
title Smart NER Logistics Platform Server

echo ======================================================================
echo           Smart NER Logistics Control Platform
echo        Risk-Weighted Freight Routing ^& Offline Navigation
echo ======================================================================
echo.

cd /d "%~dp0"

:: 1. Detect Python 3 environment (tries python, py -3, py)
set "PY_CMD="
python -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_CMD=python"
) else (
    py -3 -c "import sys; sys.exit(0)" >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY_CMD=py -3"
    ) else (
        py -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" >nul 2>&1
        if !errorlevel! equ 0 (
            set "PY_CMD=py"
        )
    )
)

if not defined PY_CMD (
    echo [ERROR] Python 3 was not detected in your system PATH!
    echo Please make sure Python 3 is installed and added to PATH.
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [*] Using Python: !PY_CMD!

:: 2. Check if port 8000 is occupied by a stale/previous process
netstat -ano | findstr /r ":8000 .*LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo [!] Port 8000 is currently occupied.
    echo [*] Terminating stale process on port 8000 to ensure clean startup...
    powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { try { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } catch {} }" >nul 2>&1
    powershell -NoProfile -Command "Start-Sleep -Milliseconds 600" >nul 2>&1
)

:: 3. Launch browser helper (polls health endpoint and opens default browser once server is ready)
start "" /min !PY_CMD! backend\open_browser.py http://127.0.0.1:8000

echo [*] Starting FastAPI application server on http://127.0.0.1:8000 ...
echo [*] Browser will open automatically once the server is ready.
echo.
echo ======================================================================
echo   Local Web Interface: http://127.0.0.1:8000
echo   Direct Sign-up Page: http://127.0.0.1:8000/signup
echo   API Health Endpoint: http://127.0.0.1:8000/api/health
echo   Interactive Swagger: http://127.0.0.1:8000/docs
echo ======================================================================
echo.

!PY_CMD! -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo [*] Server has been stopped.
pause
