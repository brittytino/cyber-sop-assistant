"""
Analytics Endpoint - Usage Statistics
"""
from fastapi import APIRouter, Depends

from app.models.schemas import UsageStats
from app.repositories.analytics_repository import AnalyticsRepository
from app.core.dependencies import get_analytics_repository
from app.core.logging import logger

router = APIRouter()


@router.get("/stats", response_model=UsageStats)
async def get_usage_stats(
    repo: AnalyticsRepository = Depends(get_analytics_repository)
):
    """
    Get application usage statistics
    
    Returns:
    - Total queries processed
    - Crime type distribution
    - Language usage
    - Performance metrics
    """
    logger.info("Fetching usage statistics")
    
    stats = await repo.get_statistics()
    
    return UsageStats(**stats)
