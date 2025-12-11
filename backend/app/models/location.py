"""
Location and Police Station Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class StationType(str, Enum):
    """Type of police station"""
    POLICE_STATION = "police_station"
    CYBER_CELL = "cyber_cell"
    CYBER_CRIME_UNIT = "cyber_crime_unit"
    WOMEN_POLICE_STATION = "women_police_station"
    DISTRICT_HQ = "district_hq"
    STATE_HQ = "state_hq"


class StationStatus(str, Enum):
    """Station operational status"""
    ACTIVE = "active"
    TEMPORARILY_CLOSED = "temporarily_closed"
    RELOCATED = "relocated"
    VERIFIED = "verified"
    UNVERIFIED = "unverified"


class GeoCoordinates(BaseModel):
    """Geographic coordinates"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy_meters: Optional[float] = None


class LocationRequest(BaseModel):
    """Location request from user"""
    # Either coordinates or address-based search
    coordinates: Optional[GeoCoordinates] = None
    pincode: Optional[str] = Field(None, pattern=r'^[1-9][0-9]{5}$')
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    
    # Search preferences
    radius_km: float = Field(default=10, ge=1, le=100)
    station_types: List[StationType] = Field(default=[StationType.CYBER_CELL, StationType.POLICE_STATION])
    max_results: int = Field(default=10, ge=1, le=50)
    include_closed: bool = Field(default=False)


class PoliceStation(BaseModel):
    """Police station information"""
    station_id: str
    name: str
    name_local: Optional[str] = None  # Name in local language
    station_type: StationType
    
    # Location
    address: str
    address_local: Optional[str] = None
    city: str
    district: str
    state: str
    pincode: str
    coordinates: Optional[GeoCoordinates] = None
    
    # Contact
    phone_numbers: List[str] = Field(default=[])
    emergency_phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Operating hours
    open_24x7: bool = Field(default=True)
    operating_hours: Optional[str] = None  # e.g., "9 AM - 6 PM"
    
    # Metadata
    status: StationStatus = StationStatus.ACTIVE
    last_verified: Optional[datetime] = None
    google_maps_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=1, le=5)
    
    # Cybercrime specific
    handles_cybercrime: bool = Field(default=False)
    has_cyber_expert: bool = Field(default=False)
    online_complaint_url: Optional[str] = None


class NearbyStationResult(BaseModel):
    """Station with distance information"""
    station: PoliceStation
    distance_km: float
    estimated_travel_time_minutes: Optional[int] = None
    directions_url: str


class NearbyStationsResponse(BaseModel):
    """Response with nearby stations"""
    user_location: Optional[GeoCoordinates] = None
    location_source: str  # "gps", "pincode", "city", "ip"
    stations: List[NearbyStationResult]
    total_found: int
    search_radius_km: float
    cyber_cells: List[NearbyStationResult] = Field(default=[])
    nearest_cyber_cell: Optional[NearbyStationResult] = None
    message: Optional[str] = None


class StateWiseCyberCells(BaseModel):
    """State-wise cybercrime cells directory"""
    state: str
    state_code: str
    nodal_officer: Optional[str] = None
    nodal_email: Optional[str] = None
    nodal_phone: Optional[str] = None
    cyber_cells: List[PoliceStation]
    total_count: int


class PoliceDirectoryUpdate(BaseModel):
    """Update request for police directory (admin)"""
    station_id: str
    updates: dict
    verified_by: Optional[str] = None
    source: str


class LocationPrivacyConsent(BaseModel):
    """User consent for location access"""
    consent_given: bool
    consent_type: str = Field(pattern=r'^(gps|manual|ip)$')
    timestamp: datetime
    session_id: str
    purpose: str = "Find nearby police stations and cybercrime cells"


# Emergency response models
class EmergencyAction(BaseModel):
    """Quick emergency action"""
    action_id: str
    title: str
    title_local: Optional[str] = None
    description: str
    description_local: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    action_type: str  # "call", "website", "app", "sms"
    priority: int = Field(ge=1, le=10)
    available_24x7: bool = True
    icon: Optional[str] = None
    category: str  # "emergency", "helpline", "portal", "support"


class EmergencyPanel(BaseModel):
    """Emergency actions panel"""
    actions: List[EmergencyAction]
    last_updated: datetime
    locale: str
