# Cyber SOP Assistant - Central Server Startup

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Cyber SOP Assistant - Central Server  " -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get IP
`$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {`$_.IPAddress -like "192.168.*"} | Select-Object -First 1).IPAddress
if (-not `$ip) { `$ip = "localhost" }

Write-Host "IP Address: `$ip" -ForegroundColor Green
Write-Host ""

# Check prerequisites
if (-not (Test-Path "backend\venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Read-Host "Press Enter"
    exit 1
}

# Firewall
Write-Host "Configuring firewall..." -ForegroundColor Cyan
try {
    Get-NetFirewallRule -DisplayName "Cyber SOP Backend" -ErrorAction SilentlyContinue | Out-Null
    if (`$LASTEXITCODE -eq 0) {
        New-NetFirewallRule -DisplayName "Cyber SOP Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow -ErrorAction Stop | Out-Null
    }
    Get-NetFirewallRule -DisplayName "Ollama LLM Server" -ErrorAction SilentlyContinue | Out-Null
    if (`$LASTEXITCODE -eq 0) {
        New-NetFirewallRule -DisplayName "Ollama LLM Server" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow -ErrorAction Stop | Out-Null
    }
    Write-Host "Firewall configured" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Run as Admin to configure firewall" -ForegroundColor Yellow
}

# Start Ollama
Write-Host "Checking Ollama..." -ForegroundColor Cyan
if (-not (Get-Process ollama -ErrorAction SilentlyContinue)) {
    `$env:OLLAMA_HOST = "0.0.0.0:11434"
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 2
}
Write-Host "Ollama running" -ForegroundColor Green

# Start Backend
Write-Host "Starting backend..." -ForegroundColor Cyan
Start-Process cmd.exe -ArgumentList "/k", "start_backend.bat"
Write-Host "Backend starting (check new window)" -ForegroundColor Green

Write-Host ""
Start-Sleep -Seconds 8
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "     SERVER READY!    " -ForegroundColor Green  
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  http://`${ip}:8000" -ForegroundColor White
Write-Host "API Docs:     http://`${ip}:8000/api/docs" -ForegroundColor White  
Write-Host "Ollama LLM:   http://`${ip}:11434" -ForegroundColor White
Write-Host ""
Write-Host "Share with developers:" -ForegroundColor Yellow
Write-Host "VITE_API_BASE_URL=http://`${ip}:8000" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"
