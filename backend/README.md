# Backend - Cyber-SOP Assistant API

FastAPI backend with RAG (Retrieval Augmented Generation) for Indian cybercrime guidance.

## Features

- **RAG Pipeline**: Retrieves relevant documents and generates contextual answers
- **Local LLM**: Uses Ollama (Mistral) for text generation
- **Vector Search**: ChromaDB for semantic document search
- **SQLite Database**: Stores chats, messages, resources, and police stations
- **REST API**: Well-documented endpoints with Swagger UI

## API Endpoints

### Chat
- `POST /api/chat/message` - Send message and get AI response
- `GET /api/chat/chats` - List recent chats
- `GET /api/chat/chats/{id}` - Get specific chat
- `DELETE /api/chat/chats/{id}` - Delete chat

### Resources
- `GET /api/resources/` - List all resources
- `POST /api/resources/` - Add new resource
- `POST /api/resources/initialize` - Initialize default resources

### Police
- `GET /api/police/search` - Search police stations
- `GET /api/police/states` - List all states
- `POST /api/police/initialize` - Initialize sample data

### Admin
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/health` - Health check
- `GET /api/admin/documents` - List indexed documents

## Setup

1. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
copy .env.example .env
```

4. Initialize database:
```bash
python scripts\init_db.py
```

5. Run server:
```bash
uvicorn app.main:app --reload
```

## Configuration

Edit `.env`:

```env
DATABASE_URL=sqlite:///./cyber_sop.db
CHROMA_DIR=../data/chroma_store
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral:instruct
```

## Adding Documents for RAG

See `scripts/add_custom_data.py` example in QUICKSTART.md

## Tech Stack

- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- ChromaDB 0.4.18
- sentence-transformers 2.2.2
- Ollama (via HTTP API)
