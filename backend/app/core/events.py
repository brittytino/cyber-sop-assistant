"""
Application Lifecycle Events
Startup and shutdown event handlers
"""
from app.core.logging import logger
from app.core.config import settings
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service
from app.db.session import init_db
import asyncio


async def startup_event():
    """Execute on application startup"""
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info("=" * 60)
    
    # Initialize database
    try:
        logger.info("📊 Initializing database...")
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Initialize embedding model
    try:
        logger.info("🤖 Loading embedding model...")
        await embedding_service.initialize()
        logger.info("✅ Embedding model loaded")
    except Exception as e:
        logger.error(f"❌ Embedding model initialization failed: {e}")
    
    # Initialize RAG service (ChromaDB)
    try:
        logger.info("🗄️  Initializing vector database...")
        await rag_service.initialize()
        doc_count = rag_service.get_document_count()
        logger.info(f"✅ Vector database initialized ({doc_count} documents)")
    except Exception as e:
        logger.error(f"❌ Vector database initialization failed: {e}")
    
    # Check Ollama connection
    try:
        logger.info("🦙 Connecting to Ollama service...")
        is_connected = await llm_service.check_connection()
        if is_connected:
            logger.info(f"✅ Ollama connected (model: {settings.OLLAMA_MODEL})")
        else:
            logger.warning("⚠️  Ollama service not available")
    except Exception as e:
        logger.error(f"❌ Ollama connection failed: {e}")
    
    logger.info("=" * 60)
    logger.info(f"🌐 API available at http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📖 Docs available at http://{settings.HOST}:{settings.PORT}/api/docs")
    logger.info("=" * 60)


async def shutdown_event():
    """Execute on application shutdown"""
    logger.info("=" * 60)
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}")
    logger.info("=" * 60)
    
    # Cleanup RAG service
    try:
        logger.info("🗄️  Closing vector database...")
        await rag_service.cleanup()
        logger.info("✅ Vector database closed")
    except Exception as e:
        logger.error(f"❌ Vector database cleanup failed: {e}")
    
    # Cleanup embedding service
    try:
        logger.info("🤖 Unloading embedding model...")
        await embedding_service.cleanup()
        logger.info("✅ Embedding model unloaded")
    except Exception as e:
        logger.error(f"❌ Embedding model cleanup failed: {e}")
    
    logger.info("=" * 60)
    logger.info("👋 Shutdown complete")
    logger.info("=" * 60)
