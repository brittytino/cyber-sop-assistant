"""
Evidence Endpoint - Evidence Collection Checklist
"""
from fastapi import APIRouter, Depends, Query
from typing import List

from app.models.schemas import EvidenceChecklistResponse, EvidenceItem
from app.models.enums import CrimeType, EvidenceType
from app.core.logging import logger

router = APIRouter()


@router.get("/checklist", response_model=EvidenceChecklistResponse)
async def get_evidence_checklist(
    crime_type: CrimeType = Query(..., description="Type of cybercrime")
):
    """
    Get evidence collection checklist for specific crime type
    
    Returns tailored checklist based on crime category
    """
    logger.info(f"Generating evidence checklist for: {crime_type}")
    
    # Base evidence items (common for all)
    base_items = [
        EvidenceItem(
            type=EvidenceType.SCREENSHOT,
            description="Screenshots of all relevant conversations, posts, or transactions",
            collected=False,
            required=True,
            instructions="Take full-page screenshots with timestamps visible"
        ),
        EvidenceItem(
            type=EvidenceType.CHAT_LOG,
            description="Complete chat/message history with the fraudster",
            collected=False,
            required=True,
            instructions="Export chat as text file or PDF if possible"
        )
    ]
    
    # Crime-specific evidence
    specific_items = _get_crime_specific_evidence(crime_type)
    
    evidence_items = base_items + specific_items
    
    general_tips = [
        "Do NOT delete any messages or evidence",
        "Take screenshots immediately before reporting",
        "Note down dates and times of all incidents",
        "Keep original files, don't edit or crop",
        "Store evidence in multiple locations (cloud + local)"
    ]
    
    storage_instructions = """
Store all evidence in a dedicated folder with clear naming:
- Format: YYYYMMDD_CrimeType_ItemDescription.png/pdf
- Example: 20251129_UPI_Fraud_Transaction_Screenshot.png
- Keep both originals and organized copies
- Backup to Google Drive or similar cloud storage
"""
    
    return EvidenceChecklistResponse(
        crime_type=crime_type,
        evidence_items=evidence_items,
        general_tips=general_tips,
        storage_instructions=storage_instructions
    )


def _get_crime_specific_evidence(crime_type: CrimeType) -> List[EvidenceItem]:
    """Get crime-specific evidence requirements"""
    
    evidence_map = {
        CrimeType.FINANCIAL_FRAUD: [
            EvidenceItem(
                type=EvidenceType.TRANSACTION_ID,
                description="UPI transaction ID / Reference number",
                collected=False,
                required=True,
                instructions="Found in transaction details of your payment app"
            ),
            EvidenceItem(
                type=EvidenceType.BANK_STATEMENT,
                description="Bank statement showing unauthorized transactions",
                collected=False,
                required=True,
                instructions="Download from net banking (last 30 days)"
            ),
            EvidenceItem(
                type=EvidenceType.PHONE_NUMBER,
                description="Fraudster's phone number or UPI ID",
                collected=False,
                required=True,
                instructions="Note exact number/ID used for transaction"
            )
        ],
        
        CrimeType.UPI_FRAUD: [
            EvidenceItem(
                type=EvidenceType.TRANSACTION_ID,
                description="UPI transaction ID (UTR number)",
                collected=False,
                required=True,
                instructions="12-digit number in transaction details"
            ),
            EvidenceItem(
                type=EvidenceType.SCREENSHOT,
                description="Screenshot of UPI app showing transaction",
                collected=False,
                required=True,
                instructions="Show sender/receiver UPI ID, amount, date/time"
            ),
            EvidenceItem(
                type=EvidenceType.PHONE_NUMBER,
                description="Receiver's UPI ID or phone number",
                collected=False,
                required=True
            )
        ],
        
        CrimeType.SOCIAL_MEDIA_HACK: [
            EvidenceItem(
                type=EvidenceType.URL,
                description="URL of your hacked account",
                collected=False,
                required=True,
                instructions="Full profile URL (e.g., facebook.com/username)"
            ),
            EvidenceItem(
                type=EvidenceType.SCREENSHOT,
                description="Screenshots of unauthorized posts/messages",
                collected=False,
                required=True
            ),
            EvidenceItem(
                type=EvidenceType.EMAIL,
                description="Account recovery emails from platform",
                collected=False,
                required=False,
                instructions="Check spam folder too"
            )
        ],
        
        CrimeType.FAKE_PROFILE: [
            EvidenceItem(
                type=EvidenceType.URL,
                description="URL of fake profile",
                collected=False,
                required=True,
                instructions="Copy exact profile link"
            ),
            EvidenceItem(
                type=EvidenceType.SCREENSHOT,
                description="Screenshots of fake profile showing your photos",
                collected=False,
                required=True,
                instructions="Capture profile picture, posts, and about section"
            )
        ]
    }
    
    return evidence_map.get(crime_type, [])
