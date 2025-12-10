#!/usr/bin/env pwsh
# Cyber SOP Assistant - Backend Only Startup Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Starting Backend Server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
Set-Location "$PSScriptRoot\backend"

# Activate virtual environment
Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Green
& "$PSScriptRoot\backend\venv\Scripts\Activate.ps1"

# Start backend
Write-Host "[2/3] Starting FastAPI backend..." -ForegroundColor Green
Write-Host "  Backend will run at: http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "  API Docs at: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "[3/3] Server starting..." -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Run uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
