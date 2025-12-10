"""
API V1 Router - Aggregates all endpoints
"""
from fastapi import APIRouter

from app.api.v1.endpoints import chat, complaints, evidence, health, analytics, admin, location
from app.api.v1 import multilingual

api_v1_router = APIRouter()

# Include all endpoint routers
api_v1_router.include_router(
    chat.router,
    tags=["Chat"]
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
