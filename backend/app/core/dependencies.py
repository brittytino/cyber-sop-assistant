"""
Reusable FastAPI Dependencies
"""
from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from app.core.config import settings
from app.core.logging import logger
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service
from app.services.cache_service import cache_service
from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncSession:
    """Get database session"""
    async for session in get_db():
        yield session


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """Verify API key if configured"""
    if settings.API_KEY:
        if not x_api_key or x_api_key != settings.API_KEY:
            logger.warning("Invalid API key attempt")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key"
            )
    return x_api_key or "no-key"


def get_llm_service():
    """Get LLM service instance"""
    return llm_service


def get_rag_service():
    """Get RAG service instance"""
    return rag_service


def get_embedding_service():
    """Get embedding service instance"""
    return embedding_service


def get_cache_service():
    """Get cache service instance"""
    return cache_service


def get_complaint_repository(db: AsyncSession = Depends(get_db_session)) -> ComplaintRepository:
    """Get complaint repository instance"""
    return ComplaintRepository(db)


def get_analytics_repository(db: AsyncSession = Depends(get_db_session)) -> AnalyticsRepository:
    """Get analytics repository instance"""
    return AnalyticsRepository(db)


async def verify_ollama_connection():
    """Verify Ollama service is available"""
    if not await llm_service.check_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ollama service is not available. Please start Ollama service."
        )


async def verify_rag_loaded():
    """Verify RAG service is loaded with documents"""
    if not rag_service.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector database not loaded. Please run data ingestion first."
        )
