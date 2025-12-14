@echo off
echo ================================================
echo   Cyber-SOP Assistant - Complete Setup
echo ================================================
echo.
echo This script will set up the entire project.
echo Make sure you have installed:
echo   - Python 3.10+
echo   - Node.js 18+
echo   - Ollama (with mistral:instruct model)
echo.
pause

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check Ollama
echo.
echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Ollama is not running!
    echo Please:
    echo   1. Install Ollama from https://ollama.ai/download/windows
    echo   2. Run: ollama pull mistral:instruct
    echo   3. Start Ollama service
    echo.
    echo Do you want to continue anyway? (Y/N)
    set /p continue=
    if /i not "%continue%"=="Y" exit /b 1
)

echo.
echo ================================================
echo Step 1: Setting up Backend
echo ================================================
cd /d "%~dp0..\backend"

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo .env file created. Please update if needed.
) else (
    echo .env file already exists.
)

echo.
echo Initializing database...
python scripts\init_db.py

echo.
echo ================================================
echo Step 2: Setting up Frontend
echo ================================================
cd /d "%~dp0..\frontend"

echo Installing Node.js dependencies...
call npm install

echo Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo .env file created.
) else (
    echo .env file already exists.
)

echo.
echo ================================================
echo   Setup Complete! ✅
echo ================================================
echo.
echo To run the application:
echo   1. Start backend:  scripts\dev_backend.cmd
echo   2. Start frontend: scripts\dev_frontend.cmd
echo   3. Open browser:   http://localhost:5173
echo.
echo Or use the quick start script: scripts\start_all.cmd
echo.
pause
