@echo off
echo Starting Cyber SOP Assistant Backend...
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
