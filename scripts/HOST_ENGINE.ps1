# Cyber SOP Assistant - Central Server Host Script
# Run this script as Administrator to host the system for your network

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Cyber SOP Assistant - Central System Host      " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check for Administrator Privileges (Required for Firewall)
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator." -ForegroundColor Yellow
    Write-Host "Firewall rules might not be updated automatically." -ForegroundColor Yellow
    Write-Host "If other developers cannot connect, please restart this script as Administrator." -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 2
}

# 2. Detect Local IP Address
Write-Host "Detecting Network Configuration..." -ForegroundColor Cyan
$ipObj = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.InterfaceAlias -notlike "*Loopback*" -and 
    $_.InterfaceAlias -notlike "*vEthernet*" -and 
    $_.IPAddress -notlike "169.254.*" 
} | Sort-Object -Property InterfaceIndex | Select-Object -First 1

if ($ipObj) {
    $localIP = $ipObj.IPAddress
} else {
    # Fallback
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"} | Select-Object -First 1).IPAddress
}

if (-not $localIP) { $localIP = "localhost" }

Write-Host "HOST IP ADDRESS: $localIP" -ForegroundColor Green
Write-Host "--------------------------------------------------" -ForegroundColor Gray

# 3. Configure Firewall (If Admin)
if ($isAdmin) {
    Write-Host "Configuring Windows Firewall..." -ForegroundColor Cyan
    try {
        # Backend Port 8000
        $rule8000 = Get-NetFirewallRule -DisplayName "Cyber SOP Backend" -ErrorAction SilentlyContinue
        if (-not $rule8000) {
            New-NetFirewallRule -DisplayName "Cyber SOP Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow -Profile Any | Out-Null
            Write-Host "  [+] Allowed Port 8000 (Backend)" -ForegroundColor Green
        } else {
            Write-Host "  [.] Port 8000 already allowed" -ForegroundColor Gray
        }

        # Ollama Port 11434
        $rule11434 = Get-NetFirewallRule -DisplayName "Ollama LLM Server" -ErrorAction SilentlyContinue
        if (-not $rule11434) {
            New-NetFirewallRule -DisplayName "Ollama LLM Server" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow -Profile Any | Out-Null
            Write-Host "  [+] Allowed Port 11434 (Ollama)" -ForegroundColor Green
        } else {
            Write-Host "  [.] Port 11434 already allowed" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  [!] Failed to configure firewall: $_" -ForegroundColor Red
    }
}

# 4. Start Ollama (LLM)
Write-Host "Starting Ollama LLM Server..." -ForegroundColor Cyan
# Kill existing ollama if running to ensure we bind to 0.0.0.0
$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
if ($ollamaProcess) {
    Write-Host "  Restarting Ollama to apply network binding..." -ForegroundColor Yellow
    Stop-Process -Name ollama -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Set Environment Variable to listen on all interfaces
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_ORIGINS = "*"

try {
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Write-Host "  [+] Ollama started on 0.0.0.0:11434" -ForegroundColor Green
} catch {
    Write-Host "  [!] Failed to start Ollama. Is it installed?" -ForegroundColor Red
}

# 5. Generate Connection Info for Other Developers
$devGuide = @"
==================================================
   CONNECTION INFO FOR OTHER DEVELOPERS
==================================================

Give these details to your team:

1. Backend API URL: http://$($localIP):8000
2. Ollama URL:      http://$($localIP):11434

INSTRUCTIONS FOR TEAM MEMBERS:
------------------------------
1. Open 'frontend/.env.development' in their VS Code.
2. Update these lines:
   VITE_API_BASE_URL=http://$($localIP):8000
   VITE_OLLAMA_URL=http://$($localIP):11434

3. If they are running the Backend locally but want to use YOUR Ollama:
   Update 'config/development/backend.env':
   OLLAMA_BASE_URL=http://$($localIP):11434

==================================================
"@

Write-Host $devGuide -ForegroundColor White

# 6. Start Backend
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
# Point to the new internal script in the scripts folder
Start-Process cmd.exe -ArgumentList "/k", "scripts\run_backend.bat"

Write-Host "System is running!" -ForegroundColor Green
Write-Host "Keep this window open." -ForegroundColor Gray
