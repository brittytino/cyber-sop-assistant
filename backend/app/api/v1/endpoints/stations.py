"""
Police Stations Endpoints
Find nearby police stations and cybercrime cells
"""
from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional, List

from app.services.stations_service import stations_service
from app.models.location import (
    LocationRequest, NearbyStationsResponse, PoliceStation,
    StateWiseCyberCells, StationType, GeoCoordinates
)
from app.core.logging import logger

router = APIRouter()


@router.get("/nearby", response_model=NearbyStationsResponse)
async def find_nearby_stations(
    latitude: Optional[float] = Query(None, ge=-90, le=90, description="User latitude"),
    longitude: Optional[float] = Query(None, ge=-180, le=180, description="User longitude"),
    pincode: Optional[str] = Query(None, min_length=6, max_length=6, description="Indian pincode"),
    city: Optional[str] = Query(None, max_length=100, description="City name"),
    state: Optional[str] = Query(None, max_length=100, description="State name"),
    radius_km: float = Query(10, ge=1, le=100, description="Search radius in km"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum results to return"),
    include_cyber_cells: bool = Query(True, description="Include cybercrime cells"),
    include_police_stations: bool = Query(True, description="Include regular police stations")
):
    """
    Find nearby police stations and cybercrime cells
    
    Provide either:
    - GPS coordinates (latitude + longitude) - most accurate
    - Pincode - good accuracy
    - City name - shows all stations in city
    
    Returns sorted list with distance, contact info, and directions
    """
    # Build location request
    coordinates = None
    if latitude is not None and longitude is not None:
        coordinates = GeoCoordinates(latitude=latitude, longitude=longitude)
    
    station_types = []
    if include_cyber_cells:
        station_types.append(StationType.CYBER_CELL)
        station_types.append(StationType.CYBER_CRIME_UNIT)
    if include_police_stations:
        station_types.append(StationType.POLICE_STATION)
        station_types.append(StationType.WOMEN_POLICE_STATION)
    
    if not station_types:
        station_types = [StationType.CYBER_CELL, StationType.POLICE_STATION]
    
    request = LocationRequest(
        coordinates=coordinates,
        pincode=pincode,
        city=city,
        state=state,
        radius_km=radius_km,
        max_results=max_results,
        station_types=station_types
    )
    
    logger.info(f"Finding nearby stations: pincode={pincode}, city={city}, coords={coordinates}")
    
    result = await stations_service.find_nearby_stations(request)
    
    if not result.stations:
        logger.warning(f"No stations found for request: {request}")
    
    return result


@router.get("/cyber-cells", response_model=List[PoliceStation])
async def get_cyber_cells(
    state: Optional[str] = Query(None, description="Filter by state")
):
    """
    Get list of all cybercrime cells
    
    Optionally filter by state
    """
    if state:
        state_data = await stations_service.get_state_cyber_cells(state)
        if state_data:
            return state_data.cyber_cells
        return []
    
    # Return all cyber cells
    all_cells = [s for s in stations_service.stations 
                 if s.station_type == StationType.CYBER_CELL]
    return all_cells


@router.get("/states")
async def get_states_list():
    """
    Get list of states with police station data
    """
    states = await stations_service.get_all_states()
    return {"states": sorted(states)}


@router.get("/state/{state_name}", response_model=StateWiseCyberCells)
async def get_state_cyber_cells(state_name: str):
    """
    Get all cybercrime cells for a specific state
    """
    result = await stations_service.get_state_cyber_cells(state_name)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No cybercrime cells found for state: {state_name}"
        )
    
    return result


@router.get("/{station_id}", response_model=PoliceStation)
async def get_station_details(station_id: str):
    """
    Get detailed information about a specific station
    """
    station = await stations_service.get_station_by_id(station_id)
    
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station not found: {station_id}"
        )
    
    return station


@router.get("/pincode/{pincode}")
async def get_stations_by_pincode(pincode: str):
    """
    Get stations near a specific pincode
    
    Convenient endpoint for pincode-based search
    """
    if not pincode or len(pincode) != 6 or not pincode.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pincode format. Must be 6 digits."
        )
    
    request = LocationRequest(
        pincode=pincode,
        radius_km=15,
        max_results=10
    )
    
    return await stations_service.find_nearby_stations(request)


@router.get("/city/{city_name}")
async def get_stations_by_city(city_name: str):
    """
    Get all stations in a specific city
    """
    request = LocationRequest(
        city=city_name,
        radius_km=50,
        max_results=20
    )
    
    return await stations_service.find_nearby_stations(request)
