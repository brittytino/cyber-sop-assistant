@echo off
echo ================================================
echo   Starting Cyber-SOP Backend Server
echo ================================================
echo.

cd /d "%~dp0..\backend"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first:
    echo   1. cd backend
    echo   2. python -m venv venv
    echo   3. .\venv\Scripts\activate
    echo   4. pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Virtual environment activated
echo.

REM Check if Ollama is running
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Ollama is not running!
    echo Please start Ollama:
    echo   Open a new terminal and run: ollama serve
    echo   Or start Ollama application
    echo.
    echo Continuing anyway... backend will start but AI won't work.
    timeout /t 3
)

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

echo.
echo Starting FastAPI server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
