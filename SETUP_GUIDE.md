# Complete Windows Setup Guide for Cyber-SOP Assistant

## 📋 Step-by-Step Setup (Windows 10/11)

### Step 1: Install Prerequisites

#### 1.1 Install Python 3.10+
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation:
```powershell
python --version
# Should show: Python 3.10.x or higher
```

#### 1.2 Install Node.js 18+
1. Download from: https://nodejs.org/ (LTS version)
2. Install with default options
3. Verify installation:
```powershell
node --version
# Should show: v18.x.x or higher

npm --version
# Should show: 9.x.x or higher
```

#### 1.3 Install Ollama
1. Download from: https://ollama.ai/download/windows
2. Install Ollama
3. Open PowerShell and download the AI model:
```powershell
ollama pull mistral:instruct
```
4. Verify Ollama is working:
```powershell
ollama list
# Should show mistral:instruct in the list
```

---

### Step 2: Setup Backend

1. **Open PowerShell** in the project root directory

2. **Navigate to backend**:
```powershell
cd backend
```

3. **Create virtual environment**:
```powershell
python -m venv venv
```

4. **Activate virtual environment**:
```powershell
.\venv\Scripts\activate
```
You should see `(venv)` in your prompt

5. **Upgrade pip**:
```powershell
python -m pip install --upgrade pip
```

6. **Install dependencies**:
```powershell
pip install -r requirements.txt
```
This will take 5-10 minutes. Wait for it to complete.

7. **Create .env file**:
```powershell
copy .env.example .env
```

8. **Initialize database**:
```powershell
python scripts\init_db.py
```
You should see: "✅ Database initialization complete!"

---

### Step 3: Setup Frontend

1. **Open a NEW PowerShell window** (keep backend window open)

2. **Navigate to frontend**:
```powershell
cd frontend
```

3. **Install dependencies**:
```powershell
npm install
```
This will take 3-5 minutes.

4. **Create .env file**:
```powershell
copy .env.example .env
```

---

### Step 4: Start the Application

#### Option A: Use Convenient Scripts (Recommended)

1. **Double-click**: `scripts\setup.cmd` (First time only)
   - This sets up everything automatically

2. **Double-click**: `scripts\start_all.cmd`
   - This starts both backend and frontend

#### Option B: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

---

### Step 5: Access the Application

1. **Open your browser** to: http://localhost:5173
2. **API Documentation**: http://localhost:8000/docs
3. **Health Check**: http://localhost:8000/api/health

---

## ✅ Verification Checklist

### Backend Verification

1. **Check if backend is running**:
```powershell
curl http://localhost:8000/
```
Should return: `{"message":"Cyber-SOP Assistant API","version":"1.0.0"...}`

2. **Check health status**:
```powershell
curl http://localhost:8000/api/health
```
Should show all services as "healthy"

3. **Check resources**:
```powershell
curl http://localhost:8000/api/resources/
```
Should return list of resources (NCRP, CEIR, etc.)

4. **Check Ollama connection**:
```powershell
curl http://localhost:11434/api/tags
```
Should show list of available models

### Frontend Verification

1. Open http://localhost:5173
2. You should see:
   - Left sidebar with "Cyber SOP Assistant" logo
   - Chat interface in the center
   - "Ask anything about cybercrime..." input box

3. Try sending a message:
   - Type: "How to report cybercrime?"
   - Press Enter or click Send
   - You should get a response from the AI

---

## 🎯 Testing the Complete Flow

### Test 1: Chat Functionality
```
1. Open http://localhost:5173
2. Type: "What is NCRP?"
3. Press Enter
4. You should get an AI response about National Cyber Crime Reporting Portal
```

### Test 2: Resources Section
```
1. Click "Resources" in the sidebar
2. You should see links to:
   - NCRP
   - CEIR
   - TAFCOP
   - CERT-In
   - etc.
```

### Test 3: Police Locator
```
1. Click "Near By Police" in sidebar
2. Select a state (e.g., "Delhi")
3. Click Search
4. You should see list of police stations
```

### Test 4: API Documentation
```
1. Click "API Documentation" in sidebar
2. Opens http://localhost:8000/docs
3. You can test API endpoints directly
```

---

## 🔧 Common Issues and Solutions

### Issue 1: "Python is not recognized"

**Solution:**
1. Reinstall Python
2. **Check "Add Python to PATH"** during installation
3. Restart PowerShell

### Issue 2: "Cannot activate virtual environment"

**Solution:**
```powershell
# Try this alternative activation:
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 3: "npm is not recognized"

**Solution:**
1. Reinstall Node.js
2. Restart PowerShell
3. Verify: `node --version`

### Issue 4: "Cannot connect to Ollama"

**Solution:**
```powershell
# Check if Ollama is running:
ollama list

# If not working, restart Ollama:
# Open Ollama application from Start Menu
# Or run in terminal:
ollama serve
```

### Issue 5: "Port 8000 is already in use"

**Solution:**
```powershell
# Find and kill the process:
netstat -ano | findstr :8000
# Note the PID, then:
taskkill /PID <PID_NUMBER> /F
```

### Issue 6: "Module not found" errors

**Solution:**
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

### Issue 7: Empty AI responses

**Solution:**
This means no documents are indexed yet. The system will work but won't have specific cybercrime knowledge.

To add documents:
1. Use the API at http://localhost:8000/docs
2. POST to `/api/admin/documents`
3. Or create a Python script (see QUICKSTART.md)

---

## 📊 System Requirements

### Minimum:
- Windows 10/11
- 8GB RAM
- 10GB free disk space
- Quad-core processor

### Recommended:
- Windows 11
- 16GB RAM
- 20GB free disk space
- 8-core processor
- SSD storage

---

## 🎨 Customization

### Change Theme Colors

Edit `frontend\src\index.css`:

```css
:root {
  --bg-primary: #0f0f0f;        /* Main background */
  --bg-secondary: #171717;      /* Sidebar background */
  --accent-color: #2ea043;      /* Primary accent */
  --text-primary: #ececec;      /* Main text */
}
```

### Change LLM Model

Edit `backend\.env`:

```env
LLM_MODEL=mistral:instruct
# Or try: llama2, codellama, etc.
```

Download new model:
```powershell
ollama pull llama2
```

### Add More Resources

1. Go to http://localhost:8000/docs
2. Find `POST /api/resources/`
3. Click "Try it out"
4. Add your JSON:
```json
{
  "name": "My Resource",
  "url": "https://example.com",
  "category": "Custom",
  "description": "Description here",
  "icon": "🔗",
  "order": 10
}
```

---

## 📝 Development Workflow

### Making Changes

1. **Backend changes**:
   - Edit Python files in `backend/app/`
   - Server auto-reloads (if running with `--reload`)
   - Check logs in terminal

2. **Frontend changes**:
   - Edit TypeScript/React files in `frontend/src/`
   - Browser auto-refreshes (Hot Module Replacement)
   - Check browser console (F12)

### Database Changes

If you modify models in `backend/app/models.py`:

```powershell
cd backend
.\venv\Scripts\activate

# Delete old database
rm cyber_sop.db
rm -r ..\data\chroma_store

# Reinitialize
python scripts\init_db.py
```

---

## 🚀 Next Steps

1. ✅ Complete setup
2. ✅ Test all features
3. 📝 Add your own cybercrime documents (see QUICKSTART.md)
4. 🎨 Customize the UI
5. 🧪 Test with different queries
6. 📊 Monitor system stats at http://localhost:8000/api/admin/stats

---

## 🆘 Getting Help

If you're stuck:

1. Check this guide's "Common Issues" section
2. Check QUICKSTART.md for detailed examples
3. Check logs in both terminal windows
4. Visit http://localhost:8000/api/health to see system status
5. Check backend logs for error messages

---

## 📚 Additional Resources

- **Ollama Models**: https://ollama.ai/library
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **ChromaDB Docs**: https://docs.trychroma.com/

---

**You're all set! Happy coding! 🎉**

For quick reference, keep this checklist handy:

```
☐ Python 3.10+ installed
☐ Node.js 18+ installed  
☐ Ollama installed with mistral:instruct
☐ Backend venv created and activated
☐ Backend dependencies installed (pip install -r requirements.txt)
☐ Backend .env created
☐ Database initialized (python scripts\init_db.py)
☐ Frontend dependencies installed (npm install)
☐ Frontend .env created
☐ Both servers running
☐ Can access http://localhost:5173
☐ Can send chat messages
☐ AI responds correctly
```
