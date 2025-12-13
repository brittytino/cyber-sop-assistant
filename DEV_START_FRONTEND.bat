@echo off
:: ==========================================
::  CYBER SOP ASSISTANT - DEVELOPER FRONTEND
::  Run this to start the Frontend Interface
:: ==========================================

echo.
echo  Cyber SOP Assistant - Frontend Dev
echo ==========================================
echo.

cd frontend

:: Check if node_modules exists
if not exist "node_modules\" (
    echo [!] First time setup: Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [X] Failed to install dependencies. Do you have Node.js installed?
        pause
        exit /b
    )
)

echo.
echo [i] REMINDER: Ensure you have updated '.env.development'
echo     with the Host IP address provided by your team lead.
echo.
echo Starting Frontend...
echo.

call npm run dev

pause
