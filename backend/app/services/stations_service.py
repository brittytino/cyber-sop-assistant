"""
Police Stations Service
Maintains directory of police stations and cybercrime cells across India
"""
import math
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.core.logging import logger
from app.models.location import (
    PoliceStation, StationType, StationStatus, GeoCoordinates,
    NearbyStationResult, NearbyStationsResponse, StateWiseCyberCells, LocationRequest
)


# Sample data - in production, use database with regular updates
POLICE_STATIONS_DATA = [
    # Delhi
    {
        "station_id": "DEL-CC-001",
        "name": "Delhi Cyber Crime Cell",
        "name_local": "दिल्ली साइबर क्राइम सेल",
        "station_type": StationType.CYBER_CELL,
        "address": "Mandir Marg, Near Gole Market, New Delhi",
        "address_local": "मंदिर मार्ग, गोल मार्केट के पास, नई दिल्ली",
        "city": "New Delhi",
        "district": "Central Delhi",
        "state": "Delhi",
        "pincode": "110001",
        "coordinates": {"latitude": 28.6358, "longitude": 77.2090},
        "phone_numbers": ["011-23490000", "011-23490099"],
        "emergency_phone": "112",
        "email": "dcp-cybercrime-dl@nic.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=28.6358,77.2090"
    },
    {
        "station_id": "DEL-PS-001",
        "name": "Parliament Street Police Station",
        "station_type": StationType.POLICE_STATION,
        "address": "Parliament Street, New Delhi",
        "city": "New Delhi",
        "district": "Central Delhi",
        "state": "Delhi",
        "pincode": "110001",
        "coordinates": {"latitude": 28.6230, "longitude": 77.2140},
        "phone_numbers": ["011-23362121"],
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": True,
        "google_maps_url": "https://maps.google.com/?q=28.6230,77.2140"
    },
    # Mumbai
    {
        "station_id": "MH-CC-001",
        "name": "Maharashtra Cyber Cell",
        "name_local": "महाराष्ट्र सायबर सेल",
        "station_type": StationType.CYBER_CELL,
        "address": "BKC, Bandra East, Mumbai",
        "address_local": "बीकेसी, बांद्रा पूर्व, मुंबई",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "400051",
        "coordinates": {"latitude": 19.0596, "longitude": 72.8656},
        "phone_numbers": ["022-22026636", "022-22027270"],
        "email": "cybercell.mumbai@mahapolice.gov.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=19.0596,72.8656"
    },
    # Bangalore
    {
        "station_id": "KA-CC-001",
        "name": "Karnataka CID Cyber Crime Cell",
        "name_local": "ಕರ್ನಾಟಕ ಸಿಐಡಿ ಸೈಬರ್ ಕ್ರೈಮ್ ಸೆಲ್",
        "station_type": StationType.CYBER_CELL,
        "address": "CID Headquarters, 2nd Floor, Carlton House, Palace Road, Bangalore",
        "city": "Bangalore",
        "district": "Bangalore Urban",
        "state": "Karnataka",
        "pincode": "560001",
        "coordinates": {"latitude": 12.9789, "longitude": 77.5917},
        "phone_numbers": ["080-22942475", "080-22943050"],
        "email": "cybercrimeps@ksp.gov.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=12.9789,77.5917"
    },
    # Chennai
    {
        "station_id": "TN-CC-001",
        "name": "Tamil Nadu Cyber Crime Wing",
        "name_local": "தமிழ்நாடு சைபர் கிரைம் விங்",
        "station_type": StationType.CYBER_CELL,
        "address": "CBCID Office, 100 Feet Road, Guindy, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600032",
        "coordinates": {"latitude": 13.0067, "longitude": 80.2206},
        "phone_numbers": ["044-22501999", "044-28530500"],
        "email": "cybercrime@tnpolice.gov.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=13.0067,80.2206"
    },
    # Kolkata
    {
        "station_id": "WB-CC-001",
        "name": "West Bengal Cyber Crime Cell",
        "name_local": "পশ্চিমবঙ্গ সাইবার ক্রাইম সেল",
        "station_type": StationType.CYBER_CELL,
        "address": "Lalbazar, Kolkata",
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "pincode": "700001",
        "coordinates": {"latitude": 22.5726, "longitude": 88.3639},
        "phone_numbers": ["033-22143000", "033-22143024"],
        "email": "cybercrime.wb@gmail.com",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=22.5726,88.3639"
    },
    # Hyderabad
    {
        "station_id": "TS-CC-001",
        "name": "Telangana Cyber Crime Police Station",
        "name_local": "తెలంగాణ సైబర్ క్రైమ్ పోలీస్ స్టేషన్",
        "station_type": StationType.CYBER_CELL,
        "address": "D.S. Complex, 6th Floor, M.G Road, Secunderabad",
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "pincode": "500003",
        "coordinates": {"latitude": 17.4399, "longitude": 78.4983},
        "phone_numbers": ["040-27852274", "040-27852040"],
        "email": "cybercrime-hyd-ts@gov.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=17.4399,78.4983"
    },
    # Ahmedabad
    {
        "station_id": "GJ-CC-001",
        "name": "Gujarat Cyber Crime Cell",
        "name_local": "ગુજરાત સાઇબર ક્રાઇમ સેલ",
        "station_type": StationType.CYBER_CELL,
        "address": "CID Crime Branch, Shahibaug, Ahmedabad",
        "city": "Ahmedabad",
        "district": "Ahmedabad",
        "state": "Gujarat",
        "pincode": "380004",
        "coordinates": {"latitude": 23.0469, "longitude": 72.6030},
        "phone_numbers": ["079-25630045", "079-25630046"],
        "email": "cybercrime-ahd@gujarat.gov.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=23.0469,72.6030"
    },
    # Pune
    {
        "station_id": "MH-CC-002",
        "name": "Pune Cyber Crime Cell",
        "name_local": "पुणे सायबर क्राइम सेल",
        "station_type": StationType.CYBER_CELL,
        "address": "Commissioner Office, 2 Sadhu Vaswani Road, Pune",
        "city": "Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "pincode": "411001",
        "coordinates": {"latitude": 18.5204, "longitude": 73.8567},
        "phone_numbers": ["020-26123346", "020-26207400"],
        "email": "cybercell.pune@mahapolice.gov.in",
        "open_24x7": True,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=18.5204,73.8567"
    }
]

# Pincode to coordinates mapping (subset for common areas)
PINCODE_COORDINATES = {
    # Delhi
    "110001": {"latitude": 28.6358, "longitude": 77.2090, "city": "New Delhi", "state": "Delhi"},
    "110002": {"latitude": 28.6315, "longitude": 77.2167, "city": "New Delhi", "state": "Delhi"},
    "110003": {"latitude": 28.6474, "longitude": 77.2219, "city": "New Delhi", "state": "Delhi"},
    # Mumbai
    "400001": {"latitude": 18.9388, "longitude": 72.8354, "city": "Mumbai", "state": "Maharashtra"},
    "400051": {"latitude": 19.0596, "longitude": 72.8656, "city": "Mumbai", "state": "Maharashtra"},
    # Bangalore
    "560001": {"latitude": 12.9789, "longitude": 77.5917, "city": "Bangalore", "state": "Karnataka"},
    "560002": {"latitude": 12.9653, "longitude": 77.6084, "city": "Bangalore", "state": "Karnataka"},
    # Chennai
    "600001": {"latitude": 13.0878, "longitude": 80.2785, "city": "Chennai", "state": "Tamil Nadu"},
    "600032": {"latitude": 13.0067, "longitude": 80.2206, "city": "Chennai", "state": "Tamil Nadu"},
    # Kolkata
    "700001": {"latitude": 22.5726, "longitude": 88.3639, "city": "Kolkata", "state": "West Bengal"},
    # Hyderabad
    "500001": {"latitude": 17.3850, "longitude": 78.4867, "city": "Hyderabad", "state": "Telangana"},
    # Ahmedabad
    "380001": {"latitude": 23.0225, "longitude": 72.5714, "city": "Ahmedabad", "state": "Gujarat"},
    # Pune
    "411001": {"latitude": 18.5204, "longitude": 73.8567, "city": "Pune", "state": "Maharashtra"},
}


class StationsService:
    """Service for finding nearby police stations and cybercrime cells"""
    
    def __init__(self):
        self.stations = self._load_stations()
    
    def _load_stations(self) -> List[PoliceStation]:
        """Load stations from data"""
        stations = []
        for data in POLICE_STATIONS_DATA:
            coords = data.get("coordinates")
            stations.append(PoliceStation(
                station_id=data["station_id"],
                name=data["name"],
                name_local=data.get("name_local"),
                station_type=data["station_type"],
                address=data["address"],
                address_local=data.get("address_local"),
                city=data["city"],
                district=data["district"],
                state=data["state"],
                pincode=data["pincode"],
                coordinates=GeoCoordinates(**coords) if coords else None,
                phone_numbers=data.get("phone_numbers", []),
                emergency_phone=data.get("emergency_phone"),
                email=data.get("email"),
                open_24x7=data.get("open_24x7", True),
                status=data.get("status", StationStatus.ACTIVE),
                handles_cybercrime=data.get("handles_cybercrime", False),
                has_cyber_expert=data.get("has_cyber_expert", False),
                google_maps_url=data.get("google_maps_url")
            ))
        return stations
    
    def _calculate_distance(
        self,
        lat1: float, lon1: float,
        lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _create_directions_url(self, station: PoliceStation, user_coords: GeoCoordinates = None) -> str:
        """Create Google Maps directions URL"""
        if station.coordinates:
            dest = f"{station.coordinates.latitude},{station.coordinates.longitude}"
        else:
            dest = station.address.replace(" ", "+")
        
        if user_coords:
            return f"https://www.google.com/maps/dir/{user_coords.latitude},{user_coords.longitude}/{dest}"
        return f"https://www.google.com/maps/dir//{dest}"
    
    async def get_coordinates_from_pincode(self, pincode: str) -> Optional[Dict[str, Any]]:
        """Get coordinates from pincode"""
        return PINCODE_COORDINATES.get(pincode)
    
    async def find_nearby_stations(
        self,
        request: LocationRequest
    ) -> NearbyStationsResponse:
        """Find police stations near user location"""
        
        user_coords = None
        location_source = "unknown"
        
        # Determine user location
        if request.coordinates:
            user_coords = request.coordinates
            location_source = "gps"
        elif request.pincode:
            pincode_data = await self.get_coordinates_from_pincode(request.pincode)
            if pincode_data:
                user_coords = GeoCoordinates(
                    latitude=pincode_data["latitude"],
                    longitude=pincode_data["longitude"]
                )
                location_source = "pincode"
        elif request.city:
            # Search by city name
            location_source = "city"
        
        results: List[NearbyStationResult] = []
        cyber_cells: List[NearbyStationResult] = []
        
        for station in self.stations:
            # Filter by station type
            if station.station_type not in request.station_types and not station.handles_cybercrime:
                continue
            
            # Filter by status
            if not request.include_closed and station.status == StationStatus.TEMPORARILY_CLOSED:
                continue
            
            # Calculate distance if coordinates available
            distance_km = 999999
            if user_coords and station.coordinates:
                distance_km = self._calculate_distance(
                    user_coords.latitude, user_coords.longitude,
                    station.coordinates.latitude, station.coordinates.longitude
                )
                
                if distance_km > request.radius_km:
                    continue
            elif request.city and station.city.lower() != request.city.lower():
                continue
            
            # Estimate travel time (rough: 2 min per km in city)
            travel_time = int(distance_km * 2) if distance_km < 999999 else None
            
            result = NearbyStationResult(
                station=station,
                distance_km=round(distance_km, 2) if distance_km < 999999 else 0,
                estimated_travel_time_minutes=travel_time,
                directions_url=self._create_directions_url(station, user_coords)
            )
            
            if station.station_type == StationType.CYBER_CELL:
                cyber_cells.append(result)
            else:
                results.append(result)
        
        # Sort by distance
        results.sort(key=lambda x: x.distance_km)
        cyber_cells.sort(key=lambda x: x.distance_km)
        
        # Limit results
        results = results[:request.max_results]
        
        # Combine cyber cells and regular stations
        all_results = cyber_cells + results
        all_results.sort(key=lambda x: x.distance_km)
        
        return NearbyStationsResponse(
            user_location=user_coords,
            location_source=location_source,
            stations=all_results[:request.max_results],
            total_found=len(all_results),
            search_radius_km=request.radius_km,
            cyber_cells=cyber_cells,
            nearest_cyber_cell=cyber_cells[0] if cyber_cells else None,
            message=f"Found {len(all_results)} stations within {request.radius_km}km"
        )
    
    async def get_state_cyber_cells(self, state: str) -> Optional[StateWiseCyberCells]:
        """Get all cyber cells for a state"""
        state_cells = [s for s in self.stations 
                      if s.state.lower() == state.lower() 
                      and s.station_type == StationType.CYBER_CELL]
        
        if not state_cells:
            return None
        
        return StateWiseCyberCells(
            state=state,
            state_code=state[:2].upper(),
            cyber_cells=state_cells,
            total_count=len(state_cells)
        )
    
    async def get_all_states(self) -> List[str]:
        """Get list of all states with police station data"""
        return list(set(s.state for s in self.stations))
    
    async def get_station_by_id(self, station_id: str) -> Optional[PoliceStation]:
        """Get station by ID"""
        for station in self.stations:
            if station.station_id == station_id:
                return station
        return None


# Singleton instance
stations_service = StationsService()
