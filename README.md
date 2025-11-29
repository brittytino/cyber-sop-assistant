# 🛡️ Cyber SOP Assistant

AI-powered assistant for Indian cybercrime reporting guidance based on official government SOPs.

## 🚀 Features

- **Real-time Chat Interface** - Natural language queries about cybercrimes
- **RAG-powered Responses** - Context-aware answers from official government documents
- **Multi-language Support** - 8 Indian languages (English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada)
- **Complaint Generation** - Auto-generate complaint drafts for cybercrime.gov.in
- **Evidence Checklists** - Crime-specific evidence collection guidance
- **Emergency Helpline Access** - Quick access to 1930 and other helplines
- **100% Local** - No API costs, runs completely offline

## 🏗️ Architecture

- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + Python 3.11
- **LLM**: Ollama (Mistral 7B Instruct)
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Database**: SQLite

## 📋 Prerequisites

- Pop!_OS / Ubuntu 22.04+ (or any Linux distribution)
- 16GB RAM minimum
- 20GB free disk space
- Python 3.11+
- Node.js 20+

## 🔧 Installation

### 1. Clone Repository
git clone <repository-url>
cd cyber-sop-assistant

text

### 2. Run Setup Scripts
Install system dependencies
chmod +x scripts/setup/.sh
chmod +x scripts/deployment/.sh

./scripts/setup/00_install_dependencies.sh
./scripts/setup/01_setup_ollama.sh

text

### 3. Setup Backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

text

### 4. Setup Frontend
cd frontend
npm install
cd ..

text

### 5. Download Models & Initialize DB
./scripts/setup/02_download_models.sh
./scripts/setup/03_initialize_db.sh

text

### 6. Scrape Government Data
cd backend
source venv/bin/activate
python scripts/data/01_scrape_government_data.py
python scripts/vectorstore/01_create_vectorstore.py
python scripts/vectorstore/02_populate_vectorstore.py

text

## 🚀 Running the Application

### Terminal 1 - Start Ollama
./scripts/deployment/start_ollama.sh

text

### Terminal 2 - Start Backend
./scripts/deployment/start_backend.sh

text

### Terminal 3 - Start Frontend
./scripts/deployment/start_frontend.sh

text

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## 🧪 Testing

cd backend
source venv/bin/activate
pytest tests/ -v --cov=app

text

## 📚 Documentation

See `docs/` folder for detailed documentation:
- `SETUP.md` - Detailed setup instructions
- `API.md` - API endpoint documentation
- `ARCHITECTURE.md` - System architecture
- `DEPLOYMENT.md` - Production deployment guide

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📄 License

MIT License

## 🙏 Acknowledgments

- Government of India - National Cyber Crime Portal
- CERT-In - Cyber security advisories
- RBI - Banking fraud guidelines
- MeitY - IT Rules and regulations