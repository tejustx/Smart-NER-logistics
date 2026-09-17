@echo off
title Smart NER Logistics Platform Server
echo ===================================================
echo   Smart NER Logistics Control Platform
echo   Starting server at http://127.0.0.1:8000 ...
echo ===================================================
echo.
cd /d "%~dp0"
:: Open browser once the server has bound port 8000
start "" /b cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/signup"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
