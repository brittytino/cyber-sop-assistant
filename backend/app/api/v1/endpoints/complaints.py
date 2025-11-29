"""
Complaints Endpoint - Generate Complaint Drafts
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from app.models.schemas import ComplaintCreate, ComplaintResponse
from app.models.enums import ComplaintStatus
from app.repositories.complaint_repository import ComplaintRepository
from app.core.dependencies import get_complaint_repository
from app.core.logging import logger
from app.core.security import generate_request_id

router = APIRouter()


@router.post("/generate", response_model=ComplaintResponse)
async def generate_complaint(
    complaint: ComplaintCreate,
    repo: ComplaintRepository = Depends(get_complaint_repository)
):
    """
    Generate complaint draft for cybercrime portal
    
    Creates a structured complaint text that can be copied
    to the official portal at cybercrime.gov.in
    """
    complaint_id = f"DRAFT-{generate_request_id()[:12].upper()}"
    
    logger.info(f"Generating complaint draft: {complaint_id}")
    
    try:
        # Generate complaint text
        draft_text = _generate_complaint_text(complaint)
        
        # Save to database
        db_complaint = await repo.create_complaint(
            complaint_id=complaint_id,
            crime_type=complaint.crime_type,
            incident_date=complaint.incident_date,
            incident_description=complaint.incident_description,
            amount_lost=complaint.amount_lost,
            victim_name=complaint.victim_name,
            victim_email=complaint.victim_email,
            victim_phone=complaint.victim_phone,
            victim_address=complaint.victim_address,
            draft_text=draft_text,
            language=complaint.language
        )
        
        response = ComplaintResponse(
            complaint_id=complaint_id,
            status=ComplaintStatus.DRAFT,
            draft_text=draft_text,
            portal_url="https://cybercrime.gov.in",
            generated_at=datetime.utcnow(),
            pdf_available=True
        )
        
        logger.info(f"Complaint draft generated: {complaint_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating complaint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate complaint: {str(e)}"
        )


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: str,
    repo: ComplaintRepository = Depends(get_complaint_repository)
):
    """Retrieve previously generated complaint"""
    complaint = await repo.get_by_complaint_id(complaint_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint {complaint_id} not found"
        )
    
    return ComplaintResponse(
        complaint_id=complaint.complaint_id,
        status=complaint.status,
        draft_text=complaint.draft_text,
        portal_url="https://cybercrime.gov.in",
        generated_at=complaint.created_at,
        pdf_available=True
    )


def _generate_complaint_text(complaint: ComplaintCreate) -> str:
    """Generate formatted complaint text"""
    
    text = f"""CYBERCRIME COMPLAINT DRAFT
Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

CRIME TYPE: {complaint.crime_type.value.replace('_', ' ').title()}
INCIDENT DATE: {complaint.incident_date.strftime('%Y-%m-%d')}

VICTIM DETAILS:
Name: {complaint.victim_name}
Email: {complaint.victim_email}
Phone: {complaint.victim_phone}
Address: {complaint.victim_address}

INCIDENT DESCRIPTION:
{complaint.incident_description}
"""
    
    if complaint.amount_lost:
        text += f"\nFINANCIAL LOSS: ₹{complaint.amount_lost:,.2f}\n"
    
    if complaint.platform:
        text += f"\nPLATFORM: {complaint.platform.value.title()}\n"
    
    if complaint.suspect_details:
        text += f"\nSUSPECT DETAILS:\n{complaint.suspect_details}\n"
    
    text += """
INSTRUCTIONS:
1. Copy the above text
2. Visit https://cybercrime.gov.in
3. Click "File a Complaint"
4. Register/Login with your mobile number
5. Select the appropriate crime category
6. Paste this draft in the incident description
7. Upload all evidence (screenshots, transaction IDs, etc.)
8. Submit and save your acknowledgment number

EMERGENCY: For financial fraud, call 1930 immediately.
"""
    
    return text
