@echo off
setlocal enabledelayedexpansion
title Smart NER Logistics - Temporary Public Share

echo ======================================================================
echo           Smart NER Logistics Control Platform
echo   Temporary Public Web Deployment (Cloudflare Tunnel)
echo ======================================================================
echo.

cd /d "%~dp0"

:: 1. Detect Python 3 environment
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

:: 2. Verify cloudflared.exe exists
if not exist ".\cloudflared.exe" (
    echo [ERROR] cloudflared.exe binary was not found in the root directory!
    echo Please ensure cloudflared.exe is present.
    echo.
    pause
    exit /b 1
)

:: 3. Check if local backend is already healthy on port 8000
!PY_CMD! -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=1)" >nul 2>&1
if !errorlevel! neq 0 (
    echo [*] Starting local FastAPI backend server in background...
    start "FastAPI Server" /min !PY_CMD! -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
    
    :: Wait until server responds to health check (up to 15 seconds)
    echo [*] Waiting for server startup...
    powershell -NoProfile -Command "for ($i=0; $i -lt 30; $i++) { try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1; if ($r.StatusCode -eq 200) { exit 0 } } catch {}; Start-Sleep -Milliseconds 500 }; exit 1" >nul 2>&1
    if !errorlevel! equ 0 (
        echo [*] FastAPI backend server is up and healthy!
    ) else (
        echo [!] Backend took longer than expected to report healthy, proceeding with tunnel...
    )
) else (
    echo [*] Local FastAPI backend is already running and healthy on port 8000.
)

echo.
echo ======================================================================
echo Starting secure public tunnel via Cloudflare...
echo Your public HTTPS link will appear below (look for the .trycloudflare.com URL):
echo ======================================================================
echo.

.\cloudflared.exe tunnel --protocol http2 --url http://127.0.0.1:8000

echo.
echo [*] Cloudflare tunnel session closed.
pause
