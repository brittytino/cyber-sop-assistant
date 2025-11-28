"""
Pydantic Schemas for Request/Response Validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.enums import CrimeType, Language, Platform, EvidenceType, ComplaintStatus


# Chat Schemas
class ChatRequest(BaseModel):
    """Chat request schema"""
    query: str = Field(..., min_length=10, max_length=2000, description="User query about cybercrime")
    language: Language = Field(default=Language.ENGLISH, description="Response language")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    include_sources: bool = Field(default=True, description="Include source documents")
    
    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        """Sanitize query input"""
        return v.strip()


class OfficialLink(BaseModel):
    """Official link schema"""
    name: str
    url: str
    category: str
    description: Optional[str] = None


class EmergencyContact(BaseModel):
    """Emergency contact schema"""
    name: str
    number: str
    description: str
    available_24x7: bool = True


class ChatResponse(BaseModel):
    """Chat response schema"""
    request_id: str
    crime_type: Optional[CrimeType] = None
    immediate_actions: List[str]
    reporting_steps: List[str]
    evidence_checklist: List[str]
    official_links: List[OfficialLink]
    emergency_contacts: List[EmergencyContact]
    platform_specific: Optional[Dict[str, Any]] = None
    sources: Optional[List[str]] = None
    language: Language
    timestamp: datetime
    processing_time_ms: float


# Complaint Schemas
class ComplaintCreate(BaseModel):
    """Create complaint schema"""
    crime_type: CrimeType
    incident_date: datetime
    incident_description: str = Field(..., min_length=50, max_length=5000)
    amount_lost: Optional[float] = Field(None, ge=0)
    platform: Optional[Platform] = None
    suspect_details: Optional[str] = None
    victim_name: str = Field(..., min_length=2, max_length=100)
    victim_email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    victim_phone: str = Field(..., pattern=r"^\+?[\d\s-]{10,15}$")
    victim_address: str = Field(..., min_length=10, max_length=500)
    language: Language = Language.ENGLISH


class ComplaintResponse(BaseModel):
    """Complaint response schema"""
    complaint_id: str
    status: ComplaintStatus
    draft_text: str
    portal_url: str
    generated_at: datetime
    pdf_available: bool = True


# Evidence Schemas
class EvidenceItem(BaseModel):
    """Evidence item schema"""
    type: EvidenceType
    description: str
    collected: bool = False
    required: bool = True
    instructions: Optional[str] = None


class EvidenceChecklistResponse(BaseModel):
    """Evidence checklist response"""
    crime_type: CrimeType
    evidence_items: List[EvidenceItem]
    general_tips: List[str]
    storage_instructions: str


# Analytics Schemas
class UsageStats(BaseModel):
    """Usage statistics schema"""
    total_queries: int
    total_complaints_generated: int
    most_common_crime_types: List[Dict[str, Any]]
    language_distribution: Dict[str, int]
    average_response_time_ms: float
    success_rate: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, bool]
    document_count: int
    uptime_seconds: float


# Admin Schemas
class DataRefreshRequest(BaseModel):
    """Data refresh request"""
    sources: List[str] = Field(default=["all"], description="Data sources to refresh")
    force: bool = Field(default=False, description="Force refresh even if recent")


class DataRefreshResponse(BaseModel):
    """Data refresh response"""
    task_id: str
    status: str
    message: str
    estimated_time_minutes: int
