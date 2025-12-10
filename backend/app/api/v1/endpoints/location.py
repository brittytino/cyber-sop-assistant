"""
Location Endpoint - Get user location and nearby police stations
"""
from fastapi import APIRouter, Request, Query
from typing import Optional
from app.services.location_service import location_service
from app.core.logging import logger
from pydantic import BaseModel, Field
from typing import List, Dict, Any


router = APIRouter()


class LocationResponse(BaseModel):
    """Location detection response"""
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class PoliceStationResponse(BaseModel):
    """Police station information"""
    name: str
    address: Optional[str]
    phone: Optional[str]
    distance_km: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]


class CybercrimeCellResponse(BaseModel):
    """Cybercrime cell information"""
    name: str
    address: str
    phone: str
    email: Optional[str]
    helpline: str
    website: Optional[str]
    description: Optional[str]


class NearbyStationsResponse(BaseModel):
    """Response with location and nearby stations"""
    location: LocationResponse
    police_stations: List[PoliceStationResponse]
    cybercrime_cells: List[CybercrimeCellResponse]


@router.get("/detect", response_model=LocationResponse)
async def detect_location(request: Request):
    """
    Auto-detect user location from IP address
    """
    try:
        # Get client IP
        client_ip = request.client.host
        
        # For development/localhost, use a fallback
        if client_ip in ["127.0.0.1", "localhost", "::1"]:
            client_ip = "8.8.8.8"  # Fallback for testing
            logger.info("Using fallback IP for localhost")
        
        location = await location_service.get_location_from_ip(client_ip)
        
        if location:
            return LocationResponse(**location)
        
        # Return empty response if detection fails
        return LocationResponse(
            city=None,
            state=None,
            country=None,
            latitude=None,
            longitude=None
        )
        
    except Exception as e:
        logger.error(f"Location detection error: {e}")
        return LocationResponse(
            city=None,
            state=None,
            country=None,
            latitude=None,
            longitude=None
        )


@router.get("/nearby-stations", response_model=NearbyStationsResponse)
async def get_nearby_stations(
    request: Request,
    latitude: Optional[float] = Query(None, description="User latitude"),
    longitude: Optional[float] = Query(None, description="User longitude"),
    radius_km: float = Query(10.0, ge=1.0, le=50.0, description="Search radius in km")
):
    """
    Get nearby police stations and cybercrime cells
    """
    try:
        # If coordinates not provided, detect from IP
        if latitude is None or longitude is None:
            client_ip = request.client.host
            if client_ip in ["127.0.0.1", "localhost", "::1"]:
                # Default to Delhi for localhost testing
                latitude = 28.6139
                longitude = 77.2090
                city = "New Delhi"
                state = "Delhi"
                country = "India"
            else:
                location = await location_service.get_location_from_ip(client_ip)
                if location:
                    latitude = location.get("latitude")
                    longitude = location.get("longitude")
                    city = location.get("city")
                    state = location.get("state")
                    country = location.get("country")
        else:
            # Reverse geocode provided coordinates
            location = await location_service.get_location_from_coordinates(latitude, longitude)
            city = location.get("city") if location else None
            state = location.get("state") if location else None
            country = location.get("country") if location else None
        
        # Find nearby police stations
        police_stations = []
        if latitude and longitude:
            stations = await location_service.find_nearby_police_stations(
                latitude, longitude, radius_km
            )
            police_stations = [PoliceStationResponse(**station) for station in stations]
        
        # Find cybercrime cells
        cybercrime_cells = []
        if state:
            cells = await location_service.find_cybercrime_cells(city or "", state)
            cybercrime_cells = [CybercrimeCellResponse(**cell) for cell in cells]
        
        return NearbyStationsResponse(
            location=LocationResponse(
                city=city,
                state=state,
                country=country,
                latitude=latitude,
                longitude=longitude
            ),
            police_stations=police_stations,
            cybercrime_cells=cybercrime_cells
        )
        
    except Exception as e:
        logger.error(f"Nearby stations error: {e}")
        return NearbyStationsResponse(
            location=LocationResponse(city=None, state=None, country=None, latitude=None, longitude=None),
            police_stations=[],
            cybercrime_cells=[]
        )
