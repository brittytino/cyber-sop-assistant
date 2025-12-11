"""
Progress and Timeline Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ProgressStage(str, Enum):
    """Stages in the complaint process"""
    DESCRIBE_ISSUE = "describe_issue"
    AI_ANALYSIS = "ai_analysis"
    GUIDANCE_RECEIVED = "guidance_received"
    EVIDENCE_COLLECTION = "evidence_collection"
    COMPLAINT_DRAFTED = "complaint_drafted"
    USER_REVIEW = "user_review"
    READY_TO_FILE = "ready_to_file"
    FILING_IN_PROGRESS = "filing_in_progress"
    COMPLAINT_SUBMITTED = "complaint_submitted"
    ACKNOWLEDGMENT_RECEIVED = "acknowledgment_received"
    FOLLOW_UP = "follow_up"
    RESOLVED = "resolved"


class StageStatus(str, Enum):
    """Status of each stage"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    NEEDS_ACTION = "needs_action"
    ERROR = "error"


class TimelineStep(BaseModel):
    """Single step in the timeline"""
    step_id: str
    stage: ProgressStage
    title: str
    title_local: Optional[str] = None
    description: str
    description_local: Optional[str] = None
    status: StageStatus
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    actions: List[str] = Field(default=[])
    data: Optional[Dict[str, Any]] = None
    order: int


class UserProgress(BaseModel):
    """User's progress through the complaint process"""
    session_id: str
    user_id: Optional[str] = None  # None for anonymous users
    complaint_id: Optional[str] = None
    current_stage: ProgressStage
    current_stage_status: StageStatus
    timeline: List[TimelineStep]
    started_at: datetime
    updated_at: datetime
    estimated_completion_minutes: Optional[int] = None
    completion_percentage: int = Field(ge=0, le=100)
    
    # Context
    crime_type: Optional[str] = None
    language: str = "en"
    is_anonymous: bool = True
    
    # Next actions
    next_steps: List[str] = Field(default=[])
    pending_user_actions: List[str] = Field(default=[])


class ProgressUpdate(BaseModel):
    """Update progress for a session"""
    session_id: str
    stage: ProgressStage
    status: StageStatus
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


# Evidence Checklist Models
class EvidenceItem(BaseModel):
    """Single evidence item"""
    item_id: str
    name: str
    name_local: Optional[str] = None
    description: str
    description_local: Optional[str] = None
    instructions: str
    instructions_local: Optional[str] = None
    required: bool = True
    collected: bool = False
    file_id: Optional[str] = None  # If uploaded
    priority: int = Field(ge=1, le=5)
    category: str  # "screenshot", "document", "transaction", "communication"


class EvidenceChecklist(BaseModel):
    """Evidence checklist for a crime type"""
    crime_type: str
    checklist_id: str
    title: str
    title_local: Optional[str] = None
    description: str
    description_local: Optional[str] = None
    items: List[EvidenceItem]
    general_tips: List[str]
    general_tips_local: Optional[List[str]] = None
    storage_instructions: str
    storage_instructions_local: Optional[str] = None
    total_items: int
    required_items: int
    collected_items: int = 0


class EvidenceChecklistByType(BaseModel):
    """Evidence requirements mapped by crime type"""
    crime_type: str
    required_evidence: List[EvidenceItem]
    recommended_evidence: List[EvidenceItem]
    platform_specific: Dict[str, List[EvidenceItem]]
    tips: List[str]


# Complaint Status Tracking
class ComplaintTrackingStatus(str, Enum):
    """Status for complaint tracking"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    UNDER_INVESTIGATION = "under_investigation"
    ADDITIONAL_INFO_REQUIRED = "additional_info_required"
    TRANSFERRED = "transferred"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


class ComplaintStatusUpdate(BaseModel):
    """Status update for a complaint"""
    complaint_id: str
    portal_reference: Optional[str] = None
    status: ComplaintTrackingStatus
    message: str
    message_local: Optional[str] = None
    updated_at: datetime
    source: str  # "portal", "manual", "system"
    next_steps: List[str] = Field(default=[])
    attachments: List[str] = Field(default=[])


class ComplaintTracking(BaseModel):
    """Full tracking information for a complaint"""
    complaint_id: str
    user_id: Optional[str] = None
    portal_reference: Optional[str] = None
    portal: str
    crime_type: str
    current_status: ComplaintTrackingStatus
    status_history: List[ComplaintStatusUpdate]
    created_at: datetime
    last_checked: datetime
    auto_check_enabled: bool = True
    notifications_enabled: bool = True


class SafetyPrivacyMessage(BaseModel):
    """Safety and privacy messaging"""
    message_id: str
    title: str
    title_local: Optional[str] = None
    content: str
    content_local: Optional[str] = None
    message_type: str  # "info", "warning", "reassurance", "legal"
    display_location: str  # "chat", "form", "dashboard", "global"
    priority: int = Field(ge=1, le=10)
    dismissible: bool = True
    icon: Optional[str] = None


class PrivacySettings(BaseModel):
    """User privacy settings"""
    user_id: Optional[str] = None
    session_id: str
    data_retention_days: int = Field(default=90)
    allow_analytics: bool = False
    allow_location: bool = False
    location_consent_given: bool = False
    share_anonymized_data: bool = False
    delete_on_completion: bool = False
