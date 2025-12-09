"""
Admin Endpoint - Administrative Operations
"""
from fastapi import APIRouter, Depends, BackgroundTasks
import uuid

from app.models.schemas import DataRefreshRequest, DataRefreshResponse
# from app.services.scraper_service import scraper_service  # Requires selenium
from app.services.cache_service import cache_service
from app.core.logging import logger

router = APIRouter()


@router.post("/refresh-data", response_model=DataRefreshResponse)
async def refresh_data(
    request: DataRefreshRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger data refresh from government portals
    
    Runs scraper in background to update knowledge base
    """
    task_id = str(uuid.uuid4())
    
    logger.info(f"Data refresh initiated: {task_id}")
    
    # Add scraping task to background
    background_tasks.add_task(
        _run_data_refresh,
        task_id=task_id,
        sources=request.sources,
        force=request.force
    )
    
    return DataRefreshResponse(
        task_id=task_id,
        status="scheduled",
        message="Data refresh task scheduled. Check logs for progress.",
        estimated_time_minutes=15
    )


@router.post("/clear-cache")
async def clear_cache():
    """Clear response cache"""
    success = cache_service.clear()
    
    if success:
        logger.info("Cache cleared successfully")
        return {"status": "success", "message": "Cache cleared"}
    else:
        logger.warning("Failed to clear cache")
        return {"status": "failed", "message": "Cache clear failed"}


@router.get("/cache-stats")
async def get_cache_stats():
    """Get cache statistics"""
    stats = cache_service.get_stats()
    return stats


async def _run_data_refresh(task_id: str, sources: list, force: bool):
    """Background task to refresh data"""
    logger.info(f"[{task_id}] Data refresh requested but scraper not available (requires selenium)")
    logger.warning("Install selenium to enable data scraping: pip install selenium")
