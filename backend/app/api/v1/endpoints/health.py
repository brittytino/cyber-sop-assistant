"""
Health Check Endpoint
"""
from fastapi import APIRouter
from datetime import datetime
import time

from app.models.schemas import HealthResponse
from app.core.config import settings
from app.core.logging import logger
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service

router = APIRouter()

# Track startup time
_startup_time = time.time()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check
    
    Checks status of all critical services:
    - Ollama LLM
    - ChromaDB vector store
    - Embedding model
    """
    logger.debug("Health check requested")
    
    # Check service availability
    services = {
        "ollama": await llm_service.check_connection(),
        "chromadb": rag_service.is_loaded(),
        "embedding_model": embedding_service.is_initialized(),
        "cache": True  # Cache is always available (disk-based)
    }
    
    # Get document count
    doc_count = rag_service.get_document_count()
    
    # Calculate uptime
    uptime_seconds = time.time() - _startup_time
    
    # Determine overall status
    overall_status = "healthy" if all(services.values()) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        version=settings.VERSION,
        timestamp=datetime.utcnow(),
        services=services,
        document_count=doc_count,
        uptime_seconds=round(uptime_seconds, 2)
    )


@router.get("/ready")
async def readiness_check():
    """
    Kubernetes-style readiness probe
    Returns 200 if service is ready to accept requests
    """
    ollama_ready = await llm_service.check_connection()
    rag_ready = rag_service.is_loaded()
    
    if ollama_ready and rag_ready:
        return {"ready": True}
    else:
        return {"ready": False, "reasons": {
            "ollama": ollama_ready,
            "rag": rag_ready
        }}, 503


@router.get("/live")
async def liveness_check():
    """
    Kubernetes-style liveness probe
    Returns 200 if service is alive
    """
    return {"alive": True}
