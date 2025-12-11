"""
Emergency Actions Endpoints
Quick access to emergency numbers and actions
"""
from fastapi import APIRouter, Query
from typing import List, Optional

from app.models.location import EmergencyAction, EmergencyPanel
from app.core.logging import logger
from datetime import datetime

router = APIRouter()


# Emergency actions data
EMERGENCY_ACTIONS = [
    {
        "action_id": "call_1930",
        "title": "Cyber Fraud Helpline",
        "title_hi": "साइबर धोखाधड़ी हेल्पलाइन",
        "title_ta": "சைபர் மோசடி உதவி எண்",
        "title_te": "సైబర్ మోసం హెల్ప్‌లైన్",
        "title_bn": "সাইবার জালিয়াতি হেল্পলাইন",
        "title_mr": "सायबर फसवणूक हेल्पलाइन",
        "title_gu": "સાયબર છેતરપિંડી હેલ્પલાઇન",
        "title_kn": "ಸೈಬರ್ ವಂಚನೆ ಸಹಾಯವಾಣಿ",
        "description": "Financial fraud, UPI scams, online banking fraud - Call immediately",
        "description_hi": "वित्तीय धोखाधड़ी, UPI घोटाले, ऑनलाइन बैंकिंग धोखाधड़ी - तुरंत कॉल करें",
        "phone": "1930",
        "action_type": "call",
        "priority": 10,
        "available_24x7": True,
        "category": "emergency"
    },
    {
        "action_id": "call_112",
        "title": "Emergency Police",
        "title_hi": "आपातकालीन पुलिस",
        "description": "Immediate danger, threats, blackmail, physical safety concerns",
        "description_hi": "तत्काल खतरा, धमकी, ब्लैकमेल, शारीरिक सुरक्षा चिंता",
        "phone": "112",
        "action_type": "call",
        "priority": 10,
        "available_24x7": True,
        "category": "emergency"
    },
    {
        "action_id": "call_181",
        "title": "Women's Helpline",
        "title_hi": "महिला हेल्पलाइन",
        "description": "Harassment, sextortion, cyberstalking, threats against women",
        "description_hi": "उत्पीड़न, यौन शोषण, साइबरस्टॉकिंग, महिलाओं के खिलाफ धमकी",
        "phone": "181",
        "action_type": "call",
        "priority": 9,
        "available_24x7": True,
        "category": "helpline"
    },
    {
        "action_id": "call_1098",
        "title": "Child Helpline (CHILDLINE)",
        "title_hi": "बाल हेल्पलाइन",
        "description": "Cyberbullying, child safety, online predators",
        "description_hi": "साइबरबुलिंग, बाल सुरक्षा, ऑनलाइन शिकारी",
        "phone": "1098",
        "action_type": "call",
        "priority": 9,
        "available_24x7": True,
        "category": "helpline"
    },
    {
        "action_id": "visit_cybercrime_portal",
        "title": "National Cybercrime Portal",
        "title_hi": "राष्ट्रीय साइबर अपराध पोर्टल",
        "description": "File online complaint for any cybercrime",
        "description_hi": "किसी भी साइबर अपराध के लिए ऑनलाइन शिकायत दर्ज करें",
        "url": "https://cybercrime.gov.in",
        "action_type": "website",
        "priority": 8,
        "available_24x7": True,
        "category": "portal"
    },
    {
        "action_id": "mental_health_support",
        "title": "Mental Health Support (Vandrevala Foundation)",
        "title_hi": "मानसिक स्वास्थ्य सहायता",
        "description": "Free counseling for distressed victims",
        "description_hi": "पीड़ितों के लिए मुफ्त परामर्श",
        "phone": "1860-2662-345",
        "action_type": "call",
        "priority": 7,
        "available_24x7": True,
        "category": "support"
    },
    {
        "action_id": "block_sim",
        "title": "Block Lost SIM (TAFCOP)",
        "title_hi": "खोए हुए सिम को ब्लॉक करें",
        "description": "Check and block unauthorized SIMs on your name",
        "description_hi": "अपने नाम पर अनधिकृत सिम की जांच करें और ब्लॉक करें",
        "url": "https://tafcop.dgt.gov.in",
        "action_type": "website",
        "priority": 8,
        "available_24x7": True,
        "category": "portal"
    },
    {
        "action_id": "lock_aadhaar",
        "title": "Lock Aadhaar Biometrics",
        "title_hi": "आधार बायोमेट्रिक्स लॉक करें",
        "description": "Prevent misuse of your Aadhaar for fraud",
        "description_hi": "धोखाधड़ी के लिए अपने आधार के दुरुपयोग को रोकें",
        "url": "https://resident.uidai.gov.in/lock-unlock",
        "action_type": "website",
        "priority": 7,
        "available_24x7": True,
        "category": "portal"
    }
]


@router.get("/actions", response_model=EmergencyPanel)
async def get_emergency_actions(
    category: Optional[str] = Query(None, description="Filter by category: emergency, helpline, portal, support"),
    language: str = Query("en", description="Language code for localized content")
):
    """
    Get emergency actions panel
    
    Returns quick-access emergency numbers and important links
    organized by priority and category
    """
    actions = []
    
    for data in EMERGENCY_ACTIONS:
        if category and data.get("category") != category:
            continue
        
        # Get localized title and description
        title = data.get(f"title_{language}", data["title"])
        description = data.get(f"description_{language}", data["description"])
        
        action = EmergencyAction(
            action_id=data["action_id"],
            title=title,
            title_local=data.get(f"title_{language}"),
            description=description,
            description_local=data.get(f"description_{language}"),
            phone=data.get("phone"),
            url=data.get("url"),
            action_type=data["action_type"],
            priority=data["priority"],
            available_24x7=data["available_24x7"],
            category=data["category"]
        )
        actions.append(action)
    
    # Sort by priority (higher first)
    actions.sort(key=lambda x: x.priority, reverse=True)
    
    return EmergencyPanel(
        actions=actions,
        last_updated=datetime.utcnow(),
        locale=language
    )


@router.get("/helplines")
async def get_helplines(language: str = Query("en")):
    """
    Get all emergency helpline numbers
    
    Quick reference for all important phone numbers
    """
    helplines = [
        {
            "name": "Cyber Fraud Helpline",
            "name_local": "साइबर धोखाधड़ी हेल्पलाइन" if language == "hi" else None,
            "number": "1930",
            "description": "Financial fraud, UPI scams, banking fraud",
            "available_24x7": True,
            "category": "cybercrime"
        },
        {
            "name": "Emergency Police",
            "name_local": "आपातकालीन पुलिस" if language == "hi" else None,
            "number": "112",
            "description": "All emergencies",
            "available_24x7": True,
            "category": "emergency"
        },
        {
            "name": "Women's Helpline",
            "name_local": "महिला हेल्पलाइन" if language == "hi" else None,
            "number": "181",
            "description": "Harassment, sextortion, stalking",
            "available_24x7": True,
            "category": "women"
        },
        {
            "name": "Child Helpline",
            "name_local": "बाल हेल्पलाइन" if language == "hi" else None,
            "number": "1098",
            "description": "Child safety, cyberbullying",
            "available_24x7": True,
            "category": "child"
        },
        {
            "name": "Senior Citizen Helpline",
            "number": "14567",
            "description": "For elderly victims",
            "available_24x7": True,
            "category": "senior"
        },
        {
            "name": "Mental Health Support",
            "number": "1860-2662-345",
            "description": "Counseling for distressed victims",
            "available_24x7": True,
            "category": "support"
        }
    ]
    
    return {"helplines": helplines}


@router.get("/portals")
async def get_important_portals():
    """
    Get important government portals and websites
    
    Official resources for filing complaints and getting help
    """
    portals = [
        {
            "name": "National Cybercrime Portal",
            "url": "https://cybercrime.gov.in",
            "description": "File complaints for any cybercrime",
            "official": True
        },
        {
            "name": "CERT-In",
            "url": "https://www.cert-in.org.in",
            "description": "Report cyber security incidents",
            "official": True
        },
        {
            "name": "TAFCOP (SIM Verification)",
            "url": "https://tafcop.dgt.gov.in",
            "description": "Check and block unauthorized SIMs",
            "official": True
        },
        {
            "name": "Aadhaar Lock/Unlock",
            "url": "https://resident.uidai.gov.in/lock-unlock",
            "description": "Lock your Aadhaar biometrics",
            "official": True
        },
        {
            "name": "RBI Ombudsman",
            "url": "https://cms.rbi.org.in",
            "description": "Banking complaints and grievances",
            "official": True
        },
        {
            "name": "Women & Child Portal",
            "url": "https://cybercrime.gov.in/Webform/Womenchild.aspx",
            "description": "Specialized portal for women and children",
            "official": True
        }
    ]
    
    return {"portals": portals}
