"""
Application Constants
"""

# Emergency Contacts
EMERGENCY_CONTACTS = {
    "CYBER_FRAUD_HELPLINE": {
        "number": "1930",
        "name": "National Cyber Fraud Helpline",
        "description": "24x7 helpline for financial fraud reporting",
        "available_24x7": True
    },
    "WOMEN_HELPLINE": {
        "number": "181",
        "name": "Women's Helpline",
        "description": "Helpline for women in distress",
        "available_24x7": True
    },
    "POLICE_EMERGENCY": {
        "number": "112",
        "name": "Police Emergency",
        "description": "National emergency number",
        "available_24x7": True
    }
}

# Official Links
OFFICIAL_LINKS = {
    "CYBERCRIME_PORTAL": {
        "name": "National Cyber Crime Reporting Portal",
        "url": "https://cybercrime.gov.in",
        "category": "reporting",
        "description": "Official portal to report cybercrimes"
    },
    "CERT_IN": {
        "name": "CERT-In",
        "url": "https://www.cert-in.org.in",
        "category": "advisory",
        "description": "Indian Computer Emergency Response Team"
    },
    "RBI_FRAUD": {
        "name": "RBI - Report Banking Fraud",
        "url": "https://www.rbi.org.in",
        "category": "banking",
        "description": "Reserve Bank of India fraud reporting"
    }
}

# Platform Reporting Links
PLATFORM_LINKS = {
    "facebook": {
        "report_url": "https://www.facebook.com/help/",
        "support": "https://www.facebook.com/help/263149623790594"
    },
    "instagram": {
        "report_url": "https://help.instagram.com/",
        "support": "https://help.instagram.com/192435014247952"
    },
    "whatsapp": {
        "report_url": "https://www.whatsapp.com/contact/",
        "support": "https://faq.whatsapp.com/general/security-and-privacy/how-to-report-spam-or-block-a-contact"
    },
    "twitter": {
        "report_url": "https://help.twitter.com/forms",
        "support": "https://help.twitter.com/en/safety-and-security"
    }
}

# Crime Type Keywords (for classification)
CRIME_KEYWORDS = {
    "financial_fraud": ["money", "payment", "transaction", "bank", "upi", "fraud", "scam", "lost money"],
    "phishing": ["fake link", "suspicious email", "phishing", "fake website", "otp"],
    "social_media_hack": ["account hacked", "cannot login", "password changed", "unauthorized access"],
    "fake_profile": ["fake account", "fake profile", "impersonation", "someone using my photo"],
    "harassment": ["threats", "harassment", "bullying", "abuse", "blackmail"],
    "ransomware": ["files encrypted", "ransom", "cannot access", "locked"],
}
