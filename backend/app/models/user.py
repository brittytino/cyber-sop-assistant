"""
User and Authentication Models
"""
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
import re


class AuthProvider(str, Enum):
    """Authentication provider types"""
    EMAIL = "email"
    PHONE = "phone"
    OTP = "otp"


class UserRole(str, Enum):
    """User role types"""
    ANONYMOUS = "anonymous"
    REGISTERED = "registered"
    VERIFIED = "verified"
    ADMIN = "admin"


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


# Request Schemas
class PhoneOTPRequest(BaseModel):
    """Request OTP for phone number"""
    phone: str = Field(..., min_length=10, max_length=15, description="Indian phone number")
    country_code: str = Field(default="+91", description="Country code")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate Indian phone number format"""
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^(\+91)?[6-9]\d{9}$', cleaned):
            raise ValueError("Invalid Indian phone number format")
        return cleaned


class EmailOTPRequest(BaseModel):
    """Request OTP for email"""
    email: str = Field(..., description="Email address")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v.lower()):
            raise ValueError("Invalid email format")
        return v.lower().strip()


class VerifyOTPRequest(BaseModel):
    """Verify OTP request"""
    identifier: str = Field(..., description="Phone or email")
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit OTP")
    
    @field_validator("otp")
    @classmethod
    def validate_otp(cls, v: str) -> str:
        """Validate OTP format"""
        if not v.isdigit() or len(v) != 6:
            raise ValueError("OTP must be 6 digits")
        return v


class UserRegistration(BaseModel):
    """User registration schema"""
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = Field(None)
    name: str = Field(..., min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, min_length=6, max_length=6)
    id_type: Optional[str] = Field(None, description="Aadhaar, PAN, Voter ID, etc.")
    id_number: Optional[str] = Field(None, max_length=50, description="ID number (encrypted)")
    
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: Optional[str]) -> Optional[str]:
        """Validate Indian pincode"""
        if v is not None and not re.match(r'^[1-9][0-9]{5}$', v):
            raise ValueError("Invalid Indian pincode format")
        return v


class UserLogin(BaseModel):
    """User login schema"""
    identifier: str = Field(..., description="Phone number or email")
    password: Optional[str] = Field(None, min_length=8, description="Password (optional)")
    use_otp: bool = Field(default=True, description="Use OTP for login")


class PasswordSetup(BaseModel):
    """Set up password for account"""
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Ensure passwords match"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Passwords do not match")
        return v


class UserProfileUpdate(BaseModel):
    """Update user profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, min_length=6, max_length=6)
    preferred_language: Optional[str] = Field(None, pattern=r'^(en|hi|ta|te|bn|mr|gu|kn)$')


# Response Schemas
class OTPResponse(BaseModel):
    """OTP send response"""
    success: bool
    message: str
    expires_in_seconds: int = 300
    retry_after_seconds: Optional[int] = None


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    user_id: str


class UserProfile(BaseModel):
    """User profile response"""
    user_id: str
    phone: str
    email: Optional[str] = None
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    role: UserRole
    status: UserStatus
    has_password: bool
    email_verified: bool
    phone_verified: bool
    created_at: datetime
    updated_at: datetime
    preferred_language: str = "en"
    total_complaints: int = 0


class UserComplaintSummary(BaseModel):
    """Summary of user's complaints"""
    complaint_id: str
    crime_type: str
    status: str
    portal_reference: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserDashboard(BaseModel):
    """User dashboard data"""
    profile: UserProfile
    recent_complaints: List[UserComplaintSummary]
    pending_actions: List[str]
    notifications: List[dict]
