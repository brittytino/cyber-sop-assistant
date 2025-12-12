@echo off
echo ========================================
echo   Tamil Nadu Stations Setup
echo   Scrape + Store + LLM Integration
echo ========================================
echo.

REM Activate virtual environment
call ..\venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Please run from the backend folder
    pause
    exit /b 1
)

REM Run the setup script
python scripts\setup_tamil_nadu_complete.py

pause
