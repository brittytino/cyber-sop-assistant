"""
Progress Tracking Endpoints
Track user progress through complaint process
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from datetime import datetime

from app.models.progress import (
    UserProgress, ProgressUpdate, ProgressStage, StageStatus,
    EvidenceChecklist, ComplaintTracking, ComplaintTrackingStatus
)
from app.api.v1.endpoints.auth import get_current_user
from app.core.logging import logger

router = APIRouter()

# In-memory progress storage (use database in production)
_progress_store: dict = {}
_complaint_tracking: dict = {}


@router.get("/{session_id}", response_model=UserProgress)
async def get_progress(
    session_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get current progress for a session
    
    Works for both anonymous and authenticated users
    """
    if session_id not in _progress_store:
        # Create new progress
        progress = UserProgress(
            session_id=session_id,
            user_id=current_user['user_id'] if current_user else None,
            current_stage=ProgressStage.DESCRIBE_ISSUE,
            current_stage_status=StageStatus.IN_PROGRESS,
            timeline=[],
            started_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            completion_percentage=0,
            is_anonymous=current_user is None
        )
        _progress_store[session_id] = progress
    
    return _progress_store[session_id]


@router.post("/{session_id}/update", response_model=UserProgress)
async def update_progress(
    session_id: str,
    update: ProgressUpdate,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Update progress for a session
    
    Called by frontend as user moves through steps
    """
    if session_id not in _progress_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress session not found"
        )
    
    progress = _progress_store[session_id]
    progress.current_stage = update.stage
    progress.current_stage_status = update.status
    progress.updated_at = datetime.utcnow()
    
    # Calculate completion
    progress.completion_percentage = _calculate_completion(update.stage, update.status)
    
    logger.info(f"Progress updated: {session_id} -> {update.stage.value}")
    
    return progress


@router.get("/complaint/{complaint_id}/track", response_model=ComplaintTracking)
async def track_complaint(
    complaint_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Track status of a submitted complaint
    
    Returns portal status and updates
    """
    if complaint_id not in _complaint_tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint tracking not found"
        )
    
    tracking = _complaint_tracking[complaint_id]
    
    # Verify ownership
    if current_user and tracking.user_id != current_user['user_id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot track complaints you don't own"
        )
    
    return tracking


def _calculate_completion(stage: ProgressStage, status: StageStatus) -> int:
    """Calculate completion percentage based on stage"""
    stage_weights = {
        ProgressStage.DESCRIBE_ISSUE: 10,
        ProgressStage.AI_ANALYSIS: 20,
        ProgressStage.GUIDANCE_RECEIVED: 30,
        ProgressStage.EVIDENCE_COLLECTION: 40,
        ProgressStage.COMPLAINT_DRAFTED: 60,
        ProgressStage.USER_REVIEW: 70,
        ProgressStage.READY_TO_FILE: 80,
        ProgressStage.FILING_IN_PROGRESS: 90,
        ProgressStage.COMPLAINT_SUBMITTED: 95,
        ProgressStage.ACKNOWLEDGMENT_RECEIVED: 100,
    }
    
    base = stage_weights.get(stage, 0)
    
    if status == StageStatus.COMPLETED:
        return base
    elif status == StageStatus.IN_PROGRESS:
        return max(0, base - 5)
    else:
        return max(0, base - 10)
