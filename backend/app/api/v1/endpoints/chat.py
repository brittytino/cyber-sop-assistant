"""
Chat Endpoint - Main Conversational Interface
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import time
import asyncio

from app.models.schemas import ChatRequest, ChatResponse, OfficialLink, EmergencyContact
from app.models.enums import CrimeType
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.cache_service import cache_service
from app.services.classifier_service import classifier_service
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
        
        # Generate response using LLM
        llm_response = await llm_service.generate_sop(
            query=request.query,
            context_docs=context_docs,
            language=request.language.value
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
