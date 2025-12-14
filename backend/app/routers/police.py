"""
Police Router - Handles police station queries
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
import logging

from ..dependencies import get_db
from ..schemas import PoliceStationOut, PoliceSearchRequest, PoliceStationCreate
from ..models import PoliceStation

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search", response_model=List[PoliceStationOut])
async def search_police_stations(
    state: Optional[str] = Query(None, description="State name"),
    district: Optional[str] = Query(None, description="District name"),
    city: Optional[str] = Query(None, description="City name"),
    cyber_only: bool = Query(False, description="Show only cyber cells"),
    db: Session = Depends(get_db)
):
    """
    Search for nearby police stations
    """
    query = db.query(PoliceStation)
    
    # Apply filters
    filters = []
    if state:
        filters.append(PoliceStation.state.ilike(f"%{state}%"))
    if district:
        filters.append(PoliceStation.district.ilike(f"%{district}%"))
    if city:
        filters.append(PoliceStation.city.ilike(f"%{city}%"))
    if cyber_only:
        filters.append(PoliceStation.is_cyber_cell == True)
    
    if filters:
        query = query.filter(and_(*filters))
    
    stations = query.limit(50).all()
    # No fallback - data must come from DB
    return stations

@router.get("/states")
async def get_states(db: Session = Depends(get_db)):
    """
    Get list of all states with police stations
    """
    states = db.query(PoliceStation.state).distinct().all()
    return [s[0] for s in states]

@router.post("/", response_model=PoliceStationOut)
async def create_police_station(station: PoliceStationCreate, db: Session = Depends(get_db)):
    """
    Add a new police station (admin only)
    """
    db_station = PoliceStation(**station.dict())
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station

@router.post("/initialize")
async def initialize_police_data(db: Session = Depends(get_db)):
    """
    Initialize sample police station data
    """
    count = db.query(PoliceStation).count()
    if count > 0:
        return {"message": f"Police stations already exist ({count} stations)", "initialized": False}
    
    # Add sample data
    from ..seed_data import POLICE_STATIONS
    for station_data in POLICE_STATIONS:
        station = PoliceStation(**station_data)
        db.add(station)
    
    db.commit()
    return {"message": f"Initialized {len(POLICE_STATIONS)} police stations", "initialized": True}
