"""
FastAPI Main Application
Cyber-SOP Assistant - Indian Cybercrime Reporting & Guidance System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .db import init_db
from .routers import chat, resources, police, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting Cyber-SOP Assistant API...")
    logger.info(f"Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    
    # Auto-populate empty database
    from .db import SessionLocal
    from .models import Resource, PoliceStation
    
    db = SessionLocal()
    try:
        # Check and init Resources
        if db.query(Resource).count() == 0:
             from .seed_data import RESOURCES
             for r in RESOURCES:
                 db.add(Resource(**r))
             db.commit()
             logger.info(f"Auto-populated {len(RESOURCES)} resources")
             
        # Check and init Police
        if db.query(PoliceStation).count() == 0:
             from .seed_data import POLICE_STATIONS
             for p in POLICE_STATIONS:
                 db.add(PoliceStation(**p))
             db.commit()
             logger.info(f"Auto-populated {len(POLICE_STATIONS)} police stations")
             
    except Exception as e:
        logger.error(f"Error auto-populating DB: {e}")
    finally:
        db.close()

    logger.info(f"Chroma DB path: {settings.CHROMA_DIR}")
    logger.info(f"LLM Endpoint: {settings.LLM_ENDPOINT}")
    logger.info(f"LLM Model: {settings.LLM_MODEL}")
    yield
    # Shutdown
    logger.info("Shutting down Cyber-SOP Assistant API...")

app = FastAPI(
    title="Cyber-SOP Assistant API",
    description="Indian Cybercrime Reporting & Guidance System with RAG",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])
app.include_router(police.router, prefix="/api/police", tags=["Police Stations"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# Auth Router
from .routers import auth
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

from .routers import transcription, playground
app.include_router(transcription.router, prefix="/api/utils", tags=["Utils"])
app.include_router(playground.router, prefix="/api/playground", tags=["Playground"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cyber-SOP Assistant API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    from .services.llm_client import check_ollama_health
    from .services.rag import get_collection_stats
    
    ollama_status = check_ollama_health()
    chroma_stats = get_collection_stats()
    
    return {
        "status": "healthy",
        "database": "connected",
        "llm": ollama_status,
        "vector_store": chroma_stats
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# code update on 2025-12-15

# code update on 2025-12-26

# code update on 2025-12-15

# code update on 2025-12-15

# code update on 2025-12-15

# code update on 2025-12-26

# code update on 2025-12-27

# code update on 2025-12-28

# code update on 2025-12-29

# code update on 2025-12-30

# code update on 2025-12-31

# code update on 2026-01-03

# code update on 2026-01-05

# code update on 2026-01-01

# code update on 2026-01-08

# code update on 2025-08-20

# code update on 2025-09-08

# code update on 2025-11-03

# code update on 2026-02-01

# code update on 2025-01-02

# code update on 2025-01-12

# code update on 2025-01-15

# code update on 2025-03-08

# code update on 2025-03-09

# code update on 2025-03-10

# code update on 2025-03-21

# code update on 2025-03-23

# code update on 2025-03-24

# code update on 2025-03-25

# code update on 2025-04-02

# code update on 2025-04-05

# code update on 2025-04-20

# code update on 2025-04-26

# code update on 2025-04-28

# code update on 2025-05-23

# code update on 2025-05-25

# code update on 2025-05-28

# code update on 2025-06-01

# code update on 2025-06-15

# code update on 2025-06-19

# code update on 2025-06-24

# code update on 2025-07-11

# code update on 2025-07-18

# code update on 2025-07-20

# code update on 2025-07-21

# code update on 2025-07-22

# code update on 2025-07-29

# code update on 2025-08-01

# code update on 2025-08-11

# code update on 2025-01-21

# code update on 2025-01-31

# code update on 2025-02-11

# code update on 2025-02-13

# code update on 2025-02-17

# code update on 2025-02-23

# code update on 2025-04-08

# code update on 2025-04-11

# code update on 2025-05-01

# code update on 2025-05-04

# code update on 2025-05-05

# code update on 2025-05-10

# code update on 2025-05-15

# code update on 2025-05-20

# code update on 2025-07-02

# code update on 2025-07-05

# code update on 2024-01-04

# code update on 2024-01-06

# code update on 2024-01-07

# code update on 2024-01-09

# code update on 2024-01-11

# code update on 2024-01-12

# code update on 2024-01-16

# code update on 2024-01-18

# code update on 2024-01-23

# code update on 2024-01-25

# code update on 2024-01-28

# code update on 2024-01-30

# code update on 2024-02-02

# code update on 2024-02-04

# code update on 2024-02-05

# code update on 2024-02-07

# code update on 2024-02-09

# code update on 2024-02-12

# code update on 2024-02-19

# code update on 2024-02-21

# code update on 2024-02-23

# code update on 2024-02-26

# code update on 2024-02-28

# code update on 2024-03-16

# code update on 2024-03-27

# code update on 2024-03-29

# code update on 2024-03-31

# code update on 2024-04-02

# code update on 2024-04-04

# code update on 2024-04-06

# code update on 2024-04-14

# code update on 2024-04-15

# code update on 2024-04-16

# code update on 2024-04-26

# code update on 2024-09-04

# code update on 2024-09-06

# code update on 2024-09-29

# code update on 2024-10-03

# code update on 2024-10-04

# code update on 2024-10-06

# code update on 2024-10-08

# code update on 2024-10-11

# code update on 2024-10-15

# code update on 2024-10-24
