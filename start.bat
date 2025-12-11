@echo off
REM ============================================================
REM   Cyber SOP Assistant - Complete Startup Script (Windows)
REM ============================================================

cls
echo.
echo ============================================================
echo   Cyber SOP Assistant - Starting All Services
echo ============================================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama not found!
    echo Please install from: https://ollama.ai
    echo After installation, run: ollama pull mistral:7b-instruct
    pause
    exit /b 1
)

REM Check if Mistral model is available
ollama list | findstr "mistral" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Downloading Mistral model...
    ollama pull mistral:7b-instruct
    if errorlevel 1 (
        echo [ERROR] Failed to download Mistral model
        pause
        exit /b 1
    )
)
echo [OK] Ollama and Mistral model ready
echo.

REM Setup Backend
echo [1/3] Setting up Backend...
cd /d "%~dp0backend"

if not exist "venv\Scripts\python.exe" (
    echo   - Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo Make sure Python 3.11+ is installed
        pause
        exit /b 1
    )
)

echo   - Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Check if database needs to be populated
if not exist "data\vectorstore\chroma.sqlite3" (
    echo   - Populating knowledge base...
    python scripts\populate_data.py
)

echo [OK] Backend ready
echo.

REM Setup Frontend
echo [2/3] Setting up Frontend...
cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo   - Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install npm packages
        pause
        exit /b 1
    )
)

echo [OK] Frontend ready
echo.

REM Start Services
echo [3/3] Starting Services...
echo.
echo ============================================================
echo   Starting Backend on http://localhost:8000
echo   Starting Frontend on http://localhost:3000
echo ============================================================
echo.
echo Press Ctrl+C in each terminal to stop services
echo.

REM Start backend in new terminal
cd /d "%~dp0backend"
start "Cyber SOP Backend" cmd /k "call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new terminal
cd /d "%~dp0frontend"
start "Cyber SOP Frontend" cmd /k "npm run dev"

REM Wait for services to start
timeout /t 2 /nobreak >nul

echo.
echo ============================================================
echo   Services Started Successfully!
echo ============================================================
echo.
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/api/docs
echo   Frontend:     http://localhost:3000
echo.
echo   Close this window or press any key to exit
echo ============================================================
pause >nul
