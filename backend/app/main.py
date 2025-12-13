"""
Cyber SOP Assistant - FastAPI Application Entry Point
Government-aligned cybercrime reporting guidance system
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.events import startup_event, shutdown_event
from app.core.exceptions import register_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.monitoring_middleware import MonitoringMiddleware
from app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await startup_event()
    logger.info("🚀 Cyber SOP Assistant started successfully")
    yield
    # Shutdown
    await shutdown_event()
    logger.info("🛑 Cyber SOP Assistant shutdown complete")


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="LLM-powered assistant for Indian cybercrime reporting SOPs",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# Setup logging
setup_logging()

# Register exception handlers
register_exception_handlers(app)

# Add middleware (order matters - last added runs first)
app.add_middleware(MonitoringMiddleware)
app.add_middleware(RateLimiterMiddleware, rate_limit=settings.RATE_LIMIT_PER_MINUTE)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)

# CORS middleware - Allow network access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS + ["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"]
)

# Include routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/api/docs" if settings.DEBUG else "disabled",
        "endpoints": {
            "chat": "/api/v1/chat",
            "health": "/api/v1/health",
            "complaints": "/api/v1/complaints",
            "evidence": "/api/v1/evidence"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Simple health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
