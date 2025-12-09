"""
SOP Templates - Dynamic Standard Operating Procedure Generation
Timeline-based action items with evidence checklists
"""
from typing import Dict, List
from pydantic import BaseModel
from app.core.crime_types import CrimeType


class ActionItem(BaseModel):
    """Individual action item"""
    timeline: str  # NOW, WITHIN_24_HOURS, WITHIN_7_DAYS, ONGOING
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    action: str
    action_hi: str
    details: str
    details_hi: str
    links: List[str] = []


class EvidenceItem(BaseModel):
    """Evidence checklist item"""
    item: str
    item_hi: str
    mandatory: bool
    example: str
    example_hi: str


class SOPTemplate(BaseModel):
    """Complete SOP template for a crime type"""
    crime_type: CrimeType
    immediate_actions: List[ActionItem]
    within_24h_actions: List[ActionItem]
    within_7d_actions: List[ActionItem]
    ongoing_actions: List[ActionItem]
    evidence_checklist: List[EvidenceItem]
    important_notes: List[str]
    important_notes_hi: List[str]
    disclaimers: List[str]
    disclaimers_hi: List[str]


# SOP Templates Database
SOP_TEMPLATES: Dict[CrimeType, SOPTemplate] = {
    CrimeType.UPI_FRAUD: SOPTemplate(
        crime_type=CrimeType.UPI_FRAUD,
        immediate_actions=[
            ActionItem(
                timeline="NOW",
                priority="CRITICAL",
                action="Call your bank immediately",
                action_hi="तुरंत अपने बैंक को कॉल करें",
                details="Report unauthorized transaction to block further debits. Use bank's 24x7 fraud helpline number.",
                details_hi="अनधिकृत लेनदेन की रिपोर्ट करें। बैंक की 24x7 धोखाधड़ी हेल्पलाइन नंबर का उपयोग करें।",
                links=["bank_helpline"]
            ),
            ActionItem(
                timeline="NOW",
                priority="CRITICAL",
                action="Block UPI ID/VPA",
                action_hi="UPI ID/VPA ब्लॉक करें",
                details="Contact your UPI app provider (PhonePe/Paytm/GPay) to block compromised UPI ID",
                details_hi="अपने UPI ऐप प्रदाता से संपर्क करें",
                links=[]
            ),
            ActionItem(
                timeline="NOW",
                priority="HIGH",
                action="Take screenshots",
                action_hi="स्क्रीनशॉट लें",
                details="Capture transaction details, messages, caller ID if applicable",
                details_hi="लेनदेन विवरण, संदेश, कॉलर आईडी कैप्चर करें",
                links=[]
            ),
        ],
        within_24h_actions=[
            ActionItem(
                timeline="WITHIN_24_HOURS",
                priority="CRITICAL",
                action="File complaint on cybercrime.gov.in",
                action_hi="cybercrime.gov.in पर शिकायत दर्ज करें",
                details="Register FIR online with all transaction details and evidence",
                details_hi="सभी लेनदेन विवरण और सबूत के साथ ऑनलाइन FIR दर्ज करें",
                links=["https://cybercrime.gov.in"]
            ),
            ActionItem(
                timeline="WITHIN_24_HOURS",
                priority="HIGH",
                action="Report to bank in writing",
                action_hi="बैंक को लिखित में रिपोर्ट करें",
                details="Send email with FIR copy and request chargeback/reversal",
                details_hi="FIR कॉपी के साथ ईमेल भेजें और चार्जबैक/रिवर्सल का अनुरोध करें",
                links=[]
            ),
            ActionItem(
                timeline="WITHIN_24_HOURS",
                priority="MEDIUM",
                action="Change all banking passwords",
                action_hi="सभी बैंकिंग पासवर्ड बदलें",
                details="Update UPI PIN, net banking password, mobile banking PIN",
                details_hi="UPI पिन, नेट बैंकिंग पासवर्ड, मोबाइल बैंकिंग पिन अपडेट करें",
                links=[]
            ),
        ],
        within_7d_actions=[
            ActionItem(
                timeline="WITHIN_7_DAYS",
                priority="HIGH",
                action="File complaint with RBI if bank doesn't respond",
                action_hi="यदि बैंक जवाब नहीं देता है तो RBI में शिकायत दर्ज करें",
                details="Use RBI SACHET portal for banking complaints",
                details_hi="बैंकिंग शिकायतों के लिए RBI SACHET पोर्टल का उपयोग करें",
                links=["https://sachet.rbi.org.in"]
            ),
            ActionItem(
                timeline="WITHIN_7_DAYS",
                priority="MEDIUM",
                action="Visit nearest police station",
                action_hi="निकटतम पुलिस स्टेशन जाएं",
                details="If online FIR not registered, file physical FIR with all evidence",
                details_hi="यदि ऑनलाइन FIR दर्ज नहीं हुई है, तो सभी सबूतों के साथ भौतिक FIR दर्ज करें",
                links=[]
            ),
        ],
        ongoing_actions=[
            ActionItem(
                timeline="ONGOING",
                priority="MEDIUM",
                action="Follow up on complaint status",
                action_hi="शिकायत स्थिति पर फॉलो अप करें",
                details="Check cybercrime portal and bank regularly for updates",
                details_hi="अपडेट के लिए नियमित रूप से साइबर अपराध पोर्टल और बैंक की जांच करें",
                links=[]
            ),
            ActionItem(
                timeline="ONGOING",
                priority="LOW",
                action="Enable transaction alerts",
                action_hi="लेनदेन अलर्ट सक्षम करें",
                details="Set up SMS/email alerts for all future transactions",
                details_hi="सभी भविष्य के लेनदेन के लिए SMS/ईमेल अलर्ट सेट करें",
                links=[]
            ),
        ],
        evidence_checklist=[
            EvidenceItem(
                item="Transaction screenshots",
                item_hi="लेनदेन स्क्रीनशॉट",
                mandatory=True,
                example="UPI app transaction history showing unauthorized debit",
                example_hi="अनधिकृत डेबिट दिखाने वाला UPI ऐप लेनदेन इतिहास"
            ),
            EvidenceItem(
                item="Bank SMS/email notifications",
                item_hi="बैंक SMS/ईमेल सूचनाएं",
                mandatory=True,
                example="Transaction alert messages with date, time, amount",
                example_hi="तारीख, समय, राशि के साथ लेनदेन अलर्ट संदेश"
            ),
            EvidenceItem(
                item="Communication records",
                item_hi="संचार रिकॉर्ड",
                mandatory=False,
                example="Call logs, WhatsApp chats if scammer contacted you",
                example_hi="कॉल लॉग, WhatsApp चैट यदि स्कैमर ने संपर्क किया"
            ),
            EvidenceItem(
                item="Recipient account details",
                item_hi="प्राप्तकर्ता खाता विवरण",
                mandatory=True,
                example="UPI ID/Account number where money was transferred",
                example_hi="UPI ID/खाता संख्या जहां पैसे ट्रांसफर किए गए"
            ),
            EvidenceItem(
                item="Timeline of events",
                item_hi="घटनाओं की समयरेखा",
                mandatory=True,
                example="Written sequence: when scam started, what happened, when money lost",
                example_hi="लिखित क्रम: घोटाला कब शुरू हुआ, क्या हुआ, पैसे कब खोए"
            ),
        ],
        important_notes=[
            "UPI transactions can be reversed within 24 hours if reported immediately",
            "Zero Liability policy applies if you report within 3 days",
            "Do NOT share OTP, UPI PIN, CVV with anyone - banks never ask for these",
            "File both online cybercrime complaint AND inform your bank",
        ],
        important_notes_hi=[
            "यदि तुरंत रिपोर्ट किया जाए तो UPI लेनदेन 24 घंटे के भीतर उलटा किया जा सकता है",
            "यदि आप 3 दिनों के भीतर रिपोर्ट करते हैं तो शून्य देयता नीति लागू होती है",
            "OTP, UPI पिन, CVV किसी के साथ साझा न करें - बैंक कभी इन्हें नहीं मांगते",
            "ऑनलाइन साइबर अपराध शिकायत दर्ज करें और अपने बैंक को सूचित करें",
        ],
        disclaimers=[
            "Filing complaint on cybercrime.gov.in is equivalent to FIR in most cases",
            "This is AI-generated guidance. Verify all steps with official sources",
            "Legal advice: Consult with a lawyer for complex cases",
            "Recovery is not guaranteed but timely action increases chances",
        ],
        disclaimers_hi=[
            "cybercrime.gov.in पर शिकायत दर्ज करना अधिकांश मामलों में FIR के बराबर है",
            "यह AI-जनित मार्गदर्शन है। आधिकारिक स्रोतों के साथ सभी चरणों को सत्यापित करें",
            "कानूनी सलाह: जटिल मामलों के लिए वकील से परामर्श करें",
            "वसूली की गारंटी नहीं है लेकिन समय पर कार्रवाई से संभावना बढ़ जाती है",
        ],
    ),
    
    CrimeType.SOCIAL_MEDIA_HACKING: SOPTemplate(
        crime_type=CrimeType.SOCIAL_MEDIA_HACKING,
        immediate_actions=[
            ActionItem(
                timeline="NOW",
                priority="CRITICAL",
                action="Try to recover account via platform",
                action_hi="प्लेटफॉर्म के माध्यम से अकाउंट रिकवर करने का प्रयास करें",
                details="Use 'Forgot Password' or 'Account Compromised' option on the platform",
                details_hi="प्लेटफॉर्म पर 'पासवर्ड भूल गए' या 'अकाउंट से छेड़छाड़' विकल्प का उपयोग करें",
                links=["platform_recovery_link"]
            ),
            ActionItem(
                timeline="NOW",
                priority="CRITICAL",
                action="Change passwords of linked accounts",
                action_hi="लिंक किए गए खातों के पासवर्ड बदलें",
                details="Update email, phone number, other social media passwords immediately",
                details_hi="ईमेल, फोन नंबर, अन्य सोशल मीडिया पासवर्ड तुरंत अपडेट करें",
                links=[]
            ),
            ActionItem(
                timeline="NOW",
                priority="HIGH",
                action="Alert friends/followers",
                action_hi="दोस्तों/फॉलोअर्स को अलर्ट करें",
                details="Post from alternate account warning others about fake messages from your hacked account",
                details_hi="वैकल्पिक खाते से पोस्ट करें कि हैक किए गए खाते से नकली संदेशों के बारे में चेतावनी दें",
                links=[]
            ),
        ],
        within_24h_actions=[
            ActionItem(
                timeline="WITHIN_24_HOURS",
                priority="HIGH",
                action="Report to platform",
                action_hi="प्लेटफॉर्म को रिपोर्ट करें",
                details="Submit official hacked account report on Facebook/Instagram/Twitter help center",
                details_hi="Facebook/Instagram/Twitter हेल्प सेंटर पर आधिकारिक हैक अकाउंट रिपोर्ट सबमिट करें",
                links=["platform_report_link"]
            ),
            ActionItem(
                timeline="WITHIN_24_HOURS",
                priority="HIGH",
                action="File cybercrime complaint",
                action_hi="साइबर अपराध शिकायत दर्ज करें",
                details="Register complaint on cybercrime.gov.in if financial fraud or harassment involved",
                details_hi="यदि वित्तीय धोखाधड़ी या उत्पीड़न शामिल है तो cybercrime.gov.in पर शिकायत दर्ज करें",
                links=["https://cybercrime.gov.in"]
            ),
            ActionItem(
                timeline="WITHIN_24_HOURS",
                priority="MEDIUM",
                action="Enable two-factor authentication",
                action_hi="दो-कारक प्रमाणीकरण सक्षम करें",
                details="After recovery, enable 2FA on all social accounts",
                details_hi="रिकवरी के बाद, सभी सोशल अकाउंट पर 2FA सक्षम करें",
                links=[]
            ),
        ],
        within_7d_actions=[
            ActionItem(
                timeline="WITHIN_7_DAYS",
                priority="MEDIUM",
                action="Monitor for misuse",
                action_hi="दुरुपयोग के लिए निगरानी करें",
                details="Check if hacker posted objectionable content or messaged contacts",
                details_hi="जांचें कि क्या हैकर ने आपत्तिजनक सामग्री पोस्ट की या संपर्कों को संदेश भेजे",
                links=[]
            ),
            ActionItem(
                timeline="WITHIN_7_DAYS",
                priority="LOW",
                action="Review login activity",
                action_hi="लॉगिन गतिविधि की समीक्षा करें",
                details="Check account settings for suspicious login locations/devices",
                details_hi="संदिग्ध लॉगिन स्थानों/उपकरणों के लिए खाता सेटिंग्स की जांच करें",
                links=[]
            ),
        ],
        ongoing_actions=[
            ActionItem(
                timeline="ONGOING",
                priority="MEDIUM",
                action="Follow up on recovery request",
                action_hi="रिकवरी अनुरोध पर फॉलो अप करें",
                details="Platform may take 2-7 days to verify and restore account",
                details_hi="प्लेटफॉर्म को खाता सत्यापित और पुनर्स्थापित करने में 2-7 दिन लग सकते हैं",
                links=[]
            ),
        ],
        evidence_checklist=[
            EvidenceItem(
                item="Screenshots of hacked account",
                item_hi="हैक किए गए अकाउंट के स्क्रीनशॉट",
                mandatory=True,
                example="Changed profile picture, bio, unauthorized posts",
                example_hi="बदली गई प्रोफ़ाइल तस्वीर, बायो, अनधिकृत पोस्ट"
            ),
            EvidenceItem(
                item="Email notifications",
                item_hi="ईमेल सूचनाएं",
                mandatory=True,
                example="Password change alerts, login from new device emails",
                example_hi="पासवर्ड परिवर्तन अलर्ट, नए डिवाइस से लॉगिन ईमेल"
            ),
            EvidenceItem(
                item="Messages sent by hacker",
                item_hi="हैकर द्वारा भेजे गए संदेश",
                mandatory=False,
                example="Screenshots of spam/fraud messages sent from your account",
                example_hi="आपके खाते से भेजे गए स्पैम/धोखाधड़ी संदेशों के स्क्रीनशॉट"
            ),
            EvidenceItem(
                item="Proof of ownership",
                item_hi="स्वामित्व का प्रमाण",
                mandatory=True,
                example="Old posts, photos proving the account belongs to you",
                example_hi="पुरानी पोस्ट, फ़ोटो जो साबित करती हैं कि खाता आपका है"
            ),
        ],
        important_notes=[
            "Do NOT pay anyone claiming they can recover your account",
            "Never share OTP or verification codes with 'customer support'",
            "Platforms like Facebook/Instagram have free official recovery processes",
            "If financial fraud occurred via your hacked account, report immediately",
        ],
        important_notes_hi=[
            "किसी को भी भुगतान न करें जो दावा करता है कि वे आपका खाता पुनर्प्राप्त कर सकते हैं",
            "OTP या सत्यापन कोड 'कस्टमर सपोर्ट' के साथ कभी साझा न करें",
            "Facebook/Instagram जैसे प्लेटफॉर्म के पास मुफ्त आधिकारिक रिकवरी प्रक्रियाएं हैं",
            "यदि आपके हैक किए गए खाते से वित्तीय धोखाधड़ी हुई है, तो तुरंत रिपोर्ट करें",
        ],
        disclaimers=[
            "Account recovery depends on platform's verification process",
            "This is guidance only - follow platform's official recovery steps",
            "Police complaint may be needed if harassment or financial loss involved",
            "Prevention: Use strong unique passwords and enable 2FA always",
        ],
        disclaimers_hi=[
            "खाता रिकवरी प्लेटफॉर्म की सत्यापन प्रक्रिया पर निर्भर करती है",
            "यह केवल मार्गदर्शन है - प्लेटफॉर्म के आधिकारिक रिकवरी चरणों का पालन करें",
            "उत्पीड़न या वित्तीय नुकसान शामिल होने पर पुलिस शिकायत की आवश्यकता हो सकती है",
            "रोकथाम: हमेशा मजबूत अद्वितीय पासवर्ड का उपयोग करें और 2FA सक्षम करें",
        ],
    ),
    
    # Add more templates for other crime types...
    # (For brevity, showing structure for 2 crime types)
}


def get_sop_template(crime_type: CrimeType) -> SOPTemplate:
    """Get SOP template for specific crime type"""
    return SOP_TEMPLATES.get(crime_type, SOP_TEMPLATES[CrimeType.OTHER])


def generate_timeline_actions(crime_type: CrimeType, language: str = "en") -> Dict:
    """Generate timeline-based action items"""
    template = get_sop_template(crime_type)
    
    return {
        "immediate": [
            {
                "action": a.action if language == "en" else a.action_hi,
                "details": a.details if language == "en" else a.details_hi,
                "priority": a.priority,
                "links": a.links
            }
            for a in template.immediate_actions
        ],
        "within_24_hours": [
            {
                "action": a.action if language == "en" else a.action_hi,
                "details": a.details if language == "en" else a.details_hi,
                "priority": a.priority,
                "links": a.links
            }
            for a in template.within_24h_actions
        ],
        "within_7_days": [
            {
                "action": a.action if language == "en" else a.action_hi,
                "details": a.details if language == "en" else a.details_hi,
                "priority": a.priority,
                "links": a.links
            }
            for a in template.within_7d_actions
        ],
        "ongoing": [
            {
                "action": a.action if language == "en" else a.action_hi,
                "details": a.details if language == "en" else a.details_hi,
                "priority": a.priority,
                "links": a.links
            }
            for a in template.ongoing_actions
        ],
    }


def generate_evidence_checklist(crime_type: CrimeType, language: str = "en") -> List[Dict]:
    """Generate evidence checklist"""
    template = get_sop_template(crime_type)
    
    return [
        {
            "item": e.item if language == "en" else e.item_hi,
            "mandatory": e.mandatory,
            "example": e.example if language == "en" else e.example_hi,
        }
        for e in template.evidence_checklist
    ]
