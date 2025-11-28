"""
Custom Exception Classes
"""
from typing import Any, Optional, Dict
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger


class CyberSOPException(Exception):
    """Base exception for Cyber SOP Assistant"""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class OllamaConnectionError(CyberSOPException):
    """Ollama service connection error"""
    
    def __init__(self, message: str = "Cannot connect to Ollama service"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"service": "ollama", "action": "Check if Ollama is running"}
        )


class ChromaDBError(CyberSOPException):
    """ChromaDB operation error"""
    
    def __init__(self, message: str = "Vector database error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"service": "chromadb"}
        )


class EmbeddingModelError(CyberSOPException):
    """Embedding model error"""
    
    def __init__(self, message: str = "Embedding model not available"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"service": "embedding_model"}
        )


class ValidationError(CyberSOPException):
    """Input validation error"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else {}
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class RateLimitExceeded(CyberSOPException):
    """Rate limit exceeded error"""
    
    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after": "60 seconds"}
        )


class DataProcessingError(CyberSOPException):
    """Data processing error"""
    
    def __init__(self, message: str = "Error processing data"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ScraperError(CyberSOPException):
    """Web scraping error"""
    
    def __init__(self, message: str = "Error scraping government portal"):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY
        )


def register_exception_handlers(app):
    """Register exception handlers with FastAPI app"""
    
    @app.exception_handler(CyberSOPException)
    async def cyber_sop_exception_handler(request: Request, exc: CyberSOPException):
        """Handle custom exceptions"""
        logger.error(
            f"CyberSOPException: {exc.message}",
            extra={
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path
            }
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "details": exc.details,
                "type": exc.__class__.__name__
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        logger.warning(f"Validation error: {errors}", extra={"path": request.url.path})
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation error",
                "details": errors
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions"""
        logger.warning(
            f"HTTP exception: {exc.detail}",
            extra={"status_code": exc.status_code, "path": request.url.path}
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        logger.error(
            f"Unexpected error: {str(exc)}",
            exc_info=True,
            extra={"path": request.url.path}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )
