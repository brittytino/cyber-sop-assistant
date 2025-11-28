"""
Enumeration Types
"""
from enum import Enum


class CrimeType(str, Enum):
    """Cybercrime types"""
    FINANCIAL_FRAUD = "financial_fraud"
    UPI_FRAUD = "upi_fraud"
    CARD_FRAUD = "card_fraud"
    PHISHING = "phishing"
    IDENTITY_THEFT = "identity_theft"
    SOCIAL_MEDIA_HACK = "social_media_hack"
    FAKE_PROFILE = "fake_profile"
    CYBERBULLYING = "cyberbullying"
    HARASSMENT = "harassment"
    SEXTORTION = "sextortion"
    RANSOMWARE = "ransomware"
    MALWARE = "malware"
    OTP_SCAM = "otp_scam"
    SIM_SWAP = "sim_swap"
    KYC_FRAUD = "kyc_fraud"
    LOAN_APP_THREAT = "loan_app_threat"
    JOB_SCAM = "job_scam"
    IMPERSONATION = "impersonation"
    CRYPTO_FRAUD = "crypto_fraud"
    OTHER = "other"


class ComplaintStatus(str, Enum):
    """Complaint status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    HINDI = "hi"
    TAMIL = "ta"
    TELUGU = "te"
    BENGALI = "bn"
    MARATHI = "mr"
    GUJARATI = "gu"
    KANNADA = "kn"


class Platform(str, Enum):
    """Social media platforms"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"
    SNAPCHAT = "snapchat"
    OTHER = "other"


class EvidenceType(str, Enum):
    """Evidence types"""
    SCREENSHOT = "screenshot"
    TRANSACTION_ID = "transaction_id"
    CHAT_LOG = "chat_log"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    BANK_STATEMENT = "bank_statement"
    URL = "url"
    IP_ADDRESS = "ip_address"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"
