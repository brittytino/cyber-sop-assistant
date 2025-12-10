# Health Check Script

Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Health Check" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check Ollama
Write-Host "Ollama..." -NoNewline
try {
    Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -UseBasicParsing | Out-Null
    Write-Host " OK" -ForegroundColor Green
}
catch {
    Write-Host " NOT RUNNING" -ForegroundColor Red
}

# Check Backend
Write-Host "Backend..." -NoNewline
try {
    Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -TimeoutSec 5 -UseBasicParsing | Out-Null
    Write-Host " OK" -ForegroundColor Green
}
catch {
    Write-Host " NOT RUNNING" -ForegroundColor Red
}

# Check Frontend
Write-Host "Frontend..." -NoNewline
try {
    Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing | Out-Null
    Write-Host " OK" -ForegroundColor Green
}
catch {
    Write-Host " NOT RUNNING" -ForegroundColor Red
}

Write-Host ""
Write-Host "If all OK, open: http://localhost:3000" -ForegroundColor White
Write-Host ""
