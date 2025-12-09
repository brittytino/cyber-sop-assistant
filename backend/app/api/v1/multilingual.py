"""
API Router for Multilingual Chat and Translation
Handles language-aware endpoints for the SOP assistant using local Ollama
"""
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.local_ollama_service import local_ollama_service
from app.core.logging import logger

router = APIRouter(prefix="/api/v1/multilingual", tags=["Multilingual"])


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message")
    language: str = Field(default="en", description="Target language code")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Previous conversation messages"
    )


class SOPRequest(BaseModel):
    """SOP generation request model"""
    query: str = Field(..., description="User query about cybercrime reporting")
    language: str = Field(default="en", description="Target language code")
    category: Optional[str] = Field(None, description="Crime category filter")
    use_rag: bool = Field(default=True, description="Whether to use RAG")


class TranslationRequest(BaseModel):
    """Translation request model"""
    content: str = Field(..., description="Content to translate")
    target_language: str = Field(..., description="Target language code")
    context: Optional[str] = Field(None, description="Context about the content")


class LanguageInfo(BaseModel):
    """Language information model"""
    code: str
    name: str
    native_name: str


@router.post("/chat", response_model=Dict[str, Any])
async def chat_with_assistant(request: ChatRequest):
    """
    Chat with AI assistant in specified language using local Ollama
    
    Args:
        request: Chat request with message and language
        
    Returns:
        AI response in target language with metadata
    """
    try:
        response = await local_ollama_service.chat_with_language_awareness(
            message=request.message,
            language=request.language,
            conversation_history=request.conversation_history
        )

        return {
            "success": True,
            "response": response,
            "language": request.language,
            "timestamp": None  # Can add timestamp if needed
        }

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@router.post("/sop", response_model=Dict[str, Any])
async def generate_sop(request: SOPRequest):
    """
    Generate SOP guidance in specified language using local Ollama + RAG
    
    Args:
        request: SOP request with query and language
        
    Returns:
        Structured SOP response in target language
    """
    try:
        sop_response = await local_ollama_service.generate_sop_response(
            query=request.query,
            language=request.language,
            category=request.category,
            use_rag=request.use_rag
        )

        return {
            "success": True,
            "data": sop_response,
            "language": request.language,
            "query": request.query
        }

    except Exception as e:
        logger.error(f"SOP generation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"SOP generation failed: {str(e)}")


@router.post("/translate")
async def translate_content(request: TranslationRequest):
    """
    Translate content to target language using local Ollama
    
    Args:
        request: Translation request
        
    Returns:
        Translated content
    """
    try:
        translated = await local_ollama_service.translate_content(
            content=request.content,
            target_language=request.target_language,
            context=request.context
        )

        return {
            "success": True,
            "original": request.content,
            "translated": translated,
            "target_language": request.target_language
        }

    except Exception as e:
        logger.error(f"Translation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get("/languages", response_model=List[LanguageInfo])
async def get_supported_languages():
    """
    Get list of supported languages
    
    Returns:
        List of supported language information
    """
    languages_data = local_ollama_service.get_supported_languages()
    
    return [
        LanguageInfo(
            code=lang["code"],
            name=lang["name"],
            native_name=lang["native_name"]
        )
        for lang in languages_data
    ]


@router.get("/health")
async def check_service_health():
    """
    Check Ollama service health
    
    Returns:
        Service health status
    """
    try:
        health_status = await local_ollama_service.check_health()
        return {
            "success": True,
            "service": "local_ollama",
            **health_status
        }
    except Exception as e:
        logger.error(f"Health check error: {e}", exc_info=True)
        return {
            "success": False,
            "service": "local_ollama",
            "status": "error",
            "error": str(e)
        }

