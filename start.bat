@echo off
echo ========================================
echo   Cyber SOP Assistant - Starting...
echo ========================================
echo.

REM Activate virtual environment
echo [1/3] Activating Python environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Start backend
echo [2/3] Starting backend server...
start "Backend" cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"
timeout /t 3 /nobreak >nul

REM Start frontend
echo [3/3] Starting frontend server...
start "Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 5 /nobreak >nul

REM Open browser
start http://localhost:5173

echo.
echo ========================================
echo   Application Started!
echo ========================================
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/api/docs
echo ========================================
echo.
echo Close the terminal windows to stop servers.
pause
