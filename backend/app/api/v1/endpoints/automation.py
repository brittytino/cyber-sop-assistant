"""
Automation Endpoints
API for automated complaint filing
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.services.automation_service import automation_service
from app.api.v1.endpoints.auth import require_auth, get_current_user
from app.models.automation import (
    AutomatedFilingRequest, AutomatedFilingResponse,
    FilingStatusUpdate, FilingHistory, PortalOTPRequest
)
from app.core.logging import logger

router = APIRouter()


@router.post("/file", response_model=AutomatedFilingResponse)
async def automate_complaint_filing(
    request: AutomatedFilingRequest,
    user: dict = Depends(require_auth)
):
    """
    Queue complaint for automated filing on official portal
    
    Requirements:
    - User must be authenticated
    - Complaint draft must exist
    - User profile must have required details
    
    Process:
    1. Validates request and user eligibility
    2. Queues filing for background processing
    3. Returns filing ID for status tracking
    4. Automation runs asynchronously
    5. User receives notifications on status changes
    """
    # Verify user owns this complaint
    if request.user_id != user['user_id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only file your own complaints"
        )
    
    # Get user data for form filling
    user_data = {
        "name": user.get('name'),
        "phone": user.get('phone'),
        "email": user.get('email'),
        "address": user.get('address'),
        "city": user.get('city'),
        "state": user.get('state'),
        "pincode": user.get('pincode')
    }
    
    # Apply overrides if provided
    if not request.use_profile_details and request.override_details:
        user_data.update(request.override_details)
    
    # Validate required fields
    required = ['name', 'phone', 'address']
    missing = [f for f in required if not user_data.get(f)]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(missing)}. Please complete your profile."
        )
    
    # TODO: Fetch complaint data from database
    complaint_data = {
        "complaint_id": request.complaint_id,
        # Populated from complaint database
    }
    
    logger.info(f"User {user['user_id']} requested automated filing for {request.complaint_id}")
    
    return await automation_service.queue_filing(
        request=request,
        user_data=user_data,
        complaint_data=complaint_data
    )


@router.get("/status/{filing_id}", response_model=FilingStatusUpdate)
async def get_filing_status(
    filing_id: str,
    user: dict = Depends(require_auth)
):
    """
    Get current status of an automated filing
    
    Returns:
    - Current automation status
    - Progress percentage
    - Portal reference (if submitted)
    - Error details (if failed)
    """
    status_update = await automation_service.get_filing_status(filing_id)
    
    if not status_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filing not found"
        )
    
    return status_update


@router.get("/history", response_model=FilingHistory)
async def get_filing_history(
    user: dict = Depends(require_auth)
):
    """
    Get all automated filings for current user
    
    Returns summary and list of all filings with status
    """
    return await automation_service.get_user_filings(user['user_id'])


@router.post("/otp/{filing_id}")
async def submit_portal_otp(
    filing_id: str,
    otp_request: PortalOTPRequest,
    user: dict = Depends(require_auth)
):
    """
    Submit OTP for portal authentication during automation
    
    When automation reaches the OTP step, user provides the OTP
    received on their phone from the official portal
    """
    status_update = await automation_service.get_filing_status(filing_id)
    
    if not status_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filing not found"
        )
    
    # TODO: Pass OTP to automation handler
    logger.info(f"Portal OTP received for filing {filing_id}")
    
    return {
        "success": True,
        "message": "OTP submitted. Continuing with automation."
    }


@router.post("/cancel/{filing_id}")
async def cancel_filing(
    filing_id: str,
    user: dict = Depends(require_auth)
):
    """
    Cancel a pending automated filing
    
    Can only cancel filings that haven't started processing
    """
    success = await automation_service.cancel_filing(filing_id, user['user_id'])
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel this filing. It may have already started or doesn't exist."
        )
    
    return {
        "success": True,
        "message": "Filing cancelled successfully"
    }


@router.get("/portals")
async def get_supported_portals():
    """
    Get list of supported portals for automated filing
    
    Returns portal information and requirements
    """
    return {
        "portals": [
            {
                "id": "cybercrime_gov",
                "name": "National Cybercrime Portal",
                "url": "https://cybercrime.gov.in",
                "description": "Official portal for reporting all types of cybercrimes in India",
                "supported": True,
                "requirements": ["phone", "name", "address"],
                "crime_types": [
                    "financial_fraud", "upi_fraud", "social_media_hack",
                    "identity_theft", "harassment", "sextortion", "phishing"
                ],
                "estimated_time_minutes": 5,
                "success_rate": 0.95
            },
            {
                "id": "rbi_ombudsman",
                "name": "RBI Ombudsman",
                "url": "https://cms.rbi.org.in",
                "description": "For banking and financial service complaints",
                "supported": False,
                "requirements": ["phone", "name", "bank_details"],
                "crime_types": ["banking_fraud", "card_fraud"],
                "estimated_time_minutes": 10,
                "coming_soon": True
            },
            {
                "id": "women_child",
                "name": "Women & Child Cybercrime",
                "url": "https://cybercrime.gov.in/Webform/Womenchild.aspx",
                "description": "Specialized portal for crimes against women and children",
                "supported": False,
                "requirements": ["phone", "name"],
                "crime_types": ["harassment", "sextortion", "cyberbullying"],
                "coming_soon": True
            }
        ]
    }
