"""
Location Service - Automatic Location Detection and Nearby Police Station Finder
"""
import httpx
from typing import Dict, List, Optional, Any
from app.core.logging import logger
from app.core.config import settings


class LocationService:
    """Service for location detection and finding nearby police stations"""
    
    def __init__(self):
        self.geocoding_api = "https://nominatim.openstreetmap.org"
        self.overpass_api = "https://overpass-api.de/api/interpreter"
        
    async def get_location_from_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """
        Get location details from IP address
        
        Args:
            ip_address: Client IP address
            
        Returns:
            Location details including city, state, country, coordinates
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Use ip-api.com (free, no key required)
                response = await client.get(
                    f"http://ip-api.com/json/{ip_address}",
                    params={"fields": "status,country,countryCode,region,regionName,city,lat,lon,timezone"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        return {
                            "city": data.get("city"),
                            "state": data.get("regionName"),
                            "country": data.get("country"),
                            "country_code": data.get("countryCode"),
                            "latitude": data.get("lat"),
                            "longitude": data.get("lon"),
                            "timezone": data.get("timezone")
                        }
                        
        except Exception as e:
            logger.error(f"IP geolocation error: {e}")
            
        return None
    
    async def get_location_from_coordinates(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        Reverse geocode coordinates to location details
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Location details
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.geocoding_api}/reverse",
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json",
                        "addressdetails": 1
                    },
                    headers={"User-Agent": settings.SCRAPER_USER_AGENT}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    address = data.get("address", {})
                    
                    return {
                        "city": address.get("city") or address.get("town") or address.get("village"),
                        "state": address.get("state"),
                        "country": address.get("country"),
                        "country_code": address.get("country_code", "").upper(),
                        "postcode": address.get("postcode"),
                        "latitude": latitude,
                        "longitude": longitude,
                        "display_name": data.get("display_name")
                    }
                    
        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")
            
        return None
    
    async def find_nearby_police_stations(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10.0,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find nearby police stations using Overpass API (OpenStreetMap)
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_km: Search radius in kilometers
            max_results: Maximum number of results
            
        Returns:
            List of police stations with details
        """
        try:
            # Overpass QL query for police stations
            radius_m = radius_km * 1000  # Convert to meters
            
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="police"](around:{radius_m},{latitude},{longitude});
              way["amenity"="police"](around:{radius_m},{latitude},{longitude});
              relation["amenity"="police"](around:{radius_m},{latitude},{longitude});
            );
            out center {max_results};
            """
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.overpass_api,
                    data={"data": overpass_query},
                    headers={"User-Agent": settings.SCRAPER_USER_AGENT}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    stations = []
                    
                    for element in data.get("elements", []):
                        tags = element.get("tags", {})
                        
                        # Get coordinates
                        if element.get("type") == "node":
                            lat = element.get("lat")
                            lon = element.get("lon")
                        elif "center" in element:
                            lat = element["center"].get("lat")
                            lon = element["center"].get("lon")
                        else:
                            continue
                        
                        # Calculate distance
                        distance = self._calculate_distance(
                            latitude, longitude, lat, lon
                        )
                        
                        station = {
                            "name": tags.get("name", "Police Station"),
                            "type": tags.get("police:type", "police_station"),
                            "address": tags.get("addr:full") or self._build_address(tags),
                            "phone": tags.get("phone") or tags.get("contact:phone"),
                            "latitude": lat,
                            "longitude": lon,
                            "distance_km": round(distance, 2),
                            "opening_hours": tags.get("opening_hours"),
                            "operator": tags.get("operator"),
                            "website": tags.get("website") or tags.get("contact:website")
                        }
                        
                        stations.append(station)
                    
                    # Sort by distance
                    stations.sort(key=lambda x: x["distance_km"])
                    return stations[:max_results]
                    
        except Exception as e:
            logger.error(f"Police station search error: {e}")
            
        return []
    
    async def find_cybercrime_cells(
        self, 
        city: str, 
        state: str
    ) -> List[Dict[str, Any]]:
        """
        Find cybercrime police stations/cells in a city/state
        Uses predefined database of Indian cybercrime cells
        
        Args:
            city: City name
            state: State name
            
        Returns:
            List of cybercrime cells
        """
        # Comprehensive database of Indian Cybercrime Cells
        cybercrime_db = {
            "Delhi": [
                {
                    "name": "Delhi Police Cyber Crime Cell",
                    "address": "IFSO, 3rd Floor, Chanakyapuri Police Station, New Delhi - 110021",
                    "phone": "011-26107346, 011-26107730",
                    "email": "cybercrimedelhi@gmail.com",
                    "helpline": "1930",
                    "website": "https://cybercrime.gov.in"
                }
            ],
            "Maharashtra": [
                {
                    "name": "Mumbai Cyber Crime Cell",
                    "address": "CID Cyber, 4th Floor, Office of DCP (Cyber), BKC, Mumbai - 400051",
                    "phone": "022-26592333",
                    "email": "dcpcybercrime-mum@mahapolice.gov.in",
                    "helpline": "1930"
                },
                {
                    "name": "Pune Cyber Crime Cell",
                    "address": "Shivaji Nagar Police Station, Pune - 411005",
                    "phone": "020-26053026",
                    "email": "cybercrimepune@mahapolice.gov.in",
                    "helpline": "1930"
                }
            ],
            "Karnataka": [
                {
                    "name": "Bengaluru Cyber Crime Police Station",
                    "address": "CID Office, Carlton House, Palace Road, Bengaluru - 560001",
                    "phone": "080-22942555",
                    "email": "cybercrimebangalore@ksp.gov.in",
                    "helpline": "1930",
                    "website": "https://ksp.karnataka.gov.in"
                }
            ],
            "Tamil Nadu": [
                {
                    "name": "Chennai Cyber Crime Cell",
                    "address": "CB-CID, 5th Floor, Egmore, Chennai - 600008",
                    "phone": "044-23452348",
                    "email": "cybercrimechennai@tn.gov.in",
                    "helpline": "1930"
                }
            ],
            "Telangana": [
                {
                    "name": "Hyderabad Cyber Crime Police Station",
                    "address": "Banjara Hills, Hyderabad - 500034",
                    "phone": "040-27853508",
                    "email": "cyberabad.police@gov.in",
                    "helpline": "1930"
                }
            ],
            "West Bengal": [
                {
                    "name": "Kolkata Cyber Crime Cell",
                    "address": "Lalbazar, Kolkata - 700001",
                    "phone": "033-22143020",
                    "email": "cybercrimekolkata@wb.gov.in",
                    "helpline": "1930"
                }
            ],
            "Gujarat": [
                {
                    "name": "Ahmedabad Cyber Crime Cell",
                    "address": "Crime Branch, Shahibaug, Ahmedabad - 380004",
                    "phone": "079-27403322",
                    "email": "cybercrimeahmedabad@gujarat.gov.in",
                    "helpline": "1930"
                }
            ],
            "Rajasthan": [
                {
                    "name": "Jaipur Cyber Crime Cell",
                    "address": "Police Commissionerate, Jaipur - 302001",
                    "phone": "0141-2228888",
                    "email": "cybercrimejaipur@rajasthan.gov.in",
                    "helpline": "1930"
                }
            ],
            "Uttar Pradesh": [
                {
                    "name": "Lucknow Cyber Crime Cell",
                    "address": "UP Police Headquarters, Lucknow - 226001",
                    "phone": "0522-2238345",
                    "email": "cybercrimelucknow@up.gov.in",
                    "helpline": "1930"
                },
                {
                    "name": "Noida Cyber Crime Cell",
                    "address": "Sector 18, Noida - 201301",
                    "phone": "0120-2412222",
                    "email": "cybercr​imenoida@up.gov.in",
                    "helpline": "1930"
                }
            ],
            "Punjab": [
                {
                    "name": "Chandigarh Cyber Crime Cell",
                    "address": "Sector 9, Chandigarh - 160009",
                    "phone": "0172-2741031",
                    "email": "cybercrimechandigarh@punjabpolice.gov.in",
                    "helpline": "1930"
                }
            ]
        }
        
        # Search for state match
        cells = []
        for state_key, state_cells in cybercrime_db.items():
            if state and state_key.lower() in state.lower():
                cells.extend(state_cells)
        
        # If no state match, return all for India
        if not cells:
            # Return national helpline info
            cells = [{
                "name": "National Cyber Crime Helpline",
                "address": "Available across all states",
                "phone": "1930",
                "email": "report@cybercrime.gov.in",
                "helpline": "1930",
                "website": "https://cybercrime.gov.in",
                "description": "24x7 National helpline for reporting cybercrimes"
            }]
        
        return cells
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        
        Returns:
            Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c
    
    def _build_address(self, tags: Dict[str, str]) -> str:
        """Build address from OSM tags"""
        parts = []
        
        for key in ["addr:housenumber", "addr:street", "addr:city", "addr:state", "addr:postcode"]:
            if key in tags:
                parts.append(tags[key])
        
        return ", ".join(parts) if parts else "Address not available"


# Global instance
location_service = LocationService()
