# Test Chat API
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    query = "I lost money in a UPI scam"
    language = "ENGLISH"
    include_sources = $true
} | ConvertTo-Json

Write-Host "Testing Chat API..." -ForegroundColor Cyan
Write-Host "Sending request to: http://localhost:8000/api/v1/chat" -ForegroundColor Yellow
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Headers $headers -Body $body -TimeoutSec 60
    
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Crime Type: $($response.crime_type)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Immediate Actions:" -ForegroundColor Yellow
    $response.immediate_actions | ForEach-Object { Write-Host "  - $_" }
    Write-Host ""
    Write-Host "Reporting Steps:" -ForegroundColor Yellow
    $response.reporting_steps | ForEach-Object { Write-Host "  - $_" }
    Write-Host ""
    Write-Host "Response Time: $($response.processing_time_ms)ms" -ForegroundColor Magenta
}
catch {
    Write-Host "ERROR!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure the backend is running:" -ForegroundColor Yellow
    Write-Host "  .\START_BACKEND.ps1" -ForegroundColor Cyan
}
