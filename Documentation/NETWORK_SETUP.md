# 🌐 NETWORK SETUP - CENTRAL BACKEND SERVER

## Your System Configuration

**Your IP Addresses:**
- Primary: `192.168.9.160`
- Secondary: `192.168.137.1`

**Services Running:**
- Backend API: `http://192.168.9.160:8000`
- Ollama LLM: `http://192.168.9.160:11434`
- Database: SQLite (shared via backend)
- Frontend (optional): `http://192.168.9.160:5173`

---

## 🖥️ HOST SETUP (Your System)

### 1. Configure Backend for Network Access

The backend is already configured to bind to `0.0.0.0` which allows network access.

**Start Backend:**
```powershell
cd backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend is Running:**
```powershell
# From your system
curl http://192.168.9.160:8000/health

# Expected response: {"status":"healthy"}
```

### 2. Configure Ollama for Network Access

**Edit Ollama Service:**

**Option A: Windows Service (Recommended)**
1. Open Services: `Win + R` → `services.msc`
2. Find "Ollama Service"
3. Stop the service
4. Set environment variable:
   ```powershell
   [System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "Machine")
   ```
5. Restart your computer OR restart Ollama service

**Option B: Run Ollama Manually**
```powershell
# Stop Ollama service first
Stop-Service Ollama

# Run Ollama on all interfaces
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

**Verify Ollama is Accessible:**
```powershell
# From your system
curl http://192.168.9.160:11434/api/tags

# Expected: JSON with available models
```

### 3. Configure Firewall Rules

**Allow Backend Port (8000):**
```powershell
New-NetFirewallRule -DisplayName "Cyber SOP Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

**Allow Ollama Port (11434):**
```powershell
New-NetFirewallRule -DisplayName "Ollama LLM Server" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
```

**Allow Frontend Port (5173) - Optional:**
```powershell
New-NetFirewallRule -DisplayName "Vite Dev Server" -Direction Inbound -LocalPort 5173 -Protocol TCP -Action Allow
```

**Verify Firewall Rules:**
```powershell
Get-NetFirewallRule -DisplayName "Cyber SOP*" | Select-Object DisplayName, Enabled, Direction
```

### 4. Share Database Access

The SQLite database is located at:
```
D:\Work's\Github\cyber-sop-assistant\backend\data\cyber_sop.db
```

**For Better Performance (Optional - PostgreSQL):**
```powershell
# Install PostgreSQL
choco install postgresql

# Create database
psql -U postgres
CREATE DATABASE cyber_sop;
CREATE USER cyberuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE cyber_sop TO cyberuser;
```

Update `backend.env`:
```dotenv
DATABASE_URL=postgresql://cyberuser:your_password@192.168.9.160:5432/cyber_sop
```

### 5. Start All Services

**Create a startup script: `start_server.ps1`**
```powershell
# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\Work's\Github\cyber-sop-assistant\backend; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment
Start-Sleep -Seconds 2

# Check if Ollama is running
$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
if (-not $ollamaProcess) {
    Write-Host "Starting Ollama..."
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
}

Write-Host "✅ Server started!"
Write-Host "Backend: http://192.168.9.160:8000"
Write-Host "Ollama: http://192.168.9.160:11434"
Write-Host "Docs: http://192.168.9.160:8000/api/docs"
```

Run it:
```powershell
.\start_server.ps1
```

---

## 👥 DEVELOPER SETUP (Other Team Members)

### Prerequisites
- Node.js 18+ and npm
- Git
- Network access to host system

### 1. Clone Repository

```bash
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant
```

### 2. Configure Frontend to Use Central Backend

**Create/Update: `frontend/.env.development`**
```env
# Backend API - Use Host's IP
VITE_API_BASE_URL=http://192.168.9.160:8000
VITE_API_VERSION=v1

# Optional: Ollama Direct Access (if needed for testing)
VITE_OLLAMA_URL=http://192.168.9.160:11434
```

**Create/Update: `frontend/.env`**
```env
VITE_API_BASE_URL=http://192.168.9.160:8000
VITE_API_VERSION=v1
```

### 3. Update API Client (if not using env vars)

**Edit: `frontend/src/lib/api/client.ts`**
```typescript
import axios from 'axios'

// Use environment variable or fallback to central backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://192.168.9.160:8000'

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

### 4. Install Dependencies & Run Frontend

```bash
cd frontend
npm install
npm run dev
```

**Frontend will be available at:**
- Local: `http://localhost:5173`
- Network: `http://YOUR_IP:5173`

### 5. Verify Connection to Central Backend

**Test API Connection:**
```bash
# Windows PowerShell
curl http://192.168.9.160:8000/health

# Linux/Mac
curl http://192.168.9.160:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### 6. Test Full Stack

1. Open browser: `http://localhost:5173`
2. Try anonymous chat - should connect to central backend
3. Upload evidence - files stored on central system
4. Check backend logs on host system

---

## 🔍 TROUBLESHOOTING

### Developers Can't Connect to Backend

**1. Check Host Firewall:**
```powershell
# On host system
Test-NetConnection -ComputerName 192.168.9.160 -Port 8000
```

**2. Verify Backend is Running:**
```powershell
# On host system
netstat -ano | findstr :8000
```

**3. Check Network Connectivity:**
```bash
# From developer's machine
ping 192.168.9.160
telnet 192.168.9.160 8000
```

**4. Check CORS Configuration:**
- Ensure developer's IP is in `ALLOWED_ORIGINS` in `backend.env`
- Or use wildcard `*` for development (not recommended for production)

### Ollama Connection Issues

**1. Verify Ollama is Running:**
```powershell
# On host system
curl http://localhost:11434/api/tags
```

**2. Check Ollama Network Binding:**
```powershell
# Should show 0.0.0.0:11434
netstat -ano | findstr :11434
```

**3. Test from Developer Machine:**
```bash
curl http://192.168.9.160:11434/api/tags
```

**4. Restart Ollama with Network Binding:**
```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

### Database Issues

**If using SQLite:**
- Ensure backend has write permissions to `data/` folder
- SQLite is file-based - developers access via backend API only
- No direct database access needed

**If using PostgreSQL:**
- Check PostgreSQL is listening on `0.0.0.0`
- Verify `pg_hba.conf` allows network connections
- Test connection: `psql -h 192.168.9.160 -U cyberuser -d cyber_sop`

### Frontend Can't Connect

**1. Check API Base URL:**
```bash
# In frontend terminal
echo $env:VITE_API_BASE_URL  # Windows
echo $VITE_API_BASE_URL       # Linux/Mac
```

**2. Clear Vite Cache:**
```bash
rm -rf node_modules/.vite
npm run dev
```

**3. Check Browser Console:**
- F12 → Network tab
- Look for CORS errors
- Check API request URLs

### Performance Issues

**1. Network Latency:**
- Use `ping` to check network latency
- Consider using wired connection for host
- Ensure host system has good network bandwidth

**2. Ollama Performance:**
- Check host system RAM (needs 8GB+ for Mistral 7B)
- Monitor CPU usage
- Consider smaller model if needed: `ollama pull mistral:7b-instruct-q4_0`

**3. Database Performance:**
- Switch from SQLite to PostgreSQL for better concurrent access
- Add database connection pooling
- Monitor backend logs for slow queries

---

## 📊 MONITORING

### Host System Monitoring

**Backend Health:**
```powershell
# Check backend status
curl http://192.168.9.160:8000/health

# View backend logs
cd backend
Get-Content -Path "data/logs/app.log" -Tail 50 -Wait
```

**Ollama Status:**
```powershell
# Check Ollama
curl http://192.168.9.160:11434/api/tags

# List running models
ollama ps
```

**System Resources:**
```powershell
# CPU and Memory
Get-Process | Where-Object {$_.ProcessName -match "python|ollama|uvicorn"} | Select-Object ProcessName, CPU, WorkingSet64

# Network connections
netstat -ano | findstr "8000 11434"
```

### Developer Activity

**Track API Requests:**
```powershell
# View access logs
cd backend
Get-Content -Path "data/logs/access.log" -Tail 50 -Wait
```

**Monitor Active Connections:**
```powershell
# Show connected clients
netstat -ano | findstr ESTABLISHED | findstr ":8000"
```

---

## 🔒 SECURITY CONSIDERATIONS

### Development Mode

✅ **Currently Enabled:**
- CORS wildcard (`*`) for easy development
- Debug mode enabled
- API docs accessible at `/api/docs`
- All endpoints accessible

⚠️ **For Production:**
- Update `ALLOWED_ORIGINS` to specific domains only
- Set `DEBUG=False` in backend.env
- Disable API docs
- Add authentication to all endpoints
- Use HTTPS with SSL certificates
- Implement rate limiting
- Add API keys for developers

### Network Security

**Current Setup (Development):**
- Backend accessible on local network only
- No external internet exposure
- Firewall rules limit access to specific ports

**Recommendations:**
1. Use VPN for remote developers
2. Implement API key authentication
3. Monitor access logs regularly
4. Keep all systems updated
5. Use strong passwords for database

---

## 📝 QUICK REFERENCE

### Host System (Your Machine)

**IP Address:** `192.168.9.160`

**Services:**
| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://192.168.9.160:8000 |
| API Docs | 8000 | http://192.168.9.160:8000/api/docs |
| Ollama LLM | 11434 | http://192.168.9.160:11434 |
| Frontend (optional) | 5173 | http://192.168.9.160:5173 |

**Start Commands:**
```powershell
# Backend
cd backend; venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ollama
$env:OLLAMA_HOST="0.0.0.0:11434"; ollama serve

# Frontend (optional)
cd frontend; npm run dev -- --host 0.0.0.0
```

### Developer Machines

**Environment Variables:**
```env
VITE_API_BASE_URL=http://192.168.9.160:8000
```

**Test Connection:**
```bash
curl http://192.168.9.160:8000/health
```

**Start Development:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🎯 SUMMARY

### What's Centralized:
✅ Backend API (FastAPI)  
✅ Database (SQLite/PostgreSQL)  
✅ Ollama LLM (Mistral 7B)  
✅ File Storage (Evidence files)  
✅ Vector Store (ChromaDB)

### What Developers Work On:
✅ Frontend development (React/TypeScript)  
✅ UI/UX improvements  
✅ New feature pages  
✅ Translation additions  
✅ Testing and debugging

### Network Flow:
```
Developer Machine → Frontend (localhost:5173)
                  ↓
                  Backend API (192.168.9.160:8000)
                  ↓
                  ├── Database (SQLite)
                  ├── Ollama LLM (192.168.9.160:11434)
                  └── Vector Store (ChromaDB)
```

---

## 🚀 NEXT STEPS

1. ✅ Start backend on host system
2. ✅ Configure Ollama for network access
3. ✅ Set firewall rules
4. ✅ Share IP address with developers
5. ✅ Developers update their `.env` files
6. ✅ Test connection from developer machines
7. ✅ Start developing!

**Status:** ✅ Ready for team collaboration!

**Last Updated:** December 13, 2025
