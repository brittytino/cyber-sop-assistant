# 🛡️ Cyber SOP Assistant

**AI-Driven Cybercrime Reporting Guidance System for India**

> *Bridging the gap between citizens and India's fragmented cybercrime reporting infrastructure through accurate, step-by-step guidance based on official government SOPs*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)

---

## 🎯 Problem Statement

**The Challenge:**
India faces a critical gap in cybercrime awareness and reporting. Citizens struggle with:
- **Fragmented reporting infrastructure** across multiple platforms (cybercrime.gov.in, 1930 helpline, platform-specific portals)
- **Complex procedures** varying by crime type (financial fraud, social media hacking, sextortion, phishing)
- **Lack of step-by-step guidance** aligned with official government SOPs
- **Language barriers** preventing access to help in native languages
- **Time-sensitive situations** where immediate action is critical (SIM swap fraud, financial fraud)

**The Solution:**
An AI-powered assistant that provides:
✅ **Instant, accurate guidance** based on official government procedures  
✅ **Crime-specific SOPs** from cybercrime.gov.in, CERT-In, RBI, MeitY guidelines  
✅ **Step-by-step reporting** for National Cybercrime Portal, 1930 helpline, platform-specific processes  
✅ **Multi-language support** (8 Indian languages)  
✅ **Evidence collection checklists** to strengthen complaints  
✅ **Platform-specific reporting** (Facebook, Instagram, WhatsApp, banking apps, UPI)  
✅ **Emergency response protocols** for time-critical situations  

---

## ✨ Features & Enhancements

### **🚀 Production-Level Features**

#### **1. Advanced Crime Classification (30+ Types)**
- **Financial Fraud:** UPI scams, Internet banking fraud, Credit/Debit card fraud, Cryptocurrency fraud, Investment scams, Online shopping fraud, Fake payment requests, ATM fraud, Wallet fraud, Loan app fraud
- **Social Media Crimes:** Account hacking, Identity theft, Fake profiles, Cyberbullying, Impersonation, Morphed images, Social media fraud
- **Women/Child Safety:** Sextortion, Online blackmail, Cyberstalking, Child abuse material (CSAM), Online harassment, Revenge porn
- **Cyber Attacks:** Phishing (Email/SMS/Call), Ransomware, Malware, DDoS attacks, Website defacement, Data breach
- **Others:** SIM swap fraud, Online job fraud, Fake apps, Lottery scams, Matrimonial fraud, OTP fraud, Domain fraud, Email hacking

#### **2. Multi-Language Support (8 Languages)** 🌍
- **Supported Languages:** English, Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Bengali (বাংলা), Marathi (मराठी), Gujarati (ગુજરાતી), Kannada (ಕನ್ನಡ)
- **Two-Layer Translation System:**
  - **Static UI:** Translated using i18next (navigation, buttons, forms)
  - **Dynamic AI Content:** Translated using OpenRouter AI models
- **9 Free AI Models** for translation (Llama 3.3, Gemma 3, DeepSeek, etc.)
- **Language-aware chat** - AI responds in user's selected language
- **RAG + Translation** - Local Ollama generates content, OpenRouter translates
- **See [MULTILINGUAL_GUIDE.md](MULTILINGUAL_GUIDE.md) for details**

#### **3. Multi-Intent Detection**
- Detects multiple crime types in a single query
- Example: "My Instagram was hacked and the hacker is doing financial fraud"
- Provides comprehensive response covering all detected intents

#### **4. Official Links Database**
- **100% verified .gov.in and official portal links**
- Cybercrime helplines (National: 1930, Women: 181, Child: 1098)
- Banking fraud contacts (All major banks)
- Telecom operators (Airtel, Jio, Vi, BSNL)
- State-wise cyber cells (All 36 states/UTs)
- Platform support (Meta, Google, Twitter/X, WhatsApp)

#### **5. Timeline-Based SOP Templates**
- **NOW (Immediate 0-5 minutes):** Critical safety actions
- **24 HOURS:** Urgent reporting steps
- **7 DAYS:** Follow-up and evidence collection
- **ONGOING:** Long-term security measures
- Dynamic action items with severity levels (CRITICAL, HIGH, MEDIUM, LOW)

#### **6. Enhanced Query Processing**
- Smart query understanding with context awareness
- Fallback handling for unknown queries
- Comprehensive response structure with:
  - Detected language
  - Identified crime types
  - Step-by-step actions
  - Official contacts
  - Evidence requirements
  - Legal provisions

---

## 🏗️ Core Technical Architecture

### **Primary Data Sources**

The LLM is trained/fine-tuned on official government SOPs from:

1. **National Cybercrime Reporting Portal** (cybercrime.gov.in)
   - Main complaint filing system for all cybercrimes
   - Separate pathways for Women/Child crimes and Other cybercrimes

2. **CERT-In** (Indian Computer Emergency Response Team)
   - 6-hour mandatory incident reporting requirements
   - Critical infrastructure protection advisories

3. **Ministry of Electronics and IT (MeitY)**
   - IT Rules 2021 for intermediary obligations
   - Content reporting and takedown procedures

4. **Reserve Bank of India (RBI)**
   - Cyber Security Framework for financial institutions
   - Banking fraud protocols and reporting

5. **Citizen Financial Cyber Fraud Reporting System**
   - 1930 helpline workflows for urgent financial fraud
   - Inter-bank fund freezing coordination

6. **Platform-Specific Mechanisms**
   - Social media grievance categories (Facebook: 13, Instagram: 12, Twitter/X: 13, WhatsApp, YouTube: 9)
   - UPI/NPCI complaint escalation procedures
   - Telecom SIM-swap fraud reporting

### **Response Template Structure**

Every AI response follows this universal SOP template:

1. **Immediate Safety Actions** (First 5 minutes)
2. **Emergency Helpline** (1930 for financial crimes)
3. **National Cybercrime Portal Reporting** (Step-by-step)
4. **Evidence Collection Checklist**
5. **Platform-Specific Reporting** (When applicable)
6. **Financial Recovery Steps** (For monetary loss)
7. **Security Hardening** (Post-incident protection)
8. **CERT-In Reporting** (For organizations/critical incidents)
9. **Escalation & Follow-up** (If unresolved)

---

## 📋 Prerequisites

### **System Requirements**
- **OS**: Windows 10/11 (64-bit) | macOS 10.15+ | Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- **RAM**: 16GB minimum (recommended for Mistral 7B model)
- **Storage**: 20GB free disk space
- **Internet**: Required for initial setup only (offline operation after setup)

### **Software Requirements**
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 20.x LTS** - [Download](https://nodejs.org/)
- **Ollama** (Local LLM runtime) - [Download](https://ollama.com/download)
- **Git** (for cloning repository)

---

## 🚀 Quick Start (3 Simple Steps)

> ⚠️ **IMPORTANT PATH REQUIREMENT**
> 
> Python packages fail to compile when the project path contains **special characters like apostrophes**.
> 
> **If your path looks like this:** `D:\Work's\Github\cyber-sop-assistant` ❌
> 
> **Move it to:** `D:\Works\Github\cyber-sop-assistant` ✅
> 
> ```powershell
> # Quick fix:
> # 1. Close all terminals
> # 2. Rename "Work's" folder to "Works"
> # 3. Navigate to new path and run QUICK_START.bat
> ```

---

### **🪟 Windows Users**

```powershell
# 1. Clone the repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# 2. Run the launcher script
.\QUICK_START.bat
```

**That's it!** The script will:
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies (Python packages)
- ✅ Install all frontend dependencies (npm packages)
- ✅ Start Backend server → http://localhost:8000
- ✅ Start Frontend dev server → http://localhost:5173
- ✅ Open in separate labeled terminal windows

**First-time setup:** 5-10 minutes (downloads all dependencies)  
**Subsequent starts:** Instant! (Just launches the services)

**Access the application:** http://localhost:5173

---

### **🐧 Linux/macOS Users**

```bash
# 1. Clone the repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# 2. Install dependencies and start
chmod +x scripts/setup/*.sh
./scripts/setup/00_install_dependencies.sh

# 3. Start services (3 terminals)
# Terminal 1: Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2: Frontend  
cd frontend && npm run dev
```

---

## 🚀 Quick Start (Automated Setup)

### **Option 1: Automated Setup (Recommended)**

<details open>
<summary><b>Windows</b></summary>

1. **Clone the repository:**
```powershell
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant
```

2. **Run automated setup:**
```powershell
.\setup.bat
```

3. **Start all services:**
```powershell
.\START.bat
```

This opens 3 terminal windows:
- **Ollama Service** (http://localhost:11434)
- **Backend API** (http://localhost:8000)
- **Frontend** (http://localhost:5173)

4. **Access the application:**
Open browser → **http://localhost:5173**

</details>

<details>
<summary><b>Linux/macOS</b></summary>

1. **Clone the repository:**
```bash
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant
```

2. **Run automated setup:**
```bash
chmod +x scripts/setup/*.sh
./scripts/setup/00_install_dependencies.sh
./scripts/setup/01_setup_ollama.sh
./scripts/setup/02_download_models.sh
./scripts/setup/03_initialize_db.sh
```

3. **Start all services (3 separate terminals):**

**Terminal 1 - Ollama:**
```bash
./scripts/deployment/start_ollama.sh
```

**Terminal 2 - Backend:**
```bash
./scripts/deployment/start_backend.sh
```

**Terminal 3 - Frontend:**
```bash
./scripts/deployment/start_frontend.sh
```

**Or use tmux/screen for single terminal:**
```bash
# Install tmux (if not installed)
sudo apt install tmux  # Ubuntu/Debian
sudo yum install tmux  # CentOS/RHEL

# Start all services
tmux new-session -d -s ollama './scripts/deployment/start_ollama.sh'
tmux new-session -d -s backend './scripts/deployment/start_backend.sh'
tmux new-session -d -s frontend './scripts/deployment/start_frontend.sh'

# View logs
tmux attach -t backend  # Press Ctrl+B, then D to detach
```

4. **Access the application:**
Open browser → **http://localhost:5173**

</details>

**The automated setup will:**
- ✅ Check all prerequisites (Python, Node.js, Ollama)
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies (FastAPI, ChromaDB, etc.)
- ✅ Install all frontend dependencies (React, TypeScript, Tailwind)
- ✅ Download Ollama Mistral 7B model (4GB, ~10-15 minutes)
- ✅ Download sentence-transformers embedding model (90MB)
- ✅ Initialize SQLite database with tables
- ✅ Populate vector database with 7 comprehensive SOP documents
- ✅ Create all necessary directories (data/, models/, logs/)

---

### **Option 2: Manual Setup**

<details>
<summary>Click to expand manual installation steps</summary>

#### **Step 1: Install Prerequisites**

<details>
<summary><b>Windows</b></summary>

**1.1 Python 3.11+**
```powershell
# Download from: https://www.python.org/downloads/
# ✅ IMPORTANT: Check "Add Python to PATH" during installation

# Verify:
python --version  # Should show Python 3.11.x or higher
```

**1.2 Node.js 20.x LTS**
```powershell
# Download from: https://nodejs.org/

# Verify:
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x
```

**1.3 Ollama**
```powershell
# Download from: https://ollama.com/download

# Verify:
ollama --version

# Download Mistral 7B model (~4GB, 10-15 minutes):
ollama pull mistral:7b-instruct

# Verify model:
ollama list  # Should show mistral:7b-instruct
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

**1.1 Python 3.11+**
```bash
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# macOS (with Homebrew):
brew install python@3.11

# Verify:
python3 --version  # Should show Python 3.11.x or higher
```

**1.2 Node.js 20.x LTS**
```bash
# Ubuntu/Debian (using NodeSource):
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS (with Homebrew):
brew install node@20

# Verify:
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x
```

**1.3 Ollama**
```bash
# Linux:
curl -fsSL https://ollama.com/install.sh | sh

# macOS:
brew install ollama

# Verify:
ollama --version

# Download Mistral 7B model (~4GB, 10-15 minutes):
ollama pull mistral:7b-instruct

# Verify model:
ollama list  # Should show mistral:7b-instruct
```

</details>

#### **Step 2: Clone Repository**

<details>
<summary><b>Windows</b></summary>

```powershell
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant
```

</details>

#### **Step 3: Backend Setup**

<details>
<summary><b>Windows</b></summary>

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # PowerShell
# OR
venv\Scripts\activate.bat  # CMD

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (5-10 minutes)
pip install -r requirements.txt

# Create necessary directories
New-Item -ItemType Directory -Force -Path data\vectorstore, data\cache, data\logs, data\processed, data\raw, models\embeddings

# Initialize database and download embedding model
python scripts\init_setup.py

# Populate vector database with SOP documents
python scripts\populate_data.py
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (5-10 minutes)
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/{vectorstore,cache,logs,processed,raw} models/embeddings

# Initialize database and download embedding model
python scripts/init_setup.py

# Populate vector database with SOP documents
python scripts/populate_data.py
```

</details>

#### **Step 4: Frontend Setup**

<details>
<summary><b>Windows</b></summary>

```powershell
cd ..\frontend

# Install dependencies (5-10 minutes)
npm install
# If errors occur, try:
# npm install --legacy-peer-deps
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
cd ../frontend

# Install dependencies (5-10 minutes)
npm install
# If errors occur, try:
# npm install --legacy-peer-deps
```

</details>

#### **Step 5: Start Services (3 separate terminals)**

<details>
<summary><b>Windows</b></summary>

**Terminal 1 - Ollama:**
```powershell
ollama serve
```

**Terminal 2 - Backend:**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 - Frontend:**
```powershell
cd frontend
npm run dev
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

**Or use tmux/screen:**
```bash
# Install tmux
sudo apt install tmux  # Ubuntu/Debian
sudo yum install tmux  # CentOS/RHEL
brew install tmux      # macOS

# Start all services
tmux new-session -d -s ollama 'ollama serve'
tmux new-session -d -s backend 'cd backend && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload'
tmux new-session -d -s frontend 'cd frontend && npm run dev'

# View logs
tmux attach -t backend  # Ctrl+B, D to detach
tmux ls                 # List sessions
tmux kill-session -t backend  # Kill a session
```

</details>

</details>

---

## 🌐 Access the Application

**Main Application:** http://localhost:5173

**API Documentation:** http://localhost:8000/api/docs (Swagger UI)

**Health Check:** http://localhost:8000/api/v1/health

---

## 🧪 Testing the System

Try these sample queries to verify the AI assistant is working:

### **Financial Fraud:**
- *"I lost ₹50,000 in a UPI scam. Someone sent me a fake payment request and I approved it by mistake. What should I do?"*
- *"I received a call saying my account will be blocked. They asked for my OTP and withdrew money. How do I report this?"*
- *"Someone hacked my credit card and made unauthorized transactions. Help!"*

### **Social Media Hacking:**
- *"My Instagram account was hacked. I can't log in anymore. How do I recover it?"*
- *"Someone hacked my Facebook and is posting from my account. Help!"*
- *"Someone created a fake profile using my photos"*

### **Sextortion/Blackmail:**
- *"Someone is threatening to share my private photos unless I pay money. What should I do?"*

### **Phishing:**
- *"I clicked a link in an SMS saying my KYC needs update. Did I get scammed?"*

### **Job Fraud:**
- *"I paid ₹5000 for a work-from-home job but they're asking for more money. Is this a scam?"*

### **SIM Swap:**
- *"My phone suddenly shows 'No Service' and I'm getting bank transaction alerts. What's happening?"*

### **Multi-Intent (Advanced):**
- *"My Instagram was hacked and the hacker is doing financial fraud from my account"*
- *"मेरा WhatsApp हैक हो गया और वो मेरे दोस्तों से पैसे मांग रहे हैं"* (Hindi)

**Expected Response:**
- ✅ Detected language and crime type(s)
- ✅ Immediate safety actions (NOW section)
- ✅ Step-by-step cybercrime portal reporting
- ✅ 1930 helpline instructions (for financial crimes)
- ✅ Evidence collection checklist
- ✅ Platform-specific reporting steps
- ✅ Official contacts and links
- ✅ Legal provisions and follow-up actions

---

## 📁 Project Structure

```
cyber-sop-assistant/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   └── v1/           # API v1 routes
│   │   │       └── endpoints/ # Chat, admin, complaints
│   │   ├── core/             # Core configuration
│   │   │   ├── crime_types.py        # 30+ crime classification
│   │   │   ├── official_links.py     # Verified .gov.in links
│   │   │   ├── sop_templates.py      # Timeline-based SOPs
│   │   │   └── config.py             # Settings
│   │   ├── db/               # Database
│   │   │   ├── database.py           # SQLite/PostgreSQL
│   │   │   └── session.py            # Session management
│   │   ├── models/           # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── enhanced_query_service.py  # Multi-intent detection
│   │   │   ├── rag_service.py             # Vector search
│   │   │   ├── llm_service.py             # Ollama integration
│   │   │   └── embedding_service.py       # Sentence transformers
│   │   ├── middleware/       # Custom middleware
│   │   │   ├── logging.py            # Request logging
│   │   │   └── error_handler.py      # Error handling
│   │   └── utils/           # Helper functions
│   ├── data/                # Generated data
│   │   ├── vectorstore/     # ChromaDB storage
│   │   ├── cache/          # Response cache
│   │   ├── logs/           # Application logs
│   │   └── processed/      # Processed SOP data
│   ├── models/              # ML models
│   │   └── embeddings/     # Sentence transformer models
│   ├── scripts/             # Setup scripts
│   │   ├── init_setup.py    # Initialize DB & models
│   │   └── populate_data.py # Populate vector DB
│   ├── tests/               # Test suite
│   │   ├── unit/           # Unit tests
│   │   ├── integration/    # Integration tests
│   │   └── e2e/           # End-to-end tests
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── LanguageSelector.tsx
│   │   │   └── EmergencyButton.tsx
│   │   ├── features/        # Feature modules
│   │   ├── context/         # State management
│   │   ├── hooks/           # Custom hooks
│   │   ├── lib/            # Utilities
│   │   └── styles/         # Tailwind styles
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
│
├── scripts/               # Project scripts
│   ├── setup/            # Setup automation
│   │   ├── 00_install_dependencies.sh
│   │   ├── 01_setup_ollama.sh
│   │   ├── 02_download_models.sh
│   │   └── 03_initialize_db.sh
│   └── deployment/       # Deployment scripts
│       ├── start_ollama.sh
│       ├── start_backend.sh
│       ├── start_frontend.sh
│       └── stop_all.sh
│
├── config/               # Configuration files
│   ├── development/     # Dev environment
│   ├── production/      # Prod environment
│   └── test/           # Test environment
│
├── setup.bat            # Windows automated setup
├── START.bat            # Windows start all services
├── README.md            # This file
├── LICENSE              # MIT License
├── SECURITY.md          # Security policy
└── CODE_OF_CONDUCT.md   # Contributor guidelines
```

---

## 🛠️ For Contributors & Developers

### **Daily Development Workflow**

<details>
<summary><b>Windows</b></summary>

```powershell
# 1. Pull latest changes
git pull origin main

# 2. Start all services
.\START.bat  # Opens 3 terminal windows

# 3. Make changes and test

# 4. Run tests
cd backend
.\venv\Scripts\activate
pytest tests/ -v --cov=app

# 5. Commit and push
git add .
git commit -m "feat: your feature description"
git push origin your-branch-name
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
# 1. Pull latest changes
git pull origin main

# 2. Start all services (3 terminals or tmux)
# Terminal 1: ollama serve
# Terminal 2: cd backend && source venv/bin/activate && uvicorn app.main:app --reload
# Terminal 3: cd frontend && npm run dev

# 3. Make changes and test

# 4. Run tests
cd backend
source venv/bin/activate
pytest tests/ -v --cov=app

# 5. Commit and push
git add .
git commit -m "feat: your feature description"
git push origin your-branch-name
```

</details>

### **Running Tests**

<details>
<summary><b>Windows</b></summary>

```powershell
# Backend tests
cd backend
.\venv\Scripts\activate
pytest tests/ -v                    # All tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests
pytest tests/ -v --cov=app          # With coverage

# Frontend tests
cd frontend
npm test                            # Run tests
npm run test:coverage               # With coverage
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/ -v                    # All tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests
pytest tests/ -v --cov=app          # With coverage

# Frontend tests
cd frontend
npm test                            # Run tests
npm run test:coverage               # With coverage
```

</details>

### **Git Commit Conventions**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, missing semicolons, etc.
- `refactor:` Code restructure without changing behavior
- `test:` Adding or updating tests
- `chore:` Dependencies, config, build scripts

---

## 🐛 Troubleshooting

### **Common Issues (Cross-Platform)**

<details>
<summary><b>"Ollama not running" Error</b></summary>

**Windows:**
```powershell
# Start Ollama service
ollama serve

# Verify model exists
ollama list

# If model missing, download it:
ollama pull mistral:7b-instruct
```

**Linux/macOS:**
```bash
# Start Ollama service
ollama serve

# Verify model exists
ollama list

# If model missing, download it:
ollama pull mistral:7b-instruct
```

</details>

<details>
<summary><b>"Port Already in Use" Error</b></summary>

**Windows:**
```powershell
# Find and kill process on port 8000 (Backend)
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Find and kill process on port 5173 (Frontend)
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F

# Find and kill process on port 11434 (Ollama)
netstat -ano | findstr :11434
taskkill /PID <PID_NUMBER> /F
```

**Linux/macOS:**
```bash
# Find and kill process on port 8000 (Backend)
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 5173 (Frontend)
lsof -ti:5173 | xargs kill -9

# Find and kill process on port 11434 (Ollama)
lsof -ti:11434 | xargs kill -9
```

</details>

<details>
<summary><b>"Module Not Found" (Backend)</b></summary>

**Windows:**
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

**Linux/macOS:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

</details>

<details>
<summary><b>"Module Not Found" (Frontend)</b></summary>

**Windows:**
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

**Linux/macOS:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

</details>

<details>
<summary><b>"ChromaDB Not Initialized" Error</b></summary>

**Windows:**
```powershell
cd backend
.\venv\Scripts\activate
python scripts\init_setup.py
python scripts\populate_data.py
```

**Linux/macOS:**
```bash
cd backend
source venv/bin/activate
python scripts/init_setup.py
python scripts/populate_data.py
```

</details>

<details>
<summary><b>Slow LLM Response</b></summary>

- Ensure 16GB+ RAM available
- Close memory-intensive applications
- Mistral 7B requires ~8GB RAM for inference
- First query is always slower (model loading)
- Subsequent queries should be faster (2-5 seconds)

</details>

<details>
<summary><b>Python Version Issues</b></summary>

**Windows:**
```powershell
# If you have multiple Python versions:
py -3.11 -m venv venv  # Use specific version
```

**Linux/macOS:**
```bash
# If you have multiple Python versions:
python3.11 -m venv venv  # Use specific version
```

</details>

---

## 🔒 Security Considerations

### **Development Environment**
- ⚠️ `.env` files are gitignored - never commit them
- ⚠️ Default `SECRET_KEY` is insecure - change for production
- ⚠️ Debug mode enabled - disable in production
- ⚠️ CORS allows all origins - restrict in production

### **Production Environment**
- ✅ Change `SECRET_KEY` to strong random value (use `openssl rand -hex 32`)
- ✅ Set `DEBUG=false` in environment variables
- ✅ Configure specific `ALLOWED_ORIGINS` (frontend domain only)
- ✅ Enable HTTPS/TLS with valid SSL certificates
- ✅ Use PostgreSQL instead of SQLite for production
- ✅ Implement proper authentication (JWT, OAuth2)
- ✅ Rate limiting on API endpoints
- ✅ Regular security updates and dependency patching
- ✅ Set up proper logging and monitoring

### **Data Privacy**
- ✅ All processing is **100% local** - no external API calls
- ✅ No user data sent to third parties
- ✅ Conversations stored locally in browser (clearable)
- ✅ Vector database is local (ChromaDB)
- ✅ LLM inference is local (Ollama/Mistral)
- ✅ No tracking, analytics, or telemetry
- ✅ Fully compliant with data protection regulations

### **Security Reporting**
Please report security vulnerabilities to: security@yourproject.com  
See [SECURITY.md](SECURITY.md) for details.

---

## 📚 Technology Stack

### **Backend**
- **Framework:** FastAPI 0.124.0 (async, high-performance)
- **LLM:** Ollama (Mistral 7B Instruct, 7B parameters)
- **Vector DB:** ChromaDB 1.3.5 (similarity search)
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2 (384-dim, multilingual)
- **Database:** SQLite (aiosqlite) / PostgreSQL (production)
- **Language:** Python 3.11+ (type hints, async/await)
- **ORM:** SQLAlchemy 2.0 (async)
- **Validation:** Pydantic v2
- **HTTP Client:** httpx (async)
- **Testing:** pytest, pytest-cov, pytest-asyncio

### **Frontend**
- **Framework:** React 18.3.1 + TypeScript 5.2
- **Build Tool:** Vite 5.0 (fast HMR, optimized builds)
- **Styling:** Tailwind CSS 3.4 (utility-first)
- **UI Components:** shadcn/ui (headless, accessible)
- **State Management:** Zustand 4.4 (lightweight)
- **HTTP Client:** Axios 1.6 (REST API calls)
- **Icons:** Lucide React
- **Testing:** Vitest, React Testing Library

### **AI/ML Pipeline**
- **RAG Workflow:** User Query → Embedding → Vector Search (ChromaDB) → Context Retrieval → LLM Generation
- **Embedding Model:** all-MiniLM-L6-v2 (384-dimensional, multilingual, sentence similarity)
- **LLM:** Mistral 7B Instruct (7 billion parameters, instruction-tuned, context window: 8K tokens)
- **Vector Search:** Cosine similarity search with top-k retrieval (k=5)
- **Response Caching:** In-memory + SQLite cache for faster responses

### **DevOps & Tools**
- **Version Control:** Git + GitHub
- **Package Management:** pip (Python), npm (Node.js)
- **Containerization:** Docker + Docker Compose (optional)
- **CI/CD:** GitHub Actions (optional)
- **Linting:** pylint, black (Python), ESLint, Prettier (TypeScript)
- **API Documentation:** Swagger UI (FastAPI auto-generated)

---

## 🛠️ Troubleshooting

### **Common Issues & Solutions**

#### ❌ **Error: "numpy compilation failed" or "Malformed value in machine file"**

**Cause:** Your project path contains special characters (like apostrophes `'`) that break Python package compilation.

**Solution:**
```powershell
# Option 1: Use the special fix script (tries pre-built wheels only)
.\START_APP_FIX.bat

# Option 2: Move project to a path without special characters (Recommended)
# From:  D:\Work's\Github\cyber-sop-assistant
# To:    D:\Works\Github\cyber-sop-assistant

# Steps to move:
# 1. Close all terminals and VS Code
# 2. Rename folder: Work's -> Works
# 3. Navigate to new path and run START_APP.bat
```

---

#### ❌ **Error: "uvicorn: command not found" or "not recognized"**

**Cause:** Virtual environment not activated or dependencies not installed.

**Solution:**
```powershell
# Windows - Run from backend/ directory
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

#### ❌ **Error: "Port 8000 already in use"**

**Cause:** Another process is using port 8000 (previous instance still running).

**Solution:**
```powershell
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use alternative port
uvicorn app.main:app --reload --port 8001

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

---

#### ❌ **Error: "OpenRouter API returns 401 Unauthorized"**

**Cause:** Missing or invalid OpenRouter API key.

**Solution:**
```powershell
# 1. Get free API key from https://openrouter.ai/keys
# 2. Add to backend/.env or backend/config/development/backend.env:
OPENROUTER_API_KEY=your_actual_key_here

# 3. Restart backend
```

---

#### ❌ **Frontend shows "Failed to fetch" or "Network Error"**

**Cause:** Backend is not running or CORS misconfigured.

**Solution:**
```powershell
# 1. Verify backend is running
# Open: http://localhost:8000/api/v1/health

# 2. Check backend terminal for errors

# 3. Verify frontend API_URL in vite.config.ts
# Should be: http://localhost:8000
```

---

#### ❌ **Ollama models not found**

**Cause:** Ollama not installed or models not downloaded.

**Solution:**
```powershell
# 1. Install Ollama from https://ollama.ai

# 2. Pull required model
ollama pull mistral

# 3. Verify model is available
ollama list

# 4. Restart backend
```

---

#### ❌ **Language switching doesn't work**

**Cause:** i18next not initialized properly or translation files missing.

**Solution:**
```powershell
# 1. Verify translation files exist
ls frontend/src/locales/*/translation.json

# 2. Check browser console for errors (F12)

# 3. Clear browser cache and reload
# Or hard reload: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)

# 4. Verify i18n is imported in main.tsx
```

---

#### ❌ **Virtual environment activation fails**

**Cause:** Execution policy restriction (Windows).

**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single command
powershell -ExecutionPolicy Bypass -File START_APP.bat
```

---

#### ❌ **Dependencies install very slowly**

**Cause:** Large packages like transformers, torch downloading from source.

**Solution:**
```powershell
# Use pip cache and parallel downloads
pip install -r requirements.txt --cache-dir ~/.pip-cache

# Or install specific packages with pre-built wheels
pip install --only-binary :all: torch transformers
```

---

### **Getting Help**

If issues persist:

1. **Check Logs:**
   ```powershell
   # Backend logs
   cat backend/data/logs/app.log  # Last 100 lines
   
   # Or check terminal output directly
   ```

2. **Verify Environment:**
   ```powershell
   # Python version (needs 3.11+)
   python --version
   
   # Node version (needs 18+)
   node --version
   
   # Pip version
   pip --version
   ```

3. **Reset Everything:**
   ```powershell
   # Delete virtual environments and caches
   Remove-Item -Recurse backend/venv, frontend/node_modules
   
   # Run START_APP.bat again
   .\START_APP.bat
   ```

4. **Check System Requirements:**
   - Python 3.11 or higher
   - Node.js 18 or higher  
   - 8GB+ RAM (for running local models)
   - 10GB+ free disk space
   - Windows 10/11, macOS 10.15+, or Linux

---

## 📖 API Endpoints

### **Core Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/chat` | POST | Basic chat (original) |
| `/api/v1/chat/v2` | POST | Enhanced chat (multi-intent, multi-language) |
| `/api/v1/multilingual/chat` | POST | Language-aware chat |
| `/api/v1/multilingual/sop` | POST | Generate SOP in any language |
| `/api/v1/multilingual/translate` | POST | Translate content |
| `/api/v1/multilingual/languages` | GET | Get supported languages |
| `/api/v1/complaints` | GET | List all complaints |
| `/api/v1/complaints` | POST | Create complaint |
| `/api/v1/complaints/{id}` | GET | Get complaint details |
| `/api/v1/admin/stats` | GET | System statistics |

### **Enhanced Chat API (v2)**

**Endpoint:** `POST /api/v1/chat/v2`

**Request:**
```json
{
  "message": "My Instagram was hacked and they are doing financial fraud",
  "conversation_id": "optional-uuid"
}
```

**Response:**
```json
{
  "request_id": "unique-uuid",
  "query": "My Instagram was hacked...",
  "detected_language": "ENGLISH",
  "detected_crime_types": ["SOCIAL_MEDIA_HACKING", "FINANCIAL_FRAUD"],
  "response": "Based on your query...",
  "sources": [...],
  "official_contacts": {
    "helplines": {...},
    "portals": {...}
  },
  "sop_actions": {
    "now": [...],
    "within_24h": [...],
    "within_7d": [...],
    "ongoing": [...]
  },
  "response_time_ms": 1234.56
}
```

---

## 🎯 Common Tasks & Commands

### **Starting the Application**

**Windows:**
```powershell
# Quick start (recommended)
.\START_APP.bat

# Manual start
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Linux/macOS:**
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### **Stopping Services**

**Windows:**
```powershell
# Find and stop processes
taskkill /F /FI "WINDOWTITLE eq *Backend*"
taskkill /F /FI "WINDOWTITLE eq *Frontend*"

# Or just close the terminal windows
```

**Linux/macOS:**
```bash
# Press Ctrl+C in each terminal

# Or find and kill processes
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

### **Reinstalling Dependencies**

**Backend:**
```powershell
# Windows
cd backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```powershell
# Windows
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install

# Linux/macOS
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### **Running Tests**

```powershell
# Backend tests
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
pytest tests/ -v

# Frontend tests  
cd frontend
npm test
```

### **Checking Logs**

```powershell
# Backend logs
cat backend/data/logs/app.log  # Linux/macOS
Get-Content backend/data/logs/app.log -Tail 50  # Windows

# Or check terminal output directly
```

### **Accessing API Documentation**

```
Open browser: http://localhost:8000/api/docs
```

---

## 📖 API Endpoints

---

## 📖 Supported Crime Categories

### **Financial Fraud** (10 types)
✅ UPI/Digital Payment Fraud  
✅ Internet Banking Fraud  
✅ Credit/Debit Card Fraud  
✅ Cryptocurrency Scams  
✅ Investment Fraud  
✅ Online Shopping Fraud  
✅ Fake Payment Requests  
✅ ATM Fraud  
✅ Wallet Fraud (Paytm, PhonePe, etc.)  
✅ Loan App Fraud  

### **Social Media** (7 types)
✅ Account Hacking (Instagram, Facebook, Twitter)  
✅ Identity Theft  
✅ Fake Profiles  
✅ Cyberbullying  
✅ Impersonation  
✅ Morphed Images  
✅ Social Media Fraud  

### **Women/Child Safety** (6 types)
✅ Sextortion  
✅ Online Blackmail  
✅ Cyberstalking  
✅ Child Abuse Material (CSAM)  
✅ Online Harassment  
✅ Revenge Porn  

### **Cyber Attacks** (6 types)
✅ Phishing (Email/SMS/Call)  
✅ Ransomware  
✅ Malware/Viruses  
✅ DDoS Attacks  
✅ Website Defacement  
✅ Data Breach  

### **Others** (8 types)
✅ SIM Swap Fraud  
✅ Online Job Fraud  
✅ Fake Apps  
✅ Lottery Scams  
✅ Matrimonial Fraud  
✅ OTP Fraud  
✅ Domain Fraud  
✅ Email Hacking  

**Total: 37+ Crime Types**

---

## 🌍 Multi-Language Support

### **Supported Languages (8)**
- 🇮🇳 **English** (Default)
- 🇮🇳 **Hindi** (हिंदी)
- 🇮🇳 **Tamil** (தமிழ்)
- 🇮🇳 **Telugu** (తెలుగు)
- 🇮🇳 **Bengali** (বাংলা)
- 🇮🇳 **Marathi** (मराठी)
- 🇮🇳 **Gujarati** (ગુજરાતી)
- 🇮🇳 **Kannada** (ಕನ್ನಡ)

### **Two-Layer Translation System**

#### **Layer 1: Static UI (i18next)**
- Navigation menus, buttons, forms automatically translated
- Instant language switching with localStorage persistence
- Complete translation files for all 8 languages

#### **Layer 2: Dynamic AI Content (OpenRouter)**
- AI responses generated in user's selected language
- 9 free AI models available (Llama 3.3, Gemma 3, DeepSeek, etc.)
- Context-aware translations preserving technical terms and URLs

### **Setup for Multilingual Features**

1. **Get OpenRouter API Key (Free):**
   - Visit: https://openrouter.ai/keys
   - Sign up and copy your API key

2. **Configure Backend:**
   ```env
   # Add to backend/.env
   OPENROUTER_API_KEY=your-key-here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_DEFAULT_MODEL=meta-llama/llama-3.3-70b-instruct:free
   SUPPORTED_LANGUAGES=en,hi,ta,te,bn,mr,gu,kn
   DEFAULT_LANGUAGE=en
   ```

3. **Install Additional Dependencies:**
   ```bash
   # Backend
   cd backend
   pip install httpx
   
   # Frontend
   cd frontend
   npm install i18next react-i18next i18next-browser-languagedetector i18next-http-backend
   ```

4. **Start and Use:**
   - Click Globe icon in header to select language
   - UI updates instantly
   - AI responds in selected language

### **Available AI Models (Free)**
- `meta-llama/llama-3.3-70b-instruct:free` ⭐ Default
- `google/gemma-3-27b-it:free` - Good for Indian languages
- `tngtech/deepseek-r1t2-chimera:free` - Fast responses
- `amazon/nova-2-lite-v1:free` - Lightweight
- `kwaipilot/kat-coder-pro:free` - Specialized
- And 4 more models...

### **Architecture**
```
User selects language → LanguageContext updates
                              ↓
                    ┌─────────┴────────┐
                    │                  │
           Static UI (i18n)    Dynamic AI (OpenRouter)
                    │                  │
              Instant updates    RAG → Ollama (English)
              Navigation, UI           ↓
              Buttons, Forms     OpenRouter translates
                                 to target language
```

### **API Endpoints**

**Chat in any language:**
```http
POST /api/v1/multilingual/chat
{
  "message": "What is phishing?",
  "language": "hi"  // Hindi
}
```

**Generate SOP:**
```http
POST /api/v1/multilingual/sop
{
  "query": "How to report UPI fraud?",
  "language": "ta",  // Tamil
  "use_rag": true
}
```

**Translate content:**
```http
POST /api/v1/multilingual/translate
{
  "content": "Contact helpline",
  "target_language": "te"  // Telugu
}
```

**Get supported languages:**
```http
GET /api/v1/multilingual/languages
```

### **Usage Examples**

**Frontend (React):**
```tsx
import { useTranslation } from 'react-i18next';
import { useLanguage } from '@/context/LanguageContext';

function MyComponent() {
  const { t } = useTranslation();  // Static UI
  const { language, setLanguage } = useLanguage();
  
  return (
    <>
      <h1>{t('app.title')}</h1>  {/* Static */}
      <button onClick={() => setLanguage('hi')}>हिंदी</button>
      {/* AI responses come in selected language */}
    </>
  );
}
```

**Backend (Python):**
```python
from app.services.multilingual_llm_service import multilingual_llm_service

# Generate SOP in Hindi
response = await multilingual_llm_service.generate_sop_response(
    query="How to report fraud?",
    language="hi",  # Hindi
    use_rag=True
)
```

### **Features**
- ✅ **Auto language detection** from user queries
- ✅ **Persistent language selection** (localStorage)
- ✅ **Language-aware chat** - AI responds correctly
- ✅ **Smart translation** - Preserves URLs, numbers, technical terms
- ✅ **Fallback handling** - Graceful error recovery
- ✅ **Native language support** in complete UI

---

## 📞 Official Resources

### **Emergency Helplines**
- **National Cybercrime Helpline:** **1930** (24x7, Financial Fraud)
- **Women's Helpline:** **181** (24x7)
- **Child Helpline:** **1098** (24x7)
- **Emergency:** **112** (24x7, All emergencies)

### **Reporting Portals**
- **National Cybercrime Portal:** https://cybercrime.gov.in
- **CERT-In:** https://www.cert-in.org.in
- **Women/Child Crimes:** https://cybercrime.gov.in/Webform/Womenchild.aspx
- **Financial Fraud Portal:** https://cybercrime.gov.in

### **Platform Support**
- **Meta (Facebook/Instagram):** https://transparency.fb.com
- **Twitter/X:** https://help.twitter.com/en/safety-and-security
- **Google/YouTube:** https://support.google.com/youtube/answer/2802027
- **WhatsApp:** https://www.whatsapp.com/contact/

### **Banking & Financial**
- **NPCI (UPI):** https://www.npci.org.in/what-we-do/upi/dispute-redressal-mechanism
- **RBI Grievance:** https://cms.rbi.org.in
- **Banking Ombudsman:** https://cms.rbi.org.in

### **Government Resources**
- **Ministry of Electronics & IT (MeitY):** https://www.meity.gov.in
- **Department of Telecom (DoT):** https://dot.gov.in
- **Reserve Bank of India (RBI):** https://www.rbi.org.in

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### **Getting Started**

1. **Fork the repository** on GitHub
2. **Clone your fork:**

<details>
<summary><b>Windows</b></summary>

```powershell
git clone https://github.com/YOUR_USERNAME/cyber-sop-assistant.git
cd cyber-sop-assistant
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
git clone https://github.com/YOUR_USERNAME/cyber-sop-assistant.git
cd cyber-sop-assistant
```

</details>

3. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

4. **Make your changes** and test thoroughly

5. **Run tests:**

<details>
<summary><b>Windows</b></summary>

```powershell
cd backend
.\venv\Scripts\activate
pytest tests/ -v --cov=app
```

</details>

<details>
<summary><b>Linux/macOS</b></summary>

```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov=app
```

</details>

6. **Commit your changes:**
```bash
git add .
git commit -m "feat: add your feature description"
```

7. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

8. **Create a Pull Request** on GitHub

### **Contribution Guidelines**

- Follow existing code style and conventions
- Write meaningful commit messages (see commit conventions above)
- Add tests for new features
- Update documentation as needed
- Be respectful and inclusive (see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md))

### **Areas for Contribution**

- 🐛 **Bug fixes** and error handling
- ✨ **New features** (evidence upload, PDF generation, etc.)
- 📚 **Documentation** improvements
- 🌍 **Translations** and language support
- 🧪 **Testing** (unit, integration, e2e)
- 🎨 **UI/UX** enhancements
- 🔒 **Security** improvements
- 📝 **SOP templates** for more crime types

---

## 📈 Roadmap & Future Enhancements

### **Phase 1: Core (Completed ✅)**
- [x] Local LLM integration (Ollama + Mistral 7B)
- [x] RAG pipeline with ChromaDB
- [x] 7 foundational SOP categories
- [x] FastAPI backend with async support
- [x] React + TypeScript frontend
- [x] Automated setup scripts

### **Phase 2: Enhancement (40% Complete 🚧)**
- [x] **Crime Classification:** 30+ crime types
- [x] **Multi-language:** 8 Indian languages
- [x] **Multi-intent Detection:** Handle complex queries
- [x] **Official Links Database:** Verified .gov.in contacts
- [x] **Timeline-based SOPs:** NOW/24H/7D/ONGOING actions
- [ ] **Evidence Upload:** File attachments (screenshots, docs)
- [ ] **PDF Generation:** Download complaint drafts
- [ ] **Progress Tracker:** Track complaint status
- [ ] **Voice Input/Output:** Speech-to-text and text-to-speech
- [ ] **UI Overhaul:** Language selector, emergency button, responsive design

### **Phase 3: Advanced (Planned 📋)**
- [ ] **Fine-tuned LLM:** Custom model trained on Indian cybercrime data
- [ ] **Real-time Updates:** Live complaint status from cybercrime.gov.in
- [ ] **1930 API Integration:** Direct complaint submission
- [ ] **Offline PWA:** Progressive Web App for offline access
- [ ] **Mobile App:** Native Android/iOS apps
- [ ] **Analytics Dashboard:** Crime trends and statistics
- [ ] **Chatbot API:** Embed in other websites
- [ ] **Blockchain Verification:** Immutable complaint records
- [ ] **AI-powered Evidence Analysis:** Auto-detect fraud patterns
- [ ] **Multi-tenant Support:** Separate instances for organizations

### **Phase 4: Scale & Production (Future 🚀)**
- [ ] **Cloud Deployment:** AWS/Azure/GCP hosting
- [ ] **Load Balancing:** Handle 10,000+ concurrent users
- [ ] **PostgreSQL Migration:** Production-grade database
- [ ] **Redis Caching:** Faster response times
- [ ] **Monitoring:** Prometheus + Grafana
- [ ] **CI/CD Pipeline:** Automated testing and deployment
- [ ] **Docker Orchestration:** Kubernetes deployment
- [ ] **CDN Integration:** Fast global access
- [ ] **API Rate Limiting:** Prevent abuse
- [ ] **User Authentication:** OAuth2, SSO

---

## 🎯 Quick Start Checklist

Before running the application, ensure:

- [ ] Python 3.11+ installed (`python --version` or `python3 --version`)
- [ ] Node.js 20.x installed (`node --version`)
- [ ] Ollama installed (`ollama --version`)
- [ ] Mistral 7B model downloaded (`ollama list`)
- [ ] Repository cloned (`git clone ...`)
- [ ] Virtual environment created and activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Database initialized (`python scripts/init_setup.py`)
- [ ] Vector DB populated (`python scripts/populate_data.py`)
- [ ] Ollama service running (`ollama serve`)
- [ ] Backend running (`uvicorn app.main:app --reload`)
- [ ] Frontend running (`npm run dev`)
- [ ] Application accessible at http://localhost:5173

**All green? 🎉 You're ready to go!**

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this project freely, as long as you include the original license and copyright notice.

---

## 🙏 Acknowledgments

- **Government of India** - Cybercrime guidelines and SOPs
- **CERT-In** - Incident response frameworks
- **National Cybercrime Reporting Portal** - Official complaint procedures
- **Ollama** - Local LLM runtime and tooling
- **Mistral AI** - Open-source Mistral 7B model
- **FastAPI** - Modern, fast web framework
- **React** - Powerful UI library
- **ChromaDB** - Efficient vector database
- **sentence-transformers** - Multilingual embeddings
- **Open Source Community** - Libraries, tools, and inspiration

---

## ⚖️ Disclaimer

This AI assistant provides **guidance based on official government SOPs**.

⚠️ **Important Notices:**
- Verify critical information with official portals (cybercrime.gov.in)
- This is **NOT legal advice** - consult a lawyer for legal matters
- In **emergencies**, call 1930 (financial fraud) or 112 (all emergencies) immediately
- This is an **independent project**, not affiliated with or endorsed by the Government of India
- The developers are not responsible for any actions taken based on this guidance
- Always follow official procedures and contact authorities directly

⚖️ **Legal Provisions:**
- Information Technology Act, 2000 (IT Act)
- IT (Amendment) Act, 2008
- Indian Penal Code (IPC) - Sections 66, 66A, 66B, 66C, 66D, 67, 67A, 67B, 419, 420, 463, 465, 468, 469, 471, 500, 501, 505, 506
- Criminal Procedure Code (CrPC) - FIR filing procedures

---

## 📞 Support & Contact

### **Issues & Bug Reports**
- **GitHub Issues:** https://github.com/brittytino/cyber-sop-assistant/issues
- Please include:
  - Operating system (Windows/Linux/macOS)
  - Python version (`python --version`)
  - Node.js version (`node --version`)
  - Error messages and logs
  - Steps to reproduce

### **Feature Requests**
- **GitHub Discussions:** https://github.com/brittytino/cyber-sop-assistant/discussions
- Describe the feature and use case clearly

### **Security Vulnerabilities**
- **Email:** security@yourproject.com
- Please do **NOT** create public issues for security vulnerabilities
- See [SECURITY.md](SECURITY.md) for responsible disclosure

### **General Questions**
- **GitHub Discussions:** https://github.com/brittytino/cyber-sop-assistant/discussions/categories/q-a

---

**Made with ❤️ for a safer digital India**

**🚀 Happy Coding! 🛡️**

---

**⭐ If this project helped you, please give it a star on GitHub!**

**🤝 Contributions are welcome! See [CONTRIBUTING.md](CODE_OF_CONDUCT.md) for guidelines.**
