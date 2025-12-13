@echo off
echo Starting Backend API Server...
echo ================================
echo.

cd /d "%~dp0backend"

call venv\Scripts\activate.bat

echo Starting uvicorn on 0.0.0.0:8000...
echo API will be available at your local IP address on port 8000
echo API Docs at: /api/docs
echo.
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
