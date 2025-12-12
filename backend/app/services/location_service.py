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
    
    async def get_stations_by_pincode(self, pincode: str) -> List[Dict[str, Any]]:
        """
        Get police stations by pincode using real data
        Includes both regular and cybercrime stations
        
        Args:
            pincode: 6-digit Indian pincode
            
        Returns:
            List of police stations in that pincode area
        """
        try:
            # First get location from pincode
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Use India Post API or nominatim
                response = await client.get(
                    f"{self.geocoding_api}/search",
                    params={
                        "postalcode": pincode,
                        "country": "India",
                        "format": "json",
                        "addressdetails": 1
                    },
                    headers={"User-Agent": settings.SCRAPER_USER_AGENT}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        location = data[0]
                        lat = float(location.get("lat"))
                        lon = float(location.get("lon"))
                        
                        # Get both regular police stations and cybercrime cells
                        regular_stations = await self.find_nearby_police_stations(
                            lat, lon, radius_km=15, max_results=10
                        )
                        
                        # Get cybercrime cells from database
                        address = location.get("address", {})
                        state = address.get("state", "")
                        city = address.get("city") or address.get("town") or address.get("village", "")
                        
                        cyber_cells = await self.find_cybercrime_cells(city, state)
                        
                        # Add distance to cyber cells based on coordinates
                        for cell in cyber_cells:
                            if "coordinates" in cell:
                                coords = cell["coordinates"]
                                distance = self._calculate_distance(
                                    lat, lon,
                                    coords["latitude"], coords["longitude"]
                                )
                                cell["distance_km"] = round(distance, 2)
                                cell["latitude"] = coords["latitude"]
                                cell["longitude"] = coords["longitude"]
                        
                        # Combine and sort by distance
                        all_stations = regular_stations + cyber_cells
                        all_stations.sort(key=lambda x: x.get("distance_km", 999))
                        
                        return all_stations
        
        except Exception as e:
            logger.error(f"Pincode search error: {e}")
        
        return []
    
    async def find_cybercrime_cells(
        self, 
        city: str, 
        state: str
    ) -> List[Dict[str, Any]]:
        """
        Find cybercrime police stations/cells in a city/state
        Uses comprehensive database of Indian cybercrime cells with focus on Tamil Nadu
        
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
                    "name": "Coimbatore City Cyber Crime Police Station",
                    "address": "Coimbatore City Police Office, Race Course Road, Coimbatore - 641018",
                    "phone": "0422-2303100, 0422-2303200",
                    "email": "ccpcbe.pol@tn.gov.in",
                    "helpline": "1930",
                    "district": "Coimbatore",
                    "jurisdiction": "Coimbatore City and surrounding areas",
                    "pincode": "641018",
                    "coordinates": {"latitude": 11.0168, "longitude": 76.9558},
                    "handles_cybercrime": True,
                    "open_24x7": False,
                    "working_hours": "Mon-Sat: 10:00 AM - 6:00 PM"
                },
                {
                    "name": "Coimbatore Rural Cyber Crime Wing",
                    "address": "SP Office, Coimbatore Rural, Mettupalayam Road, Coimbatore - 641043",
                    "phone": "0422-2226100",
                    "email": "sp.cbe.rural@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Coimbatore Rural",
                    "jurisdiction": "Rural areas of Coimbatore district",
                    "pincode": "641043",
                    "coordinates": {"latitude": 11.0510, "longitude": 76.9674},
                    "handles_cybercrime": True,
                    "open_24x7": False
                },
                {
                    "name": "Chennai Cyber Crime Cell (CB-CID)",
                    "address": "CB-CID, 5th Floor, Egmore, Chennai - 600008",
                    "phone": "044-23452348, 044-28447061",
                    "email": "cbcid.cybercrime@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Chennai",
                    "pincode": "600008",
                    "coordinates": {"latitude": 13.0732, "longitude": 80.2609},
                    "handles_cybercrime": True,
                    "open_24x7": True,
                    "website": "https://www.tnpolice.gov.in"
                },
                {
                    "name": "Madurai Cyber Crime Police Station",
                    "address": "City Police Office, Madurai - 625001",
                    "phone": "0452-2345100",
                    "email": "cybercrime.madurai@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Madurai",
                    "pincode": "625001",
                    "coordinates": {"latitude": 9.9252, "longitude": 78.1198},
                    "handles_cybercrime": True
                },
                {
                    "name": "Tiruchirappalli Cyber Crime Cell",
                    "address": "City Police Commissioner Office, Trichy - 620001",
                    "phone": "0431-2414141",
                    "email": "cybercrime.trichy@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Tiruchirappalli",
                    "pincode": "620001",
                    "coordinates": {"latitude": 10.7905, "longitude": 78.7047},
                    "handles_cybercrime": True
                },
                {
                    "name": "Salem Cyber Crime Police Station",
                    "address": "Salem City Police, Salem - 636001",
                    "phone": "0427-2414100",
                    "email": "cybercrime.salem@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Salem",
                    "pincode": "636001",
                    "coordinates": {"latitude": 11.6643, "longitude": 78.1460},
                    "handles_cybercrime": True
                },
                {
                    "name": "Tirunelveli Cyber Crime Cell",
                    "address": "SP Office, Tirunelveli - 627001",
                    "phone": "0462-2501100",
                    "email": "sp.tirunelveli@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Tirunelveli",
                    "pincode": "627001",
                    "coordinates": {"latitude": 8.7139, "longitude": 77.7567},
                    "handles_cybercrime": True
                },
                {
                    "name": "Erode Cyber Crime Wing",
                    "address": "SP Office, Erode - 638001",
                    "phone": "0424-2255100",
                    "email": "sp.erode@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Erode",
                    "pincode": "638001",
                    "coordinates": {"latitude": 11.3410, "longitude": 77.7172},
                    "handles_cybercrime": True
                },
                {
                    "name": "Vellore Cyber Crime Police Station",
                    "address": "SP Office, Vellore - 632001",
                    "phone": "0416-2226100",
                    "email": "sp.vellore@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Vellore",
                    "pincode": "632001",
                    "coordinates": {"latitude": 12.9165, "longitude": 79.1325},
                    "handles_cybercrime": True
                },
                {
                    "name": "Tiruppur Cyber Crime Cell",
                    "address": "SP Office, Tiruppur - 641601",
                    "phone": "0421-2212100",
                    "email": "sp.tiruppur@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Tiruppur",
                    "pincode": "641601",
                    "coordinates": {"latitude": 11.1075, "longitude": 77.3398},
                    "handles_cybercrime": True
                },
                {
                    "name": "Thanjavur Cyber Crime Wing",
                    "address": "SP Office, Thanjavur - 613001",
                    "phone": "04362-230100",
                    "email": "sp.thanjavur@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Thanjavur",
                    "pincode": "613001",
                    "coordinates": {"latitude": 10.7870, "longitude": 79.1378},
                    "handles_cybercrime": True
                },
                {
                    "name": "Kanyakumari Cyber Crime Cell",
                    "address": "SP Office, Nagercoil, Kanyakumari - 629001",
                    "phone": "04652-232100",
                    "email": "sp.kanyakumari@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Kanyakumari",
                    "pincode": "629001",
                    "coordinates": {"latitude": 8.1796, "longitude": 77.4060},
                    "handles_cybercrime": True
                },
                {
                    "name": "Dindigul Cyber Crime Police Station",
                    "address": "SP Office, Dindigul - 624001",
                    "phone": "0451-2414100",
                    "email": "sp.dindigul@tnpolice.gov.in",
                    "helpline": "1930",
                    "district": "Dindigul",
                    "pincode": "624001",
                    "coordinates": {"latitude": 10.3673, "longitude": 77.9803},
                    "handles_cybercrime": True
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
