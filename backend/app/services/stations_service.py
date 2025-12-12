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
    # Coimbatore - Primary Cyber Crime Cell
    {
        "station_id": "TN-CC-002",
        "name": "Coimbatore City Cyber Crime Police Station",
        "name_local": "கோயம்புத்தூர் நகர் சைபர் கிரைம் போலீஸ் ஸ்டேஷன்",
        "station_type": StationType.CYBER_CELL,
        "address": "Coimbatore City Police Office, Race Course Road, Coimbatore",
        "address_local": "கோயம்புத்தூர் நகர் காவல்துறை அலுவலகம், ரேஸ் கோர்ஸ் ரோடு",
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "641018",
        "coordinates": {"latitude": 11.0168, "longitude": 76.9558},
        "phone_numbers": ["0422-2303100", "0422-2303200", "0422-2303300"],
        "emergency_phone": "100",
        "email": "ccpcbe.pol@tn.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=11.0168,76.9558"
    },
    {
        "station_id": "TN-CC-003",
        "name": "Coimbatore Rural Cyber Crime Wing",
        "name_local": "கோயம்புத்தூர் கிராமப்புற சைபர் கிரைம் பிரிவு",
        "station_type": StationType.CYBER_CRIME_UNIT,
        "address": "SP Office, Coimbatore Rural, Mettupalayam Road, Coimbatore",
        "address_local": "எஸ்பி அலுவலகம், கோயம்புத்தூர் கிராமப்புறம், மேட்டுப்பாளையம் சாலை",
        "city": "Coimbatore",
        "district": "Coimbatore Rural",
        "state": "Tamil Nadu",
        "pincode": "641043",
        "coordinates": {"latitude": 11.0510, "longitude": 76.9674},
        "phone_numbers": ["0422-2226100", "0422-2420100"],
        "email": "sp.cbe.rural@tnpolice.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=11.0510,76.9674"
    },
    {
        "station_id": "TN-PS-001",
        "name": "RS Puram Police Station",
        "name_local": "ஆர்எஸ் புரம் காவல் நிலையம்",
        "station_type": StationType.POLICE_STATION,
        "address": "Trichy Road, RS Puram, Coimbatore",
        "address_local": "திருச்சி சாலை, ஆர்எஸ் புரம், கோயம்புத்தூர்",
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "641002",
        "coordinates": {"latitude": 11.0024, "longitude": 76.9528},
        "phone_numbers": ["0422-2471468", "0422-2471100"],
        "emergency_phone": "100",
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": True,
        "google_maps_url": "https://maps.google.com/?q=11.0024,76.9528"
    },
    {
        "station_id": "TN-PS-002",
        "name": "Gandhipuram Police Station",
        "name_local": "காந்திபுரம் காவல் நிலையம்",
        "station_type": StationType.POLICE_STATION,
        "address": "Gandhipuram, Coimbatore",
        "address_local": "காந்திபுரம், கோயம்புத்தூர்",
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "641012",
        "coordinates": {"latitude": 11.0184, "longitude": 76.9674},
        "phone_numbers": ["0422-2214100", "0422-2214234"],
        "emergency_phone": "100",
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": True,
        "google_maps_url": "https://maps.google.com/?q=11.0184,76.9674"
    },
    {
        "station_id": "TN-PS-003",
        "name": "Peelamedu Police Station",
        "name_local": "பீளமேடு காவல் நிலையம்",
        "station_type": StationType.POLICE_STATION,
        "address": "Avinashi Road, Peelamedu, Coimbatore",
        "address_local": "அவிநாசி சாலை, பீளமேடு, கோயம்புத்தூர்",
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "641004",
        "coordinates": {"latitude": 11.0289, "longitude": 77.0069},
        "phone_numbers": ["0422-2573100", "0422-2573255"],
        "emergency_phone": "100",
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": True,
        "google_maps_url": "https://maps.google.com/?q=11.0289,77.0069"
    },
    {
        "station_id": "TN-PS-004",
        "name": "Saibaba Colony Police Station",
        "name_local": "சாய்பாபா காலனி காவல் நிலையம்",
        "station_type": StationType.POLICE_STATION,
        "address": "Saibaba Colony, Coimbatore",
        "address_local": "சாய்பாபா காலனி, கோயம்புத்தூர்",
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "641011",
        "coordinates": {"latitude": 11.0176, "longitude": 76.9376},
        "phone_numbers": ["0422-2446100", "0422-2446400"],
        "emergency_phone": "100",
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": True,
        "google_maps_url": "https://maps.google.com/?q=11.0176,76.9376"
    },
    {
        "station_id": "TN-PS-005",
        "name": "Singanallur Police Station",
        "name_local": "சிங்கநல்லூர் காவல் நிலையம்",
        "station_type": StationType.POLICE_STATION,
        "address": "Singanallur, Coimbatore",
        "address_local": "சிங்கநல்லூர், கோயம்புத்தூர்",
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "pincode": "641005",
        "coordinates": {"latitude": 11.0033, "longitude": 77.0214},
        "phone_numbers": ["0422-2686100", "0422-2686200"],
        "emergency_phone": "100",
        "open_24x7": True,
        "status": StationStatus.ACTIVE,
        "handles_cybercrime": False,
        "google_maps_url": "https://maps.google.com/?q=11.0033,77.0214"
    },
    # Other Tamil Nadu Cities
    {
        "station_id": "TN-CC-004",
        "name": "Madurai Cyber Crime Police Station",
        "name_local": "மதுரை சைபர் கிரைம் போலீஸ் ஸ்டேஷன்",
        "station_type": StationType.CYBER_CELL,
        "address": "City Police Office, Madurai",
        "city": "Madurai",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "pincode": "625001",
        "coordinates": {"latitude": 9.9252, "longitude": 78.1198},
        "phone_numbers": ["0452-2345100", "0452-2534500"],
        "email": "cybercrime.madurai@tnpolice.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=9.9252,78.1198"
    },
    {
        "station_id": "TN-CC-005",
        "name": "Salem Cyber Crime Police Station",
        "name_local": "சேலம் சைபர் கிரைம் போலீஸ் ஸ்டேஷன்",
        "station_type": StationType.CYBER_CELL,
        "address": "Salem City Police, Salem",
        "city": "Salem",
        "district": "Salem",
        "state": "Tamil Nadu",
        "pincode": "636001",
        "coordinates": {"latitude": 11.6643, "longitude": 78.1460},
        "phone_numbers": ["0427-2414100", "0427-2315100"],
        "email": "cybercrime.salem@tnpolice.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=11.6643,78.1460"
    },
    {
        "station_id": "TN-CC-006",
        "name": "Tiruchirappalli Cyber Crime Cell",
        "name_local": "திருச்சிராப்பள்ளி சைபர் கிரைம் செல்",
        "station_type": StationType.CYBER_CELL,
        "address": "City Police Commissioner Office, Trichy",
        "city": "Tiruchirappalli",
        "district": "Tiruchirappalli",
        "state": "Tamil Nadu",
        "pincode": "620001",
        "coordinates": {"latitude": 10.7905, "longitude": 78.7047},
        "phone_numbers": ["0431-2414141", "0431-2461222"],
        "email": "cybercrime.trichy@tnpolice.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=10.7905,78.7047"
    },
    {
        "station_id": "TN-CC-007",
        "name": "Tiruppur Cyber Crime Cell",
        "name_local": "திருப்பூர் சைபர் கிரைம் செல்",
        "station_type": StationType.CYBER_CELL,
        "address": "SP Office, Tiruppur",
        "city": "Tiruppur",
        "district": "Tiruppur",
        "state": "Tamil Nadu",
        "pincode": "641601",
        "coordinates": {"latitude": 11.1075, "longitude": 77.3398},
        "phone_numbers": ["0421-2212100", "0421-2441044"],
        "email": "sp.tiruppur@tnpolice.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=11.1075,77.3398"
    },
    {
        "station_id": "TN-CC-008",
        "name": "Erode Cyber Crime Wing",
        "name_local": "ஈரோடு சைபர் கிரைம் விங்",
        "station_type": StationType.CYBER_CELL,
        "address": "SP Office, Erode",
        "city": "Erode",
        "district": "Erode",
        "state": "Tamil Nadu",
        "pincode": "638001",
        "coordinates": {"latitude": 11.3410, "longitude": 77.7172},
        "phone_numbers": ["0424-2255100", "0424-2256100"],
        "email": "sp.erode@tnpolice.gov.in",
        "open_24x7": False,
        "status": StationStatus.VERIFIED,
        "handles_cybercrime": True,
        "has_cyber_expert": True,
        "google_maps_url": "https://maps.google.com/?q=11.3410,77.7172"
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
    # Coimbatore - Comprehensive mapping
    "641001": {"latitude": 11.0168, "longitude": 76.9558, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641002": {"latitude": 11.0024, "longitude": 76.9528, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641003": {"latitude": 11.0208, "longitude": 76.9528, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641004": {"latitude": 11.0289, "longitude": 77.0069, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641005": {"latitude": 11.0033, "longitude": 77.0214, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641006": {"latitude": 11.0096, "longitude": 76.9676, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641007": {"latitude": 10.9891, "longitude": 76.9611, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641008": {"latitude": 10.9964, "longitude": 76.9612, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641009": {"latitude": 11.0079, "longitude": 76.9742, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641010": {"latitude": 11.0186, "longitude": 76.9674, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641011": {"latitude": 11.0176, "longitude": 76.9376, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641012": {"latitude": 11.0184, "longitude": 76.9674, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641013": {"latitude": 11.0239, "longitude": 76.9629, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641014": {"latitude": 11.0399, "longitude": 76.9746, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641015": {"latitude": 11.0439, "longitude": 76.9876, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641016": {"latitude": 10.9789, "longitude": 76.9631, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641017": {"latitude": 10.9834, "longitude": 76.9772, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641018": {"latitude": 11.0168, "longitude": 76.9558, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641019": {"latitude": 11.0256, "longitude": 76.9877, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641020": {"latitude": 11.0321, "longitude": 76.9816, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641021": {"latitude": 11.0265, "longitude": 77.0042, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641022": {"latitude": 11.0429, "longitude": 77.0252, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641023": {"latitude": 11.0547, "longitude": 77.0145, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641024": {"latitude": 11.0324, "longitude": 76.9526, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641025": {"latitude": 11.0463, "longitude": 76.9482, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641026": {"latitude": 11.0584, "longitude": 76.9724, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641027": {"latitude": 11.0687, "longitude": 76.9926, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641028": {"latitude": 11.0712, "longitude": 77.0147, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641029": {"latitude": 11.0542, "longitude": 77.0374, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641030": {"latitude": 11.0147, "longitude": 77.0432, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641031": {"latitude": 10.9876, "longitude": 77.0123, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641032": {"latitude": 10.9634, "longitude": 76.9876, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641033": {"latitude": 10.9542, "longitude": 77.0234, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641034": {"latitude": 10.9889, "longitude": 77.0542, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641035": {"latitude": 11.0176, "longitude": 77.0654, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641036": {"latitude": 11.0387, "longitude": 77.0876, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641037": {"latitude": 10.9764, "longitude": 77.0743, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641038": {"latitude": 10.9542, "longitude": 77.0876, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641039": {"latitude": 10.9234, "longitude": 77.0432, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641040": {"latitude": 10.9012, "longitude": 77.0234, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641041": {"latitude": 10.8876, "longitude": 76.9987, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641042": {"latitude": 10.9123, "longitude": 76.9654, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641043": {"latitude": 11.0510, "longitude": 76.9674, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641045": {"latitude": 11.0732, "longitude": 76.9432, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641046": {"latitude": 11.0876, "longitude": 76.9876, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641047": {"latitude": 11.0987, "longitude": 77.0123, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641048": {"latitude": 11.1123, "longitude": 77.0387, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641049": {"latitude": 11.0932, "longitude": 77.0654, "city": "Coimbatore", "state": "Tamil Nadu"},
    "641050": {"latitude": 11.0654, "longitude": 77.0987, "city": "Coimbatore", "state": "Tamil Nadu"},
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
