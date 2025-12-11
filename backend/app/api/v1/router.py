"""
API V1 Router - Aggregates all endpoints
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    chat, complaints, evidence, health, analytics, admin, location
)
from app.api.v1 import multilingual

# Import new endpoints
try:
    from app.api.v1.endpoints import auth, automation, progress, emergency, stations
    NEW_ENDPOINTS_AVAILABLE = True
except ImportError:
    NEW_ENDPOINTS_AVAILABLE = False

api_v1_router = APIRouter()

# Include all endpoint routers
api_v1_router.include_router(
    chat.router,
    tags=["Chat"]
)

# Authentication routes (new)
if NEW_ENDPOINTS_AVAILABLE:
    api_v1_router.include_router(
        auth.router,
        prefix="/auth",
        tags=["Authentication"]
    )

    # Automation routes (new)
    api_v1_router.include_router(
        automation.router,
        prefix="/automation",
        tags=["Automation"]
    )

    # Progress tracking routes (new)
    api_v1_router.include_router(
        progress.router,
        prefix="/progress",
        tags=["Progress"]
    )

    # Emergency actions routes (new)
    api_v1_router.include_router(
        emergency.router,
        prefix="/emergency",
        tags=["Emergency"]
    )

    # Police stations routes (new)
    api_v1_router.include_router(
        stations.router,
        prefix="/stations",
        tags=["Stations"]
)

api_v1_router.include_router(
    multilingual.router,
    tags=["Multilingual"]
)

api_v1_router.include_router(
    location.router,
    prefix="/location",
    tags=["Location"]
)

api_v1_router.include_router(
    complaints.router,
    prefix="/complaints",
    tags=["Complaints"]
)

api_v1_router.include_router(
    evidence.router,
    prefix="/evidence",
    tags=["Evidence"]
)

api_v1_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

api_v1_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

api_v1_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)
