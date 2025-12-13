# ========================================
# DEVELOPER QUICK START
# Connect to Central Backend Server
# ========================================

Write-Host "👨‍💻 Cyber SOP Assistant - Developer Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$HOST_IP = "192.168.9.160"  # Update this with host's IP address
$BACKEND_PORT = "8000"
$OLLAMA_PORT = "11434"

Write-Host "🔍 Checking connection to central server..." -ForegroundColor Yellow
Write-Host "   Host IP: $HOST_IP" -ForegroundColor Gray
Write-Host ""

# Test network connectivity
Write-Host "📡 Testing network connectivity..." -ForegroundColor Cyan
$pingResult = Test-Connection -ComputerName $HOST_IP -Count 1 -Quiet

if ($pingResult) {
    Write-Host "✅ Network connection successful" -ForegroundColor Green
} else {
    Write-Host "❌ Cannot reach host server at $HOST_IP" -ForegroundColor Red
    Write-Host "   Please check:" -ForegroundColor Yellow
    Write-Host "   1. Host IP address is correct" -ForegroundColor Yellow
    Write-Host "   2. You're on the same network" -ForegroundColor Yellow
    Write-Host "   3. Host's firewall allows connections" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Test backend connection
Write-Host "🐍 Testing backend API..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://${HOST_IP}:${BACKEND_PORT}/health" -Method Get -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Backend API is accessible" -ForegroundColor Green
    Write-Host "   URL: http://${HOST_IP}:${BACKEND_PORT}" -ForegroundColor Gray
} catch {
    Write-Host "❌ Cannot connect to backend API" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   Please ensure host has started the backend server" -ForegroundColor Yellow
}

Write-Host ""

# Test Ollama connection
Write-Host "🤖 Testing Ollama LLM..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://${HOST_IP}:${OLLAMA_PORT}/api/tags" -Method Get -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Ollama LLM is accessible" -ForegroundColor Green
    Write-Host "   URL: http://${HOST_IP}:${OLLAMA_PORT}" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Cannot connect to Ollama (this is OK if backend handles it)" -ForegroundColor Yellow
}

Write-Host ""

# Check if frontend exists
if (-not (Test-Path "frontend")) {
    Write-Host "❌ Frontend directory not found!" -ForegroundColor Red
    Write-Host "   Please run this from the project root directory" -ForegroundColor Yellow
    exit 1
}

# Update or create .env file
Write-Host "⚙️  Configuring frontend environment..." -ForegroundColor Cyan

$envContent = @"
# Backend API Configuration - Central Server
VITE_API_BASE_URL=http://${HOST_IP}:${BACKEND_PORT}
VITE_API_VERSION=v1

# Optional: Direct Ollama access
VITE_OLLAMA_URL=http://${HOST_IP}:${OLLAMA_PORT}

# Environment
VITE_ENV=development
"@

$envContent | Out-File -FilePath "frontend\.env" -Encoding UTF8
$envContent | Out-File -FilePath "frontend\.env.development" -Encoding UTF8

Write-Host "✅ Environment configuration updated" -ForegroundColor Green
Write-Host "   File: frontend\.env" -ForegroundColor Gray

Write-Host ""

# Check if node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Cyan
    Write-Host "   (This may take a few minutes...)" -ForegroundColor Gray
    Write-Host ""
    
    Push-Location frontend
    npm install
    Pop-Location
    
    Write-Host ""
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Starting frontend development server..." -ForegroundColor Yellow
Write-Host ""

# Start frontend
Push-Location frontend
npm run dev
Pop-Location
