@echo off
cls
echo ============================================================
echo  Cyber SOP Assistant - Complete Setup and Start
echo ============================================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama not found!
    echo.
    echo Please install Ollama from: https://ollama.ai
    echo After installation, pull the model: ollama pull mistral
    echo.
    pause
    exit /b 1
)

REM Check if mistral model exists
echo Checking Ollama models...
ollama list | findstr "mistral" >nul 2>&1
if errorlevel 1 (
    echo Mistral model not found. Pulling now...
    ollama pull mistral
)

REM Setup Backend
echo.
echo [1/3] Setting up Backend...
cd backend

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python 3.11+ is installed
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

REM Check and install dependencies
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install -q --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

cd ..

REM Setup Frontend
echo.
echo [2/3] Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        pause
        exit /b 1
    )
)

cd ..

REM Start all services
echo.
echo [3/3] Starting all services...
echo.

echo Starting Ollama Service...
start "Ollama Service" cmd /k "echo Ollama Service Running && echo. && ollama serve"

timeout /t 3 /nobreak > nul

echo Starting Backend API...
start "Backend API" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && echo. && echo Backend API Starting... && echo API Docs: http://localhost:8000/api/docs && echo Health: http://localhost:8000/api/v1/health && echo. && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak > nul

echo Starting Frontend...
start "Frontend Dev Server" cmd /k "cd /d %~dp0frontend && echo. && echo Frontend Starting... && echo Application: http://localhost:3000 && echo. && npm run dev"

timeout /t 2 /nobreak > nul

cls
echo.
echo ============================================================
echo  ALL SERVICES STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo  Ollama Service:      http://localhost:11434
echo  Backend API:         http://localhost:8000
echo  API Documentation:   http://localhost:8000/api/docs
echo  Frontend App:        http://localhost:3000
echo.
echo ============================================================
echo.
echo  Three terminal windows have opened:
echo  - "Ollama Service"
echo  - "Backend API"  
echo  - "Frontend Dev Server"
echo.
echo  To stop: Close those terminal windows or press Ctrl+C
echo.
echo ============================================================
echo.
echo Opening application in browser in 5 seconds...
timeout /t 5 /nobreak > nul

start http://localhost:3000

echo.
echo Press any key to close this launcher...
pause > nul
