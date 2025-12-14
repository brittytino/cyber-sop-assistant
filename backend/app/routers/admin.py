"""
Admin Router - Administrative functions and statistics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

from ..dependencies import get_db
from ..schemas import StatsResponse, DocumentOut, DocumentCreate
from ..models import Chat, Message, Document, Resource, PoliceStation
from ..services.rag import get_collection_stats

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get system statistics
    """
    total_chats = db.query(func.count(Chat.id)).scalar()
    total_messages = db.query(func.count(Message.id)).scalar()
    total_documents = db.query(func.count(Document.id)).scalar()
    total_resources = db.query(func.count(Resource.id)).scalar()
    total_police_stations = db.query(func.count(PoliceStation.id)).scalar()
    
    # Get ChromaDB stats
    chroma_stats = get_collection_stats()
    total_chunks = chroma_stats.get("total_chunks", 0)
    
    return StatsResponse(
        total_chats=total_chats,
        total_messages=total_messages,
        total_documents=total_documents,
        total_chunks=total_chunks,
        total_resources=total_resources,
        total_police_stations=total_police_stations
    )

@router.get("/documents")
async def get_documents(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Get list of indexed documents
    """
    documents = db.query(Document).offset(skip).limit(limit).all()
    total = db.query(func.count(Document.id)).scalar()
    
    return {
        "total": total,
        "documents": documents
    }

@router.post("/documents", response_model=DocumentOut)
async def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    """
    Add a new document record
    """
    db_document = Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/health")
async def admin_health():
    """
    Detailed health check
    """
    from ..services.llm_client import check_ollama_health
    
    ollama_status = check_ollama_health()
    chroma_stats = get_collection_stats()
    
    return {
        "api": "healthy",
        "llm": ollama_status,
        "vector_store": chroma_stats
    }
