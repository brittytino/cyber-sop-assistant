
# One-click start script for Windows
# Usage: ./start.ps1

Write-Host "Starting Cyber SOP Assistant..." -ForegroundColor Green

# Start Backend
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn app.main:app --reload --port 8000" -WindowStyle Normal

# Start Frontend
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Normal

Write-Host "Services started! Check the new windows." -ForegroundColor Cyan
