# Cyber SOP Assistant

<div align="center">

![Cyber SOP Assistant](https://img.shields.io/badge/Cyber%20SOP-Assistant-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.3-blue?style=for-the-badge&logo=react)

**AI-Powered Cybercrime Assistance Platform for India**

[Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-detailed-setup) • [API Docs](#-api-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
  - [Windows Setup](#windows-setup)
  - [Linux/Mac Setup](#linuxmac-setup)
- [Detailed Setup](#-detailed-setup)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## 🌟 Overview

**Cyber SOP Assistant** is an intelligent platform designed to help Indian citizens handle cybercrime incidents effectively. Built with FastAPI and React, powered by local Ollama LLM.

### What You Get:

- ✅ **AI-Powered Guidance** - Instant, contextual advice for cybercrime incidents
- ✅ **Multi-Language Support** - Available in 8 Indian languages
- ✅ **Anonymous Access** - Use without registration for complete privacy
- ✅ **Automated Filing** - Auto-fill complaints on government portals
- ✅ **Location Services** - Find nearby cyber crime police stations
- ✅ **Emergency Actions** - Quick access to helplines and resources
- ✅ **Evidence Management** - Structured checklist for evidence collection
- ✅ **Progress Tracking** - Monitor your complaint journey

---

## 🚀 Key Features

### 1. **Intelligent Chat Assistant**
- RAG-based AI powered by Ollama LLM (Llama 3 8B)
- Analyzes incident details and provides step-by-step guidance
- Suggests relevant official links and emergency contacts
- Generates evidence checklists based on crime type
- Supports 8 Indian languages with i18next

### 2. **Authentication & Privacy**
- OTP-based login (phone/email) with 6-digit codes
- Anonymous mode for privacy-conscious users
- JWT token-based secure authentication
- Complete profile management
- Session-based tracking

### 3. **Automated Complaint Filing** 
- Queue-based filing system with background processing
- Portal integration framework (cybercrime.gov.in ready)
- Form auto-fill with user profile data
- Real-time status tracking with 10+ stages
- OTP handling for portal authentication

### 4. **Station Finder**
- GPS-based nearby station search with geolocation API
- Pincode/city-based search with 13 pre-mapped pincodes
- Distance calculation using Haversine formula
- 9 pre-loaded major cyber crime cells across India
- Click-to-call and Google Maps directions integration

### 5. **Emergency Panel**
- 8 pre-configured emergency actions with priority sorting:
  - **1930** - National Cyber Fraud Helpline (24x7)
  - **112** - Emergency Police Response
  - **181** - Women's Helpline  
  - **1098** - Child Helpline
  - **Mental Health Support** - 1860-2662-345
  - **TAFCOP** - Block stolen SIM cards
  - **Aadhaar Lock** - Secure Aadhaar data
  - **Cybercrime Portal** - Direct access
- Multi-language titles and descriptions
- One-click call/visit actions

### 6. **Evidence Management**
- Interactive checklist with 10+ evidence types
- File upload with drag-drop support
- Progress tracking with percentage completion
- Tips and guidelines for each evidence type

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (dev), PostgreSQL (production)
- **Authentication**: JWT (python-jose 3.5.0), bcrypt (passlib 1.7.4)
- **LLM**: Ollama (local) - Llama 3 8B
- **Vector Store**: ChromaDB for RAG
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2

### Frontend
- **Framework**: React 18.3 with TypeScript 5.3
- **Build Tool**: Vite 5.4
- **Routing**: React Router 7.10
- **Styling**: Tailwind CSS 3.4
- **UI Components**: Custom components + shadcn/ui patterns
- **HTTP Client**: Axios with interceptors
- **Notifications**: Sonner toast library
- **Icons**: Lucide React 0.309
- **i18n**: i18next 25.7

### DevOps
- **Containerization**: Docker with docker-compose
- **Development**: Hot reload for backend & frontend
- **Environment**: Multi-environment config (dev/test/prod)

---

## ⚡ Quick Start

### Prerequisites

**All Platforms:**
- Python 3.11 or higher
- Node.js 18 or higher
- npm 9 or higher

**Windows:** PowerShell 5.1+  
**Linux/Mac:** Bash shell

---

### Windows Setup

```powershell
# Clone repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# Run start script
.\start.bat
```

The script will automatically:
- ✅ Activate Python virtual environment
- ✅ Start backend server on `http://localhost:8000`
- ✅ Start frontend server on `http://localhost:5173`
- ✅ Open browser automatically

**First Time Setup:**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ..\frontend
npm install

# Now run start.bat
cd ..
.\start.bat
```

---

### Linux/Mac Setup

```bash
# Clone repository
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant

# Make script executable
chmod +x start.sh

# Run start script
./start.sh
```

The script will automatically:
- ✅ Activate Python virtual environment
- ✅ Start backend on port 8000
- ✅ Start frontend on port 5173
- ✅ Open browser

**First Time Setup:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Now run start.sh
cd ..
./start.sh
```

---

## 📦 Detailed Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
# Windows:
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Configure environment
cp config/development/backend.env.example config/development/backend.env
# Edit backend.env - see Configuration section

# Run database migrations (if using PostgreSQL)
alembic upgrade head

# Populate initial data
python scripts/populate_data.py
python scripts/populate_cybercrime_data.py
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### 3. Ollama Setup

**Windows:**
```powershell
# Download installer from https://ollama.ai/download
# Run installer
# Open new terminal and pull model:
ollama pull llama3:8b

# Verify installation
ollama list
```

**Linux/Mac:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the model
ollama pull llama3:8b

# Start Ollama service (if not auto-started)
ollama serve

# Verify model
ollama list
```

---

## ⚙️ Configuration

### Backend Environment Variables

Edit `config/development/backend.env`:

```bash
# Debug Mode
DEBUG=True

# Database
DATABASE_URL=sqlite:///./data/cyber_sop.db
# Production: postgresql://user:password@localhost:5432/cyber_sop

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-in-production-min-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# OTP Configuration
OTP_EXPIRE_SECONDS=300
OTP_MAX_ATTEMPTS=3
OTP_RETRY_DELAY_SECONDS=60

# SMS Provider (MSG91, Twilio, etc.)
SMS_PROVIDER=msg91
SMS_API_KEY=your-sms-api-key-here
SMS_SENDER_ID=CYBERASSIST

# Email Provider (SendGrid, SMTP, etc.)
EMAIL_PROVIDER=sendgrid
EMAIL_API_KEY=your-email-api-key-here
EMAIL_FROM=noreply@cyberassist.in

# Redis (for production OTP storage)
REDIS_URL=redis://localhost:6379/0
USE_REDIS=False

# Ollama LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# ChromaDB Vector Store
CHROMA_COLLECTION_NAME=cyber_sop_docs

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=.pdf,.jpg,.jpeg,.png,.doc,.docx,.txt
```

**⚠️ Important for Production:**
- Generate strong JWT_SECRET_KEY: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Set up PostgreSQL database
- Configure Redis for OTP storage
- Add real SMS/Email API keys
- Enable HTTPS and update CORS_ORIGINS

### Frontend Environment Variables

Create `frontend/.env`:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

---

## 📖 Usage

### 1. Anonymous User Flow (No Login Required)

```
1. Visit http://localhost:5173
2. Click "Start Chat" in the home page
3. Describe your cybercrime incident in natural language
4. Receive instant AI-powered guidance with:
   - Crime type identification
   - Step-by-step reporting instructions
   - Evidence checklist
   - Official government links
   - Emergency contacts
5. Download generated complaint text
6. Access emergency helplines from emergency panel
```

### 2. Registered User Flow (Full Features)

```
1. Click "Login" button in header
2. Choose authentication method:
   - Phone OTP (enter 10-digit mobile)
   - Email OTP (enter email address)
3. Enter 6-digit OTP (check backend console in dev mode)
4. Complete profile registration:
   - Full name
   - Email (if not registered via email)
   - Phone (if not registered via phone)
   - Complete address (street, city, state, pincode)
5. Access all premium features:
   ✅ Automated complaint filing
   ✅ Station finder with GPS
   ✅ Evidence upload and management
   ✅ Progress tracking with timeline
   ✅ Filing history
```

### 3. Automated Filing Flow

```
1. Login and ensure profile is complete
2. Draft complaint using the chat interface
3. Click "Auto-File" button on complaint page
4. Select target portal (default: cybercrime.gov.in)
5. Monitor real-time filing status with updates every 3 seconds:
   📋 QUEUED → Processing in background
   ⚙️ IN_PROGRESS → Opening portal
   🔐 AWAITING_OTP → Enter OTP in status page
   📝 FORM_FILLING → Auto-filling complaint form
   📎 EVIDENCE_UPLOAD → Uploading evidence files
   ✅ SUBMITTED → Complaint submitted
   🎉 CONFIRMED → Reference number received
6. Copy portal reference number for future tracking
```

### 4. Station Finder Flow

```
1. Navigate to /stations page
2. Choose search method from tabs:
   
   📍 GPS Tab:
   - Click "Use My Location"
   - Allow location permission
   - View stations sorted by distance
   
   🔢 Pincode Tab:
   - Enter 6-digit pincode
   - Click "Search"
   - View stations in that area
   
   🏙️ City Tab:
   - Enter city name
   - Click "Search"
   - View all stations in city

3. For each station:
   - View distance and estimated travel time
   - Click phone icon to call directly
   - Click "Get Directions" for Google Maps route
   - Toggle "Show Only Cyber Cells" filter
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/otp/phone` | Request OTP to phone | No |
| POST | `/auth/otp/email` | Request OTP to email | No |
| POST | `/auth/otp/verify` | Verify OTP and get JWT tokens | No |
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Password-based login | No |
| GET | `/auth/profile` | Get user profile | Yes |
| PATCH | `/auth/profile` | Update profile | Yes |
| POST | `/auth/password/set` | Set/change password | Yes |
| POST | `/auth/refresh` | Refresh access token | Yes |
| POST | `/auth/logout` | Logout and invalidate tokens | Yes |
| POST | `/auth/session/anonymous` | Create anonymous session | No |

### Automation Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/automation/file` | Queue new automated filing | Yes |
| GET | `/automation/status/:id` | Get filing status with real-time updates | Yes |
| GET | `/automation/history` | Get user's filing history | Yes |
| POST | `/automation/otp/:id` | Submit OTP for portal authentication | Yes |
| POST | `/automation/cancel/:id` | Cancel pending filing | Yes |
| GET | `/automation/portals` | Get list of supported portals | No |

### Station Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/stations/nearby` | Find nearby stations (lat/lng or pincode) | No |
| GET | `/stations/by-city` | Find stations by city name | No |
| GET | `/stations/:id` | Get detailed station information | No |
| GET | `/stations` | List all registered stations | No |
| POST | `/stations` | Add new station (admin only) | Yes |
| PUT | `/stations/:id` | Update station details (admin only) | Yes |
| DELETE | `/stations/:id` | Delete station (admin only) | Yes |

### Emergency Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/emergency/actions?language=en` | Get emergency actions with localization | No |
| GET | `/emergency/helplines` | Get all helpline numbers | No |
| GET | `/emergency/portals` | Get important government portals | No |

### Progress Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/progress/:sessionId` | Get user progress for session | Yes |
| POST | `/progress/:sessionId/update` | Update progress to new stage | Yes |
| GET | `/progress/complaint/:id/track` | Track complaint status | Yes |

### Interactive API Documentation

Visit **http://localhost:8000/api/docs** for:
- ✅ Swagger UI with all endpoints
- ✅ Request/response schemas
- ✅ Try-it-out functionality
- ✅ Authentication testing with JWT tokens
- ✅ Example requests and responses

Alternative: **http://localhost:8000/redoc** for ReDoc UI

---

## 🚀 Deployment

### Docker Deployment (Recommended)

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Manual Production Deployment

#### Backend (Ubuntu Server)

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install python3.11 python3-pip postgresql redis-server nginx

# 2. Clone and setup
git clone https://github.com/brittytino/cyber-sop-assistant.git
cd cyber-sop-assistant/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure PostgreSQL
sudo -u postgres createdb cyber_sop
sudo -u postgres createuser cyber_user -P

# 4. Setup production environment
cp config/production/backend.env.example config/production/backend.env
nano config/production/backend.env
# Set strong JWT_SECRET_KEY, database URL, Redis URL, API keys

# 5. Run migrations
alembic upgrade head

# 6. Create systemd service
sudo nano /etc/systemd/system/cyberassist.service
```

**systemd service file:**
```ini
[Unit]
Description=Cyber SOP Assistant Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/cyber-sop-assistant/backend
Environment="PATH=/var/www/cyber-sop-assistant/backend/venv/bin"
ExecStart=/var/www/cyber-sop-assistant/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

```bash
# 7. Start and enable service
sudo systemctl daemon-reload
sudo systemctl enable cyberassist
sudo systemctl start cyberassist
sudo systemctl status cyberassist

# 8. Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/cyberassist
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name api.cyberassist.in;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 9. Enable site and test
sudo ln -s /etc/nginx/sites-available/cyberassist /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 10. Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.cyberassist.in
```

#### Frontend Deployment

**Option 1: Vercel (Recommended)**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel login
vercel

# Production deployment
vercel --prod
```

**Option 2: Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify login
netlify init

# Production deployment
netlify deploy --prod --dir=dist
```

**Option 3: Manual (Nginx)**
```bash
# Build frontend
cd frontend
npm run build

# Copy dist to server
scp -r dist/* user@server:/var/www/cyberassist/

# Nginx configuration
server {
    listen 80;
    server_name cyberassist.in www.cyberassist.in;
    root /var/www/cyberassist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/cyber-sop-assistant.git
cd cyber-sop-assistant

# 3. Create feature branch
git checkout -b feature/amazing-feature

# 4. Make your changes
# ... edit files ...

# 5. Run tests
cd backend && pytest
cd ../frontend && npm test

# 6. Commit changes
git add .
git commit -m "feat: add amazing feature"

# 7. Push to your fork
git push origin feature/amazing-feature

# 8. Open Pull Request on GitHub
```

### Code Style

- **Backend**: Follow PEP 8, use Black formatter (`black .`)
- **Frontend**: Follow ESLint rules, use Prettier (`npm run format`)
- **Commits**: Use conventional commits:
  - `feat:` - New feature
  - `fix:` - Bug fix
  - `docs:` - Documentation only
  - `style:` - Code style changes
  - `refactor:` - Code refactoring
  - `test:` - Adding tests
  - `chore:` - Maintenance tasks

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Data Sources**: 
  - CERT-IN (Indian Computer Emergency Response Team)
  - MeitY Cybercrime Portal
  - RBI Ombudsman Guidelines
  - National Cyber Crime Reporting Portal
- **LLM**: Meta's Llama 3 via Ollama
- **UI Inspiration**: shadcn/ui component patterns
- **Icons**: Lucide React icon library
- **Embeddings**: sentence-transformers by HuggingFace

---

## 📞 Support & Community

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/brittytino/cyber-sop-assistant/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/brittytino/cyber-sop-assistant/discussions)
- **📧 Email**: support@cyberassist.in
- **📖 Documentation**: [Full Docs](./COMPLETE_IMPLEMENTATION.md)

---

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Core chat interface with RAG
- [x] Authentication system (OTP/JWT)
- [x] Automated filing framework
- [x] Station finder with GPS
- [x] Emergency panel
- [x] English language support

### Phase 2 (Next)
- [ ] Complete Hindi & Tamil translations
- [ ] SMS gateway integration (MSG91/Twilio)
- [ ] Email service integration (SendGrid)
- [ ] PostgreSQL migration from SQLite
- [ ] Redis integration for OTP storage
- [ ] Headless browser for portal automation

### Phase 3 (Future)
- [ ] WhatsApp bot integration
- [ ] Mobile app (React Native)
- [ ] Voice input support (speech-to-text)
- [ ] SMS-based access for feature phones
- [ ] Integration with more portals (RBI Ombudsman, Police)
- [ ] AI model fine-tuning with Indian cybercrime cases
- [ ] Real-time case tracking dashboard
- [ ] Legal consultation booking system
- [ ] Victim community support forum

---

<div align="center">

**Made with ❤️ for India's Digital Safety**

[![GitHub Stars](https://img.shields.io/github/stars/brittytino/cyber-sop-assistant?style=social)](https://github.com/brittytino/cyber-sop-assistant)
[![GitHub Forks](https://img.shields.io/github/forks/brittytino/cyber-sop-assistant?style=social)](https://github.com/brittytino/cyber-sop-assistant/fork)
[![GitHub Issues](https://img.shields.io/github/issues/brittytino/cyber-sop-assistant)](https://github.com/brittytino/cyber-sop-assistant/issues)

[⬆ Back to Top](#cyber-sop-assistant)

</div>
