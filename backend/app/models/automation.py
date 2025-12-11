"""
Automated Complaint Filing Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AutomationStatus(str, Enum):
    """Status of automated complaint filing"""
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    AWAITING_OTP = "awaiting_otp"
    OTP_SUBMITTED = "otp_submitted"
    FORM_FILLING = "form_filling"
    EVIDENCE_UPLOAD = "evidence_upload"
    SUBMITTED = "submitted"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    MANUAL_INTERVENTION_REQUIRED = "manual_intervention_required"


class PortalType(str, Enum):
    """Supported complaint portals"""
    CYBERCRIME_GOV = "cybercrime_gov"
    RBI_OMBUDSMAN = "rbi_ombudsman"
    CERT_IN = "cert_in"
    STATE_CYBER_CELL = "state_cyber_cell"
    CONSUMER_FORUM = "consumer_forum"


class EvidenceFile(BaseModel):
    """Evidence file for upload"""
    file_id: str
    filename: str
    file_type: str
    file_size: int
    mime_type: str
    upload_status: str
    checksum: str


class AutomatedFilingRequest(BaseModel):
    """Request to automate complaint filing"""
    complaint_id: str = Field(..., description="ID of the generated complaint draft")
    portal: PortalType = Field(default=PortalType.CYBERCRIME_GOV)
    user_id: str = Field(..., description="Authenticated user ID")
    
    # User details for form filling (from profile or override)
    use_profile_details: bool = Field(default=True)
    override_details: Optional[Dict[str, Any]] = None
    
    # Evidence files to upload
    evidence_files: List[str] = Field(default=[], description="List of file IDs to upload")
    
    # Filing preferences
    priority: str = Field(default="normal", pattern=r'^(low|normal|high|urgent)$')
    notify_on_status: bool = Field(default=True)
    retry_on_failure: bool = Field(default=True)
    max_retries: int = Field(default=3, ge=1, le=5)


class AutomatedFilingResponse(BaseModel):
    """Response for automated filing request"""
    filing_id: str
    complaint_id: str
    portal: PortalType
    status: AutomationStatus
    message: str
    estimated_completion_minutes: Optional[int] = None
    tracking_url: Optional[str] = None
    created_at: datetime


class FilingStatusUpdate(BaseModel):
    """Status update for automated filing"""
    filing_id: str
    complaint_id: str
    status: AutomationStatus
    message: str
    portal_reference: Optional[str] = None  # Acknowledgment number from portal
    portal_tracking_url: Optional[str] = None
    progress_percentage: int = Field(ge=0, le=100)
    current_step: Optional[str] = None
    error_details: Optional[str] = None
    updated_at: datetime
    next_action_required: Optional[str] = None


class PortalOTPRequest(BaseModel):
    """Request for portal OTP verification"""
    filing_id: str
    otp: str = Field(..., min_length=4, max_length=8)


class FilingHistory(BaseModel):
    """History of automated filings for a user"""
    filings: List[FilingStatusUpdate]
    total_count: int
    successful_count: int
    failed_count: int
    pending_count: int


class PortalCredentials(BaseModel):
    """Portal credentials (encrypted storage)"""
    portal: PortalType
    phone: str
    email: Optional[str] = None
    # Note: Never store portal passwords, use OTP flow


class AutomationMetrics(BaseModel):
    """Metrics for automation service"""
    total_filings_today: int
    successful_filings_today: int
    average_completion_time_minutes: float
    portal_availability: Dict[str, bool]
    queue_length: int
