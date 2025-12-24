# Cyber-SOP Assistant

A comprehensive Indian Cybercrime Reporting & Guidance System with local RAG (Retrieval Augmented Generation) capabilities.

## 🎯 Features

- **AI-Powered Chat**: Get instant guidance on cybercrime reporting using local LLM (Ollama)
- **RAG System**: Retrieves relevant information from indexed cyber-SOP documents
- **Resources Hub**: Quick access to NCRP, CEIR, TAFCOP, CERT-In, and other official portals
- **Police Locator**: Find nearby police stations and cyber cells
- **Chat History**: Save and revisit your conversations
- **Fully Local**: No cloud dependencies - runs completely on your Windows machine

## 📋 Prerequisites

### Required Software:
1. **Python 3.10 or higher** - [Download](https://www.python.org/downloads/)
2. **Node.js 18 or higher** - [Download](https://nodejs.org/)
3. **Ollama** - [Download](https://ollama.ai/download/windows)
4. **Git** (optional) - [Download](https://git-scm.com/downloads)

## 🚀 Setup Guide (Windows)

### Step 1: Install Ollama and Download Model

1. Download and install Ollama from https://ollama.ai/download/windows
2. Open PowerShell and run:
```powershell
ollama pull mistral:instruct
```

3. Verify Ollama is running:
```powershell
ollama list
```

### Step 2: Backend Setup

1. Open PowerShell in the project root directory
2. Navigate to backend:
```powershell
cd backend
```

3. Create Python virtual environment:
```powershell
python -m venv venv
```

4. Activate virtual environment:
```powershell
.\venv\Scripts\activate
```

5. Install dependencies:
```powershell
pip install -r requirements.txt
```

6. Create `.env` file (copy from .env.example):
```powershell
copy .env.example .env
```

### Step 3: Frontend Setup

1. Open a NEW PowerShell window
2. Navigate to frontend:
```powershell
cd frontend
```

3. Install dependencies:
```powershell
npm install
```

4. Create `.env` file:
```powershell
copy .env.example .env
```

### Step 4: Initialize Data

1. In the backend PowerShell (with venv activated):
```powershell
# This will create database tables and initialize sample data
python -c "from app.db import init_db; init_db(); print('Database initialized')"
```

## 🎮 Running the Application

### Easy Way (Using Scripts):

1. **Start Backend** - Double-click `scripts\dev_backend.cmd`
   - Or in PowerShell: `.\scripts\dev_backend.cmd`
   - Backend runs on: http://localhost:8000

2. **Start Frontend** - Double-click `scripts\dev_frontend.cmd`
   - Or in PowerShell: `.\scripts\dev_frontend.cmd`
   - Frontend runs on: http://localhost:5173

3. **Access Application**: Open browser to http://localhost:5173

### Manual Way:

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

## 📊 Adding Your Own Data

### Method 1: Using the Admin API

Visit `http://localhost:8000/docs` and use the admin endpoints to add:
- Documents (for RAG)
- Resources
- Police stations

### Method 2: Using Python Script

Create a script in `backend/scripts/add_data.py`:

```python
import sys
sys.path.insert(0, '..')

from app.db import SessionLocal, init_db
from app.models import Document
from app.services.rag import get_collection
from app.services.embedding_client import embed_text
import uuid

init_db()
db = SessionLocal()

# Add document to database
doc = Document(
    source="NCRP Guidelines",
    title="How to Report Cybercrime",
    category="Reporting",
    content="Step 1: Visit cybercrime.gov.in..."
)
db.add(doc)
db.commit()

# Add to vector store
collection = get_collection()
chunk_id = str(uuid.uuid4())
embedding = embed_text([doc.content])[0]

collection.add(
    ids=[chunk_id],
    embeddings=[embedding],
    documents=[doc.content],
    metadatas=[{
        "source": doc.source,
        "title": doc.title,
        "category": doc.category
    }]
)

print(f"Added document: {doc.title}")
db.close()
```

Run it:
```powershell
cd backend
.\venv\Scripts\activate
python scripts\add_data.py
```

## 🏗️ Project Structure

```
cyber-sop-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── db.py             # Database setup
│   │   ├── routers/          # API endpoints
│   │   │   ├── chat.py       # Chat & RAG
│   │   │   ├── resources.py  # Resources
│   │   │   ├── police.py     # Police stations
│   │   │   └── admin.py      # Admin functions
│   │   └── services/         # Business logic
│   │       ├── rag.py        # RAG pipeline
│   │       ├── llm_client.py # Ollama client
│   │       └── embedding_client.py # Embeddings
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main app
│   │   ├── components/       # UI components
│   │   ├── hooks/            # React hooks
│   │   └── api/              # API client
│   ├── package.json
│   └── .env
│
├── data/
│   ├── chroma_store/         # Vector database
│   └── processed/            # Processed documents
│
└── scripts/
    ├── dev_backend.cmd       # Start backend
    └── dev_frontend.cmd      # Start frontend
```

## 🔧 API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 UI Features

- **Fixed Layout**: No page scroll, only chat scrolls
- **Sidebar Navigation**:
  - Recent Chats
  - Resources (NCRP, CEIR, TAFCOP, etc.)
  - Nearby Police Stations
  - API Documentation
- **Dark Theme**: Perplexity-style clean interface
- **Real-time Chat**: Instant responses from local LLM
- **Source Citations**: See which documents informed the answer

## 🐛 Troubleshooting

### Issue: "Cannot connect to Ollama"
**Solution**: 
1. Make sure Ollama is installed
2. Run `ollama serve` in a terminal
3. Verify with `ollama list`

### Issue: "Module not found" errors
**Solution**:
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

### Issue: Frontend won't start
**Solution**:
```powershell
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

### Issue: "Database locked" error
**Solution**: Close all backend instances and restart

### Issue: Empty responses from AI
**Solution**: Check if you have indexed documents. Use the admin API to add data.

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./cyber_sop.db
CHROMA_DIR=../data/chroma_store
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral:instruct
CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## 🔐 Security Notes

- This is a **local development setup** - not production-ready
- SQLite database stores all data locally
- No authentication/authorization implemented
- Add proper security measures before any deployment

## 📚 Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database
- ChromaDB - Vector database
- sentence-transformers - Embeddings
- Ollama - Local LLM inference

**Frontend:**
- React + TypeScript
- Vite - Fast build tool
- Axios - HTTP client
- Lucide Icons - Icon library

## 🤝 Contributing

This is a hackathon project. To extend:

1. Add more document sources to RAG
2. Implement user authentication
3. Add multilingual support
4. Create mobile-responsive design
5. Add more AI features (summarization, translation)

## 📄 License

This project is for educational purposes. Always refer to official government portals for authentic information.

## 🆘 Support

For issues:
1. Check the Troubleshooting section
2. Verify all prerequisites are installed
3. Check backend logs in terminal
4. Visit API docs at http://localhost:8000/docs

---

**Made for SRCAS Hackathon** 🇮🇳

<!-- updated on 2025-12-02 -->

<!-- updated on 2025-12-05 -->

<!-- updated on 2025-12-24 -->
