@echo off
:: Internal script to start backend from the scripts folder
cd /d "%~dp0..\backend"

if not exist "venv\Scripts\activate.bat" (
    echo [X] Virtual environment not found in backend/venv
    echo     Please run setup first.
    pause
    exit /b
)

call venv\Scripts\activate.bat

echo Starting uvicorn on 0.0.0.0:8000...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
