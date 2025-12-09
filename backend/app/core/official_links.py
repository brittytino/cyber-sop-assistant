"""
Official Links Database
All verified .gov.in and official portal links
Last Updated: 2025-12-09
"""
from typing import Dict, List
from pydantic import BaseModel, HttpUrl


class OfficialLink(BaseModel):
    """Official link with metadata"""
    url: str
    title: str
    title_hi: str
    description: str
    description_hi: str
    last_verified: str  # Date in YYYY-MM-DD format


class OfficialContactDatabase:
    """Database of all official contacts and links"""
    
    # National Helplines
    HELPLINES = {
        "cybercrime": OfficialLink(
            url="tel:1930",
            title="National Cybercrime Helpline",
            title_hi="राष्ट्रीय साइबर अपराध हेल्पलाइन",
            description="24x7 helpline for immediate cyber crime assistance",
            description_hi="साइबर अपराध के लिए 24x7 हेल्पलाइन",
            last_verified="2025-12-09"
        ),
        "women": OfficialLink(
            url="tel:1091",
            title="Women Helpline",
            title_hi="महिला हेल्पलाइन",
            description="Women in distress helpline",
            description_hi="महिला संकट हेल्पलाइन",
            last_verified="2025-12-09"
        ),
        "child": OfficialLink(
            url="tel:1098",
            title="Child Helpline",
            title_hi="बाल हेल्पलाइन",
            description="Child abuse and protection helpline",
            description_hi="बाल शोषण हेल्पलाइन",
            last_verified="2025-12-09"
        ),
        "senior_citizen": OfficialLink(
            url="tel:14567",
            title="Senior Citizen Helpline",
            title_hi="वरिष्ठ नागरिक हेल्पलाइन",
            description="Senior citizen assistance",
            description_hi="वरिष्ठ नागरिक सहायता",
            last_verified="2025-12-09"
        ),
    }
    
    # Main Reporting Portals
    REPORTING_PORTALS = {
        "cybercrime_portal": OfficialLink(
            url="https://cybercrime.gov.in",
            title="National Cybercrime Reporting Portal",
            title_hi="राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल",
            description="File online complaint for any cybercrime",
            description_hi="किसी भी साइबर अपराध की ऑनलाइन शिकायत दर्ज करें",
            last_verified="2025-12-09"
        ),
        "cert_in": OfficialLink(
            url="https://www.cert-in.org.in",
            title="CERT-In (Indian Computer Emergency Response Team)",
            title_hi="CERT-In (भारतीय कंप्यूटर आपातकालीन प्रतिक्रिया टीम)",
            description="Report cyber security incidents",
            description_hi="साइबर सुरक्षा घटनाओं की रिपोर्ट करें",
            last_verified="2025-12-09"
        ),
        "sanchar_saathi": OfficialLink(
            url="https://sancharsaathi.gov.in",
            title="Sanchar Saathi Portal",
            title_hi="संचार साथी पोर्टल",
            description="Block lost/stolen mobile, report SIM fraud",
            description_hi="खोया/चोरी मोबाइल ब्लॉक करें, सिम धोखाधड़ी रिपोर्ट करें",
            last_verified="2025-12-09"
        ),
        "chakshu": OfficialLink(
            url="https://sancharsaathi.gov.in/sfc",
            title="Chakshu - Report Fraud Communications",
            title_hi="चक्षु - धोखाधड़ी संचार रिपोर्ट करें",
            description="Report suspected fraud calls/SMS",
            description_hi="संदिग्ध धोखाधड़ी कॉल/एसएमएस रिपोर्ट करें",
            last_verified="2025-12-09"
        ),
    }
    
    # Financial Fraud Reporting
    FINANCIAL_PORTALS = {
        "rbi_sachet": OfficialLink(
            url="https://sachet.rbi.org.in",
            title="RBI SACHET - Banking Complaints",
            title_hi="RBI SACHET - बैंकिंग शिकायतें",
            description="Reserve Bank complaint portal for banking issues",
            description_hi="बैंकिंग मुद्दों के लिए रिज़र्व बैंक शिकायत पोर्टल",
            last_verified="2025-12-09"
        ),
        "cfp": OfficialLink(
            url="https://consumerhelpline.gov.in",
            title="Consumer Helpline",
            title_hi="उपभोक्ता हेल्पलाइन",
            description="Consumer complaints and grievances",
            description_hi="उपभोक्ता शिकायतें",
            last_verified="2025-12-09"
        ),
    }
    
    # Platform-specific Reporting
    PLATFORM_LINKS = {
        "facebook_report": OfficialLink(
            url="https://www.facebook.com/help/263149623790594",
            title="Facebook - Report Hacked Account",
            title_hi="Facebook - हैक अकाउंट रिपोर्ट करें",
            description="Report compromised Facebook account",
            description_hi="समझौता किए गए Facebook खाते की रिपोर्ट करें",
            last_verified="2025-12-09"
        ),
        "instagram_report": OfficialLink(
            url="https://help.instagram.com/368191326593075",
            title="Instagram - Report Hacked Account",
            title_hi="Instagram - हैक अकाउंट रिपोर्ट करें",
            description="Report compromised Instagram account",
            description_hi="समझौता किए गए Instagram खाते की रिपोर्ट करें",
            last_verified="2025-12-09"
        ),
        "google_security": OfficialLink(
            url="https://support.google.com/accounts/answer/6294825",
            title="Google - Secure Compromised Account",
            title_hi="Google - समझौता किए गए खाते को सुरक्षित करें",
            description="Recover and secure hacked Google account",
            description_hi="हैक किए गए Google खाते को पुनर्प्राप्त और सुरक्षित करें",
            last_verified="2025-12-09"
        ),
        "twitter_report": OfficialLink(
            url="https://help.twitter.com/en/safety-and-security/account-compromised",
            title="Twitter/X - Hacked Account Help",
            title_hi="Twitter/X - हैक अकाउंट सहायता",
            description="Report and recover hacked Twitter account",
            description_hi="हैक किए गए Twitter खाते की रिपोर्ट करें",
            last_verified="2025-12-09"
        ),
    }
    
    # Bank-specific fraud reporting
    BANK_CONTACTS = {
        "sbi": {
            "name": "State Bank of India",
            "fraud_helpline": "1800-425-3800 / 1800-112-211",
            "email": "complaints@sbi.co.in",
            "reporting_url": "https://www.onlinesbi.sbi"
        },
        "hdfc": {
            "name": "HDFC Bank",
            "fraud_helpline": "1800-202-6161",
            "email": "phonebankingcell@hdfcbank.com",
            "reporting_url": "https://www.hdfcbank.com"
        },
        "icici": {
            "name": "ICICI Bank",
            "fraud_helpline": "1860-120-7777",
            "email": "customer.care@icicibank.com",
            "reporting_url": "https://www.icicibank.com"
        },
        "axis": {
            "name": "Axis Bank",
            "fraud_helpline": "1860-419-5555",
            "email": "customer.care@axisbank.com",
            "reporting_url": "https://www.axisbank.com"
        },
        "pnb": {
            "name": "Punjab National Bank",
            "fraud_helpline": "1800-180-2222",
            "email": "care@pnb.co.in",
            "reporting_url": "https://www.pnbindia.in"
        },
    }
    
    # Telecom operator contacts
    TELECOM_CONTACTS = {
        "airtel": {
            "name": "Airtel",
            "customer_care": "121",
            "fraud_helpline": "400",
            "email": "support@airtel.in"
        },
        "jio": {
            "name": "Reliance Jio",
            "customer_care": "198 / 1800-889-9999",
            "fraud_helpline": "198",
            "email": "care@jio.com"
        },
        "vi": {
            "name": "Vi (Vodafone Idea)",
            "customer_care": "199 / 1800-102-1234",
            "fraud_helpline": "199",
            "email": "support@myvi.in"
        },
        "bsnl": {
            "name": "BSNL",
            "customer_care": "1800-180-1503",
            "fraud_helpline": "1503",
            "email": "customercare.bsnl@gmail.com"
        },
    }
    
    # State Cyber Cell Contacts (Sample - would include all states)
    STATE_CYBER_CELLS = {
        "delhi": {
            "name": "Delhi Cyber Crime Unit",
            "phone": "011-23490592",
            "email": "cybercrimedelhi@gmail.com",
            "address": "IFSO, CBI Building, CGO Complex, Lodhi Road, New Delhi"
        },
        "maharashtra": {
            "name": "Maharashtra Cyber",
            "phone": "022-2620-1122",
            "email": "mahacyber1@mahapolice.gov.in",
            "address": "Cyber Crime Investigation Cell, Mumbai"
        },
        "karnataka": {
            "name": "Karnataka Cyber Crime",
            "phone": "080-22381010",
            "email": "cybercrime@ksp.gov.in",
            "address": "CID - Cyber Crime, Bengaluru"
        },
        "tamil_nadu": {
            "name": "Tamil Nadu Cyber Crime Wing",
            "phone": "044-23452373",
            "email": "ccw-cid@tn.gov.in",
            "address": "Cyber Crime Wing, Chennai"
        },
        "uttar_pradesh": {
            "name": "UP Cyber Crime Cell",
            "phone": "155260",
            "email": "cybercrime-up@gov.in",
            "address": "UP STF Cyber Crime Cell, Lucknow"
        },
        "west_bengal": {
            "name": "West Bengal Cyber Crime",
            "phone": "1930",
            "email": "kolcybercrime@gmail.com",
            "address": "Cyber Crime PS, Kolkata"
        },
        "telangana": {
            "name": "Telangana Cyber Crime",
            "phone": "040-27852499",
            "email": "tsccps@gmail.com",
            "address": "Cyber Crime Police Station, Hyderabad"
        },
        "gujarat": {
            "name": "Gujarat Cyber Crime",
            "phone": "1930",
            "email": "ccahmedabad@gmail.com",
            "address": "Cyber Crime Cell, Ahmedabad"
        },
    }
    
    # Government Advisories Sources
    ADVISORY_SOURCES = {
        "cert_in_advisories": OfficialLink(
            url="https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES01&VLCODE=CIVN",
            title="CERT-In Security Advisories",
            title_hi="CERT-In सुरक्षा सलाह",
            description="Latest cybersecurity advisories and vulnerabilities",
            description_hi="नवीनतम साइबर सुरक्षा सलाह",
            last_verified="2025-12-09"
        ),
        "rbi_alerts": OfficialLink(
            url="https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx",
            title="RBI Press Releases & Alerts",
            title_hi="RBI प्रेस विज्ञप्ति और अलर्ट",
            description="Banking fraud alerts and advisories from RBI",
            description_hi="RBI से बैंकिंग धोखाधड़ी अलर्ट",
            last_verified="2025-12-09"
        ),
        "meity": OfficialLink(
            url="https://www.meity.gov.in",
            title="Ministry of Electronics & IT",
            title_hi="इलेक्ट्रॉनिक्स और आईटी मंत्रालय",
            description="Government IT policies and cyber initiatives",
            description_hi="सरकारी आईटी नीतियां",
            last_verified="2025-12-09"
        ),
    }


def get_relevant_links(crime_type: str, language: str = "en") -> Dict[str, List[OfficialLink]]:
    """Get relevant official links based on crime type"""
    db = OfficialContactDatabase()
    
    links = {
        "primary_portals": [],
        "helplines": [],
        "platform_links": [],
        "advisories": []
    }
    
    # Always include main portals
    links["primary_portals"].append(db.REPORTING_PORTALS["cybercrime_portal"])
    links["primary_portals"].append(db.REPORTING_PORTALS["cert_in"])
    
    # Always include national helpline
    links["helplines"].append(db.HELPLINES["cybercrime"])
    
    # Add crime-specific links
    if "financial" in crime_type or "upi" in crime_type or "bank" in crime_type:
        links["primary_portals"].append(db.FINANCIAL_PORTALS["rbi_sachet"])
        links["advisories"].append(db.ADVISORY_SOURCES["rbi_alerts"])
    
    if "sim" in crime_type or "mobile" in crime_type:
        links["primary_portals"].append(db.REPORTING_PORTALS["sanchar_saathi"])
        links["primary_portals"].append(db.REPORTING_PORTALS["chakshu"])
    
    if "social_media" in crime_type or "instagram" in crime_type or "facebook" in crime_type:
        links["platform_links"].append(db.PLATFORM_LINKS["facebook_report"])
        links["platform_links"].append(db.PLATFORM_LINKS["instagram_report"])
    
    if "email" in crime_type or "gmail" in crime_type:
        links["platform_links"].append(db.PLATFORM_LINKS["google_security"])
    
    if "sextortion" in crime_type or "harassment" in crime_type:
        links["helplines"].append(db.HELPLINES["women"])
    
    if "child" in crime_type:
        links["helplines"].append(db.HELPLINES["child"])
    
    # Add advisories
    links["advisories"].append(db.ADVISORY_SOURCES["cert_in_advisories"])
    
    return links


def get_bank_contact(bank_name: str) -> Dict:
    """Get specific bank fraud reporting contact"""
    db = OfficialContactDatabase()
    bank_key = bank_name.lower().replace(" ", "_")
    
    return db.BANK_CONTACTS.get(bank_key, {})


def get_telecom_contact(operator_name: str) -> Dict:
    """Get specific telecom operator contact"""
    db = OfficialContactDatabase()
    operator_key = operator_name.lower()
    
    return db.TELECOM_CONTACTS.get(operator_key, {})


def get_state_cyber_cell(state_name: str) -> Dict:
    """Get state-specific cyber cell contact"""
    db = OfficialContactDatabase()
    state_key = state_name.lower().replace(" ", "_")
    
    return db.STATE_CYBER_CELLS.get(state_key, {})
