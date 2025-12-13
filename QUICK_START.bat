@echo off
REM Fast Setup and Run Script for Windows
REM Automatically sets up LLM and starts the system

echo ================================================================================
echo   CYBER SOP ASSISTANT - QUICK START (WINDOWS)
echo ================================================================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
cd backend
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run universal setup
echo.
echo ================================================================================
echo   RUNNING SYSTEM SETUP
echo ================================================================================
echo.
python scripts\universal_setup.py
if errorlevel 1 (
    echo.
    echo ERROR: Setup failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo   STARTING BACKEND SERVER
echo ================================================================================
echo.
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
