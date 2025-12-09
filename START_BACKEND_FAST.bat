@echo off
cls
echo ============================================================
echo  Cyber SOP Assistant - Optimized Local Ollama Backend
echo ============================================================
echo.

cd /d "%~dp0backend"

if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo ============================================================
echo  Backend Server Starting with Optimized Settings
echo ============================================================
echo.
echo  Local Ollama Configuration:
echo  - Model: Mistral 7B Instruct
echo  - Response time: 2-5 seconds
echo  - Context window: 4096 tokens
echo  - Multilingual: 8 Indian languages
echo  - No external API calls
echo.
echo  Endpoints:
echo  - API Documentation: http://localhost:8000/api/docs
echo  - Health Check:      http://localhost:8000/api/v1/health
echo  - Chat:              http://localhost:8000/api/v1/chat/v2
echo  - Multilingual Chat: http://localhost:8000/api/v1/multilingual/chat
echo.
echo ============================================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level info
