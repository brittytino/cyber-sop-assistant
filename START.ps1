# Cyber SOP Assistant - Startup Script
# Run this in VS Code PowerShell terminal

$ErrorActionPreference = "Continue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Cyber SOP Assistant - Complete Local Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1. CHECK OLLAMA
Write-Host "[1/6] Checking Ollama..." -ForegroundColor Yellow
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Ollama not found!" -ForegroundColor Red
    Write-Host "  Install from: https://ollama.ai" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$ollamaList = ollama list 2>&1 | Out-String
if ($ollamaList -notmatch "mistral") {
    Write-Host "  Pulling Mistral model..." -ForegroundColor Yellow
    ollama pull mistral
}
Write-Host "  OK Ollama ready!" -ForegroundColor Green
Write-Host ""

# 2. SETUP BACKEND
Write-Host "[2/6] Setting up Backend..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "  Activating venv..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"

$fastApiCheck = pip show fastapi 2>&1 | Out-String
if ($fastApiCheck -notmatch "Name: fastapi") {
    Write-Host "  Installing dependencies (3-5 minutes)..." -ForegroundColor Yellow
    pip install --upgrade pip --quiet
    pip install fastapi uvicorn sqlalchemy aiosqlite httpx pydantic pydantic-settings python-dotenv --quiet
    pip install chromadb sentence-transformers --quiet
    pip install -r requirements.txt --quiet 2>&1 | Out-Null
}
else {
    Write-Host "  Dependencies OK, verifying..." -ForegroundColor Gray
    $aioCheck = pip show aiosqlite 2>&1 | Out-String
    if ($aioCheck -notmatch "Name: aiosqlite") {
        pip install aiosqlite --quiet
    }
}

Write-Host "  OK Backend ready!" -ForegroundColor Green
Set-Location ..
Write-Host ""

# 3. SETUP FRONTEND
Write-Host "[3/6] Setting up Frontend..." -ForegroundColor Yellow
Set-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing npm packages..." -ForegroundColor Gray
    npm install 2>&1 | Out-Null
}

Write-Host "  OK Frontend ready!" -ForegroundColor Green
Set-Location ..
Write-Host ""

# 4. POPULATE DATABASE
Write-Host "[4/6] Checking database..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path "data\vectorstore\chroma.sqlite3")) {
    Write-Host "  Populating knowledge base (1-2 min)..." -ForegroundColor Yellow
    & "venv\Scripts\python.exe" "scripts\populate_cybercrime_data.py" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Database populated!" -ForegroundColor Green
    }
    else {
        Write-Host "  Warning: Database population had issues" -ForegroundColor Yellow
    }
}
else {
    Write-Host "  OK Database exists!" -ForegroundColor Green
}

Set-Location ..
Write-Host ""

# 5. START SERVICES
Write-Host "[5/6] Starting services..." -ForegroundColor Yellow

# Clean old processes
Get-Process | Where-Object { $_.ProcessName -match "ollama|uvicorn|node" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Start Ollama
Write-Host "  Starting Ollama..." -ForegroundColor Gray
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 3

# Start Backend
Write-Host "  Starting Backend..." -ForegroundColor Gray
Set-Location backend
$backendScript = @"
`& venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript
Start-Sleep -Seconds 5
Set-Location ..

# Start Frontend
Write-Host "  Starting Frontend..." -ForegroundColor Gray
Set-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
Start-Sleep -Seconds 3
Set-Location ..

Write-Host "  OK All services started!" -ForegroundColor Green
Write-Host ""

# 6. OPEN BROWSER
Write-Host "[6/6] Opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     ALL SERVICES RUNNING!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/api/docs" -ForegroundColor White
Write-Host ""
Write-Host "  Helpline: 1930 | Portal: cybercrime.gov.in" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Start-Process "http://localhost:3000"

Write-Host "Services running in separate windows. Press Enter to exit..." -ForegroundColor Gray
Read-Host
