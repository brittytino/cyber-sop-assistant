"""
Complaint Repository - Complaint Database Operations
"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.repositories.base import BaseRepository
from app.models.database import Complaint
from app.models.enums import CrimeType, ComplaintStatus, Language
from app.core.logging import logger


class ComplaintRepository(BaseRepository[Complaint]):
    """Repository for complaint operations"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Complaint, session)
    
    async def create_complaint(
        self,
        complaint_id: str,
        crime_type: CrimeType,
        incident_date: datetime,
        incident_description: str,
        victim_name: str,
        victim_email: str,
        victim_phone: str,
        victim_address: str,
        draft_text: str,
        language: Language,
        amount_lost: Optional[float] = None
    ) -> Complaint:
        """Create a new complaint"""
        return await self.create(
            complaint_id=complaint_id,
            crime_type=crime_type,
            incident_date=incident_date,
            incident_description=incident_description,
            victim_name=victim_name,
            victim_email=victim_email,
            victim_phone=victim_phone,
            victim_address=victim_address,
            draft_text=draft_text,
            language=language,
            amount_lost=amount_lost,
            status=ComplaintStatus.DRAFT
        )
    
    async def get_by_complaint_id(self, complaint_id: str) -> Optional[Complaint]:
        """Get complaint by complaint_id"""
        try:
            result = await self.session.execute(
                select(Complaint).where(Complaint.complaint_id == complaint_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching complaint by ID: {e}")
            return None
    
    async def get_by_email(self, email: str) -> List[Complaint]:
        """Get all complaints by victim email"""
        try:
            result = await self.session.execute(
                select(Complaint).where(Complaint.victim_email == email)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching complaints by email: {e}")
            return []
    
    async def get_by_crime_type(self, crime_type: CrimeType) -> List[Complaint]:
        """Get all complaints by crime type"""
        try:
            result = await self.session.execute(
                select(Complaint).where(Complaint.crime_type == crime_type)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching complaints by crime type: {e}")
            return []
    
    async def update_status(self, complaint_id: str, status: ComplaintStatus) -> bool:
        """Update complaint status"""
        try:
            complaint = await self.get_by_complaint_id(complaint_id)
            if complaint:
                complaint.status = status
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating complaint status: {e}")
            return False
