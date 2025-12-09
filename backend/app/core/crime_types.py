"""
Crime Type Classification System
Comprehensive categorization of 20+ cybercrime types
"""
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class CrimeType(str, Enum):
    """Extended cybercrime type classification"""
    # Financial Crimes
    UPI_FRAUD = "upi_fraud"
    NET_BANKING_FRAUD = "net_banking_fraud"
    CREDIT_CARD_FRAUD = "credit_card_fraud"
    INVESTMENT_SCAM = "investment_scam"
    LOAN_FRAUD = "loan_fraud"
    CRYPTOCURRENCY_SCAM = "cryptocurrency_scam"
    
    # Identity & Account Crimes
    SOCIAL_MEDIA_HACKING = "social_media_hacking"
    EMAIL_HACKING = "email_hacking"
    IDENTITY_THEFT = "identity_theft"
    AADHAR_MISUSE = "aadhar_misuse"
    SIM_SWAP_FRAUD = "sim_swap_fraud"
    
    # Harassment & Extortion
    SEXTORTION = "sextortion"
    CYBERBULLYING = "cyberbullying"
    ONLINE_HARASSMENT = "online_harassment"
    REVENGE_PORN = "revenge_porn"
    BLACKMAIL = "blackmail"
    
    # Deception & Fraud
    JOB_FRAUD = "job_fraud"
    MATRIMONIAL_FRAUD = "matrimonial_fraud"
    LOTTERY_SCAM = "lottery_scam"
    PHISHING = "phishing"
    VISHING = "vishing"
    SMISHING = "smishing"
    
    # E-commerce & Services
    ONLINE_SHOPPING_FRAUD = "online_shopping_fraud"
    FAKE_WEBSITE = "fake_website"
    APP_FRAUD = "app_fraud"
    
    # Cyber Attacks
    RANSOMWARE = "ransomware"
    DATA_BREACH = "data_breach"
    WEBSITE_DEFACEMENT = "website_defacement"
    
    # Other
    FAKE_NEWS = "fake_news"
    CHILD_PORNOGRAPHY = "child_pornography"
    OTHER = "other"


class CrimeMetadata(BaseModel):
    """Metadata for each crime type"""
    display_name: str
    display_name_hi: str  # Hindi
    category: str
    severity: str  # low, medium, high, critical
    typical_loss_range: Optional[str]
    keywords: List[str]
    keywords_hi: List[str]  # Hindi keywords


# Comprehensive crime type database
CRIME_TYPE_DATABASE: Dict[CrimeType, CrimeMetadata] = {
    CrimeType.UPI_FRAUD: CrimeMetadata(
        display_name="UPI/Digital Payment Fraud",
        display_name_hi="UPI/डिजिटल पेमेंट धोखाधड़ी",
        category="Financial Crime",
        severity="high",
        typical_loss_range="₹5,000 - ₹5,00,000",
        keywords=["upi", "phonepe", "paytm", "gpay", "wrong transfer", "payment fraud", "qr code"],
        keywords_hi=["यूपीआई", "फोनपे", "पेटीएम", "गूगल पे", "गलत ट्रांसफर", "पेमेंट धोखा"]
    ),
    CrimeType.NET_BANKING_FRAUD: CrimeMetadata(
        display_name="Net Banking/Online Banking Fraud",
        display_name_hi="नेट बैंकिंग धोखाधड़ी",
        category="Financial Crime",
        severity="high",
        typical_loss_range="₹10,000 - ₹10,00,000",
        keywords=["net banking", "online banking", "unauthorized transaction", "bank account hacked"],
        keywords_hi=["नेट बैंकिंग", "ऑनलाइन बैंकिंग", "अनधिकृत लेनदेन", "खाता हैक"]
    ),
    CrimeType.CREDIT_CARD_FRAUD: CrimeMetadata(
        display_name="Credit/Debit Card Fraud",
        display_name_hi="क्रेडिट/डेबिट कार्ड धोखाधड़ी",
        category="Financial Crime",
        severity="high",
        typical_loss_range="₹5,000 - ₹2,00,000",
        keywords=["credit card", "debit card", "card cloning", "cvv", "swipe fraud", "card skimming"],
        keywords_hi=["क्रेडिट कार्ड", "डेबिट कार्ड", "कार्ड क्लोनिंग", "सीवीवी"]
    ),
    CrimeType.INVESTMENT_SCAM: CrimeMetadata(
        display_name="Investment/Trading Scam",
        display_name_hi="निवेश/ट्रेडिंग घोटाला",
        category="Financial Crime",
        severity="critical",
        typical_loss_range="₹50,000 - ₹50,00,000",
        keywords=["investment", "trading", "stock market", "mutual fund", "ponzi", "mlm", "high returns"],
        keywords_hi=["निवेश", "ट्रेडिंग", "शेयर बाजार", "म्यूचुअल फंड", "पोंजी"]
    ),
    CrimeType.LOAN_FRAUD: CrimeMetadata(
        display_name="Loan Fraud/Aadhar Loan",
        display_name_hi="ऋण धोखाधड़ी/आधार पर लोन",
        category="Financial Crime",
        severity="high",
        typical_loss_range="₹20,000 - ₹5,00,000",
        keywords=["loan on aadhar", "unauthorized loan", "instant loan app", "loan fraud"],
        keywords_hi=["आधार पर लोन", "अनधिकृत लोन", "तुरंत लोन ऐप"]
    ),
    CrimeType.CRYPTOCURRENCY_SCAM: CrimeMetadata(
        display_name="Cryptocurrency Scam",
        display_name_hi="क्रिप्टोकरेंसी घोटाला",
        category="Financial Crime",
        severity="critical",
        typical_loss_range="₹50,000 - ₹1,00,00,000",
        keywords=["bitcoin", "cryptocurrency", "crypto", "ethereum", "trading scam", "wallet hack"],
        keywords_hi=["बिटकॉइन", "क्रिप्टो", "क्रिप्टोकरेंसी"]
    ),
    CrimeType.SOCIAL_MEDIA_HACKING: CrimeMetadata(
        display_name="Social Media Account Hacking",
        display_name_hi="सोशल मीडिया अकाउंट हैकिंग",
        category="Identity Crime",
        severity="medium",
        typical_loss_range="N/A",
        keywords=["instagram hacked", "facebook hacked", "twitter hacked", "account taken over", "fake profile"],
        keywords_hi=["इंस्टाग्राम हैक", "फेसबुक हैक", "ट्विटर हैक", "नकली प्रोफाइल"]
    ),
    CrimeType.EMAIL_HACKING: CrimeMetadata(
        display_name="Email Account Hacking",
        display_name_hi="ईमेल अकाउंट हैकिंग",
        category="Identity Crime",
        severity="high",
        typical_loss_range="N/A",
        keywords=["email hacked", "gmail hacked", "password changed", "cannot access email"],
        keywords_hi=["ईमेल हैक", "जीमेल हैक", "पासवर्ड बदला"]
    ),
    CrimeType.IDENTITY_THEFT: CrimeMetadata(
        display_name="Identity Theft",
        display_name_hi="पहचान की चोरी",
        category="Identity Crime",
        severity="critical",
        typical_loss_range="Varies",
        keywords=["identity theft", "impersonation", "fake documents", "someone using my identity"],
        keywords_hi=["पहचान चोरी", "नकली दस्तावेज", "मेरी पहचान का दुरुपयोग"]
    ),
    CrimeType.AADHAR_MISUSE: CrimeMetadata(
        display_name="Aadhar Card Misuse",
        display_name_hi="आधार कार्ड दुरुपयोग",
        category="Identity Crime",
        severity="high",
        typical_loss_range="Varies",
        keywords=["aadhar misuse", "aadhaar fraud", "unauthorized aadhar use", "loan on my aadhar"],
        keywords_hi=["आधार दुरुपयोग", "आधार धोखाधड़ी", "मेरे आधार पर लोन"]
    ),
    CrimeType.SIM_SWAP_FRAUD: CrimeMetadata(
        display_name="SIM Swap Fraud",
        display_name_hi="सिम स्वैप धोखाधड़ी",
        category="Identity Crime",
        severity="critical",
        typical_loss_range="₹10,000 - ₹10,00,000",
        keywords=["sim swap", "sim cloning", "number porting fraud", "lost sim card"],
        keywords_hi=["सिम स्वैप", "सिम क्लोनिंग", "नंबर पोर्टिंग"]
    ),
    CrimeType.SEXTORTION: CrimeMetadata(
        display_name="Sextortion/Blackmail with Intimate Content",
        display_name_hi="अश्लील सामग्री से ब्लैकमेल",
        category="Harassment",
        severity="critical",
        typical_loss_range="₹10,000 - ₹5,00,000",
        keywords=["sextortion", "blackmail", "intimate photos", "video call recording", "nude photos"],
        keywords_hi=["यौन शोषण", "ब्लैकमेल", "अश्लील फोटो", "वीडियो कॉल रिकॉर्डिंग"]
    ),
    CrimeType.CYBERBULLYING: CrimeMetadata(
        display_name="Cyberbullying",
        display_name_hi="साइबर धमकी",
        category="Harassment",
        severity="medium",
        typical_loss_range="N/A",
        keywords=["cyberbullying", "online harassment", "trolling", "hate messages"],
        keywords_hi=["साइबर धमकी", "ऑनलाइन उत्पीड़न", "नफरत संदेश"]
    ),
    CrimeType.ONLINE_HARASSMENT: CrimeMetadata(
        display_name="Online Harassment/Stalking",
        display_name_hi="ऑनलाइन उत्पीड़न/पीछा करना",
        category="Harassment",
        severity="high",
        typical_loss_range="N/A",
        keywords=["stalking", "harassment", "threatening messages", "abuse online"],
        keywords_hi=["पीछा करना", "उत्पीड़न", "धमकी संदेश"]
    ),
    CrimeType.REVENGE_PORN: CrimeMetadata(
        display_name="Revenge Porn/Non-consensual Sharing",
        display_name_hi="बदला पोर्न/गैर-सहमति साझाकरण",
        category="Harassment",
        severity="critical",
        typical_loss_range="N/A",
        keywords=["revenge porn", "intimate images shared", "morphed photos", "deepfake"],
        keywords_hi=["बदला पोर्न", "अश्लील फोटो शेयर", "फोटो एडिट"]
    ),
    CrimeType.BLACKMAIL: CrimeMetadata(
        display_name="General Blackmail/Extortion",
        display_name_hi="ब्लैकमेल/जबरन वसूली",
        category="Harassment",
        severity="high",
        typical_loss_range="₹10,000 - ₹10,00,000",
        keywords=["blackmail", "extortion", "threatening", "demanding money"],
        keywords_hi=["ब्लैकमेल", "जबरन वसूली", "धमकी", "पैसे की मांग"]
    ),
    CrimeType.JOB_FRAUD: CrimeMetadata(
        display_name="Online Job/Employment Fraud",
        display_name_hi="नौकरी धोखाधड़ी",
        category="Deception",
        severity="high",
        typical_loss_range="₹5,000 - ₹50,000",
        keywords=["job fraud", "fake job offer", "work from home scam", "registration fee"],
        keywords_hi=["नौकरी धोखा", "नकली नौकरी", "घर से काम", "रजिस्ट्रेशन फीस"]
    ),
    CrimeType.MATRIMONIAL_FRAUD: CrimeMetadata(
        display_name="Matrimonial/Dating Fraud",
        display_name_hi="शादी/डेटिंग धोखाधड़ी",
        category="Deception",
        severity="high",
        typical_loss_range="₹50,000 - ₹10,00,000",
        keywords=["matrimonial fraud", "dating scam", "fake profile", "marriage fraud"],
        keywords_hi=["शादी धोखा", "डेटिंग घोटाला", "नकली प्रोफाइल"]
    ),
    CrimeType.LOTTERY_SCAM: CrimeMetadata(
        display_name="Lottery/Prize Winner Scam",
        display_name_hi="लॉटरी/पुरस्कार विजेता घोटाला",
        category="Deception",
        severity="medium",
        typical_loss_range="₹5,000 - ₹50,000",
        keywords=["lottery scam", "won prize", "kbc winner", "lucky draw"],
        keywords_hi=["लॉटरी स्कैम", "पुरस्कार जीता", "केबीसी विजेता", "लकी ड्रा"]
    ),
    CrimeType.PHISHING: CrimeMetadata(
        display_name="Phishing (Email/Website)",
        display_name_hi="फिशिंग (ईमेल/वेबसाइट)",
        category="Deception",
        severity="high",
        typical_loss_range="₹5,000 - ₹2,00,000",
        keywords=["phishing", "fake email", "fake website", "kyc update", "verify account"],
        keywords_hi=["फिशिंग", "नकली ईमेल", "नकली वेबसाइट", "केवाईसी अपडेट"]
    ),
    CrimeType.VISHING: CrimeMetadata(
        display_name="Vishing (Voice Call Fraud)",
        display_name_hi="विशिंग (वॉइस कॉल धोखाधड़ी)",
        category="Deception",
        severity="high",
        typical_loss_range="₹10,000 - ₹5,00,000",
        keywords=["vishing", "fake call", "bank call fraud", "customer care scam"],
        keywords_hi=["विशिंग", "नकली कॉल", "बैंक कॉल धोखा", "कस्टमर केयर स्कैम"]
    ),
    CrimeType.SMISHING: CrimeMetadata(
        display_name="Smishing (SMS Fraud)",
        display_name_hi="स्मिशिंग (एसएमएस धोखाधड़ी)",
        category="Deception",
        severity="medium",
        typical_loss_range="₹5,000 - ₹1,00,000",
        keywords=["smishing", "fake sms", "otp fraud", "link in sms"],
        keywords_hi=["स्मिशिंग", "नकली एसएमएस", "ओटीपी धोखा"]
    ),
    CrimeType.ONLINE_SHOPPING_FRAUD: CrimeMetadata(
        display_name="Online Shopping/E-commerce Fraud",
        display_name_hi="ऑनलाइन शॉपिंग धोखाधड़ी",
        category="E-commerce",
        severity="medium",
        typical_loss_range="₹1,000 - ₹50,000",
        keywords=["online shopping fraud", "fake seller", "product not received", "olx fraud", "quikr scam"],
        keywords_hi=["ऑनलाइन शॉपिंग धोखा", "नकली विक्रेता", "सामान नहीं मिला"]
    ),
    CrimeType.FAKE_WEBSITE: CrimeMetadata(
        display_name="Fake Website/Cloned Site",
        display_name_hi="नकली वेबसाइट",
        category="E-commerce",
        severity="high",
        typical_loss_range="₹5,000 - ₹1,00,000",
        keywords=["fake website", "cloned website", "phishing site", "look-alike domain"],
        keywords_hi=["नकली वेबसाइट", "फर्जी साइट"]
    ),
    CrimeType.APP_FRAUD: CrimeMetadata(
        display_name="Fake Mobile App Fraud",
        display_name_hi="नकली मोबाइल ऐप धोखाधड़ी",
        category="E-commerce",
        severity="high",
        typical_loss_range="₹5,000 - ₹2,00,000",
        keywords=["fake app", "malicious app", "loan app fraud", "gaming app scam"],
        keywords_hi=["नकली ऐप", "लोन ऐप धोखा", "गेमिंग ऐप स्कैम"]
    ),
    CrimeType.RANSOMWARE: CrimeMetadata(
        display_name="Ransomware Attack",
        display_name_hi="रैंसमवेयर हमला",
        category="Cyber Attack",
        severity="critical",
        typical_loss_range="₹50,000 - ₹50,00,000",
        keywords=["ransomware", "files encrypted", "data locked", "bitcoin demand"],
        keywords_hi=["रैंसमवेयर", "फाइलें एन्क्रिप्ट", "डेटा लॉक"]
    ),
    CrimeType.DATA_BREACH: CrimeMetadata(
        display_name="Data Breach/Leak",
        display_name_hi="डेटा उल्लंघन/लीक",
        category="Cyber Attack",
        severity="critical",
        typical_loss_range="Varies",
        keywords=["data breach", "data leak", "database hacked", "personal info leaked"],
        keywords_hi=["डेटा उल्लंघन", "डेटा लीक", "व्यक्तिगत जानकारी लीक"]
    ),
    CrimeType.WEBSITE_DEFACEMENT: CrimeMetadata(
        display_name="Website Defacement/Hacking",
        display_name_hi="वेबसाइट हैकिंग",
        category="Cyber Attack",
        severity="high",
        typical_loss_range="Varies",
        keywords=["website hacked", "website defaced", "site compromised"],
        keywords_hi=["वेबसाइट हैक", "साइट से छेड़छाड़"]
    ),
    CrimeType.FAKE_NEWS: CrimeMetadata(
        display_name="Fake News/Misinformation",
        display_name_hi="फेक न्यूज/गलत सूचना",
        category="Other",
        severity="low",
        typical_loss_range="N/A",
        keywords=["fake news", "misinformation", "false rumor", "propaganda"],
        keywords_hi=["फेक न्यूज", "गलत सूचना", "झूठी अफवाह"]
    ),
    CrimeType.CHILD_PORNOGRAPHY: CrimeMetadata(
        display_name="Child Sexual Abuse Material (CSAM)",
        display_name_hi="बाल यौन शोषण सामग्री",
        category="Critical",
        severity="critical",
        typical_loss_range="N/A",
        keywords=["child pornography", "csam", "child abuse", "child exploitation"],
        keywords_hi=["बाल पोर्नोग्राफी", "बाल शोषण"]
    ),
    CrimeType.OTHER: CrimeMetadata(
        display_name="Other Cybercrime",
        display_name_hi="अन्य साइबर अपराध",
        category="Other",
        severity="medium",
        typical_loss_range="Varies",
        keywords=["cybercrime", "online fraud", "internet scam"],
        keywords_hi=["साइबर अपराध", "ऑनलाइन धोखाधड़ी"]
    ),
}


def classify_crime_type(query: str, language: str = "en") -> CrimeType:
    """
    Classify query into crime type based on keywords
    Returns best matching crime type
    """
    query_lower = query.lower()
    scores = {}
    
    for crime_type, metadata in CRIME_TYPE_DATABASE.items():
        score = 0
        keywords = metadata.keywords if language == "en" else metadata.keywords_hi
        
        for keyword in keywords:
            if keyword.lower() in query_lower:
                score += 1
        
        if score > 0:
            scores[crime_type] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return CrimeType.OTHER


def get_crime_display_name(crime_type: CrimeType, language: str = "en") -> str:
    """Get localized display name for crime type"""
    metadata = CRIME_TYPE_DATABASE.get(crime_type)
    if not metadata:
        return "Unknown Crime"
    
    return metadata.display_name if language == "en" else metadata.display_name_hi
