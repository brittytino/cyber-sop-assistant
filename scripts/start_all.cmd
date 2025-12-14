@echo off
echo ================================================
echo   Starting Cyber-SOP Assistant
echo ================================================
echo.
echo Starting backend and frontend...
echo.

REM Start backend in new window
start "Cyber-SOP Backend" cmd /k "%~dp0dev_backend.cmd"

REM Wait a bit for backend to start
timeout /t 5 /nobreak

REM Start frontend in new window
start "Cyber-SOP Frontend" cmd /k "%~dp0dev_frontend.cmd"

echo.
echo Both servers are starting in separate windows.
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Your browser should open automatically.
echo If not, open: http://localhost:5173
echo.

timeout /t 3 /nobreak
start http://localhost:5173

pause
