@echo off
title Smart NER Logistics - Temporary Public Share
echo ===================================================
echo   Smart NER Logistics Control Platform
echo   Temporary Public Web Deployment (Cloudflare Tunnel)
echo ===================================================
echo.
cd /d "%~dp0"

:: Check if server is already running on port 8000
netstat -ano | findstr :8000 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo Starting local FastAPI backend server...
    start "FastAPI Server" /min python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
    timeout /t 3 /nobreak >nul
) else (
    echo Local FastAPI backend is already running on port 8000.
)

echo.
echo Starting secure public tunnel via Cloudflare...
echo Your public HTTPS link will appear below:
echo ===================================================
echo.

.\cloudflared.exe tunnel --protocol http2 --url http://127.0.0.1:8000

pause
