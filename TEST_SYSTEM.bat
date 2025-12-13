@echo off
REM Test LLM System - Windows

echo ================================================================================
echo   TESTING LLM SYSTEM
echo ================================================================================
echo.

REM Activate venv
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found. Run QUICK_START.bat first.
    pause
    exit /b 1
)

cd backend

echo Running system tests...
echo.
python scripts\test_system.py

echo.
pause
