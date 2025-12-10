"""
Chat Endpoint - Main Conversational Interface
ENHANCED with Local Ollama + RAG for Multilingual Cybercrime Guidance
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import time
import asyncio

from app.models.schemas import ChatRequest, ChatResponse, OfficialLink, EmergencyContact
from app.models.enums import CrimeType
from app.services.local_ollama_service import local_ollama_service
from app.services.rag_service import rag_service
from app.services.cache_service import cache_service
from app.services.classifier_service import classifier_service
from app.services.enhanced_query_service import enhanced_query_service
from app.repositories.analytics_repository import AnalyticsRepository
from app.core.dependencies import (
    get_analytics_repository,
    verify_ollama_connection,
    verify_rag_loaded
)
from app.core.logging import logger
from app.core.security import generate_request_id
from app.utils.constants import EMERGENCY_CONTACTS, OFFICIAL_LINKS

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    analytics_repo: AnalyticsRepository = Depends(get_analytics_repository),
    _: None = Depends(verify_ollama_connection),
    __: None = Depends(verify_rag_loaded)
):
    """
    Main chat endpoint for cybercrime SOP queries
    
    Process:
    1. Check cache for existing response
    2. Classify crime type from query
    3. Retrieve relevant documents via RAG
    4. Generate response using LLM
    5. Cache and log response
    """
    request_id = generate_request_id()
    start_time = time.time()
    
    logger.info(f"[{request_id}] Processing chat request: {request.query[:100]}...")
    
    try:
        # Check cache first
        cached_response = cache_service.get(request.query, request.language.value)
        if cached_response:
            logger.info(f"[{request_id}] Returning cached response")
            cached_response["request_id"] = request_id
            cached_response["timestamp"] = datetime.utcnow()
            return ChatResponse(**cached_response)
        
        # Classify crime type
        crime_type = await classifier_service.classify(request.query)
        logger.info(f"[{request_id}] Detected crime type: {crime_type}")
        
        # Retrieve relevant documents
        context_docs = await rag_service.retrieve(
            query=request.query,
            top_k=5
        )
        logger.info(f"[{request_id}] Retrieved {len(context_docs)} documents")
        
        # Generate response using Local Ollama with RAG
        llm_response = await local_ollama_service.generate_sop_response(
            query=request.query,
            language=request.language.value,
            category=crime_type,
            use_rag=True
        )
        
        # Build structured response
        response = ChatResponse(
            request_id=request_id,
            crime_type=crime_type,
            immediate_actions=llm_response.get("immediate_actions", []),
            reporting_steps=llm_response.get("reporting_steps", []),
            evidence_checklist=llm_response.get("evidence_checklist", []),
            official_links=[
                OfficialLink(**link) for link in llm_response.get("official_links", [])
            ],
            emergency_contacts=[
                EmergencyContact(**contact) for contact in llm_response.get("emergency_contacts", [])
            ],
            platform_specific=llm_response.get("platform_specific"),
            sources=llm_response.get("sources") if request.include_sources else None,
            language=request.language,
            timestamp=datetime.utcnow(),
            processing_time_ms=round((time.time() - start_time) * 1000, 2)
        )
        
        # Cache response
        cache_service.set(
            request.query,
            request.language.value,
            response.dict(exclude={"request_id", "timestamp"})
        )
        
        # Log query analytics
        await analytics_repo.log_query(
            request_id=request_id,
            query=request.query,
            language=request.language.value,
            crime_type=crime_type,
            response_time_ms=response.processing_time_ms,
            success=True
        )
        
        logger.info(f"[{request_id}] Response generated successfully ({response.processing_time_ms}ms)")
        
        return response
        
    except Exception as e:
        processing_time = round((time.time() - start_time) * 1000, 2)
        logger.error(f"[{request_id}] Error processing chat: {e}", exc_info=True)
        
        # Log failed query
        await analytics_repo.log_query(
            request_id=request_id,
            query=request.query,
            language=request.language.value,
            crime_type=None,
            response_time_ms=processing_time,
            success=False,
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get("/suggestions")
async def get_suggestions():
    """Get sample queries for users"""
    return {
        "suggestions": [
            {
                "category": "Financial Fraud",
                "queries": [
                    "I lost money in a UPI scam, how do I report it?",
                    "Someone did unauthorized transactions from my bank account",
                    "I got scammed in a fake investment scheme"
                ]
            },
            {
                "category": "Social Media",
                "queries": [
                    "Someone created a fake Instagram profile using my photos",
                    "My Facebook account has been hacked",
                    "I'm being harassed on WhatsApp"
                ]
            },
            {
                "category": "Identity Theft",
                "queries": [
                    "Someone is using my Aadhaar for fraud",
                    "Fake KYC is being done in my name",
                    "My SIM card was swapped without permission"
                ]
            }
        ]
    }


@router.post("/chat/v2", summary="Enhanced Chat Endpoint with Multi-Intent Detection")
async def chat_v2(
    request: ChatRequest,
    analytics_repo: AnalyticsRepository = Depends(get_analytics_repository),
    _: None = Depends(verify_ollama_connection),
    __: None = Depends(verify_rag_loaded)
):
    """
    ENHANCED chat endpoint with production-ready features:
    - Multi-intent detection (multiple crime types in one query)
    - 30+ crime type classification
    - Multi-language support (Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati)
    - Timeline-based action plans (NOW, 24H, 7D, ONGOING)
    - Evidence checklists
    - Official verified links (.gov.in)
    - Comprehensive disclaimers
    - Response time < 3 seconds
    """
    request_id = generate_request_id()
    start_time = time.time()
    
    logger.info(f"[{request_id}] Processing enhanced chat request: {request.query[:100]}...")
    
    try:
        # Check cache first
        cache_key = f"v2_{request.query}_{request.language.value}"
        cached_response = cache_service.get(cache_key)
        if cached_response:
            logger.info(f"[{request_id}] Returning cached enhanced response")
            cached_response["request_id"] = request_id
            cached_response["timestamp"] = datetime.utcnow().isoformat()
            return cached_response
        
        # Process query with enhanced service
        enhanced_response = await enhanced_query_service.process_query(
            query=request.query,
            language=request.language.value,
            user_context={
                "request_id": request_id,
                "include_sources": request.include_sources
            }
        )
        
        # Add request metadata
        enhanced_response["request_id"] = request_id
        
        # Cache response
        if enhanced_response.get("success"):
            cache_service.set(cache_key, enhanced_response)
        
        # Log query analytics
        await analytics_repo.log_query(
            request_id=request_id,
            query=request.query,
            language=request.language.value,
            crime_type=enhanced_response.get("detected_crime_type", {}).get("code"),
            response_time_ms=enhanced_response.get("response_time_ms", 0),
            success=enhanced_response.get("success", False),
            error_message=enhanced_response.get("error") if not enhanced_response.get("success") else None
        )
        
        logger.info(f"[{request_id}] Enhanced response generated ({enhanced_response.get('response_time_ms')}ms)")
        
        return enhanced_response
        
    except Exception as e:
        processing_time = round((time.time() - start_time) * 1000, 2)
        logger.error(f"[{request_id}] Error in enhanced chat: {e}", exc_info=True)
        
        # Log failed query
        await analytics_repo.log_query(
            request_id=request_id,
            query=request.query,
            language=request.language.value,
            crime_type=None,
            response_time_ms=processing_time,
            success=False,
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process enhanced query: {str(e)}"
        )
