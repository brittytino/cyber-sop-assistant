"""
Authentication Service
Handles OTP-based authentication for cybercrime assistance platform
"""
import secrets
import hashlib
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.core.logging import logger
from app.models.user import (
    UserRole, UserStatus, UserProfile, TokenResponse,
    OTPResponse, PhoneOTPRequest, EmailOTPRequest, VerifyOTPRequest
)


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OTP storage (in production, use Redis)
_otp_store: Dict[str, Dict[str, Any]] = {}

# User session storage (in production, use database)
_user_sessions: Dict[str, Dict[str, Any]] = {}

# JWT settings
JWT_SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
OTP_EXPIRE_SECONDS = 300
OTP_RETRY_DELAY_SECONDS = 60


class AuthService:
    """Authentication service for OTP and password-based auth"""
    
    def __init__(self):
        self.otp_length = 6
        self.max_otp_attempts = 3
        self.lockout_duration_minutes = 15
    
    # ==================== OTP Methods ====================
    
    def generate_otp(self) -> str:
        """Generate a secure 6-digit OTP"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(self.otp_length)])
    
    def _hash_otp(self, otp: str) -> str:
        """Hash OTP for storage"""
        return hashlib.sha256(otp.encode()).hexdigest()
    
    async def send_phone_otp(self, request: PhoneOTPRequest) -> OTPResponse:
        """Send OTP to phone number"""
        phone = self._normalize_phone(request.phone)
        
        # Check if OTP was recently sent (rate limiting)
        if phone in _otp_store:
            stored = _otp_store[phone]
            time_since_last = (datetime.utcnow() - stored['created_at']).seconds
            if time_since_last < OTP_RETRY_DELAY_SECONDS:
                return OTPResponse(
                    success=False,
                    message="Please wait before requesting another OTP",
                    expires_in_seconds=0,
                    retry_after_seconds=OTP_RETRY_DELAY_SECONDS - time_since_last
                )
        
        # Generate and store OTP
        otp = self.generate_otp()
        _otp_store[phone] = {
            'otp_hash': self._hash_otp(otp),
            'created_at': datetime.utcnow(),
            'attempts': 0,
            'type': 'phone'
        }
        
        # In production, integrate with SMS gateway (MSG91, Twilio, etc.)
        # For now, log the OTP (REMOVE IN PRODUCTION)
        logger.info(f"[DEV ONLY] OTP for {phone}: {otp}")
        
        # Simulate SMS sending
        success = await self._send_sms(phone, otp)
        
        return OTPResponse(
            success=success,
            message="OTP sent to your phone number" if success else "Failed to send OTP",
            expires_in_seconds=OTP_EXPIRE_SECONDS
        )
    
    async def send_email_otp(self, request: EmailOTPRequest) -> OTPResponse:
        """Send OTP to email address"""
        email = request.email.lower().strip()
        
        # Check rate limiting
        if email in _otp_store:
            stored = _otp_store[email]
            time_since_last = (datetime.utcnow() - stored['created_at']).seconds
            if time_since_last < OTP_RETRY_DELAY_SECONDS:
                return OTPResponse(
                    success=False,
                    message="Please wait before requesting another OTP",
                    expires_in_seconds=0,
                    retry_after_seconds=OTP_RETRY_DELAY_SECONDS - time_since_last
                )
        
        # Generate and store OTP
        otp = self.generate_otp()
        _otp_store[email] = {
            'otp_hash': self._hash_otp(otp),
            'created_at': datetime.utcnow(),
            'attempts': 0,
            'type': 'email'
        }
        
        # In production, integrate with email service
        logger.info(f"[DEV ONLY] OTP for {email}: {otp}")
        
        success = await self._send_email(email, otp)
        
        return OTPResponse(
            success=success,
            message="OTP sent to your email address" if success else "Failed to send OTP",
            expires_in_seconds=OTP_EXPIRE_SECONDS
        )
    
    async def verify_otp(self, request: VerifyOTPRequest) -> Tuple[bool, str]:
        """Verify OTP and return success status with message"""
        identifier = self._normalize_identifier(request.identifier)
        
        if identifier not in _otp_store:
            return False, "No OTP found. Please request a new one."
        
        stored = _otp_store[identifier]
        
        # Check expiry
        if (datetime.utcnow() - stored['created_at']).seconds > OTP_EXPIRE_SECONDS:
            del _otp_store[identifier]
            return False, "OTP has expired. Please request a new one."
        
        # Check attempts
        if stored['attempts'] >= self.max_otp_attempts:
            del _otp_store[identifier]
            return False, "Too many failed attempts. Please request a new OTP."
        
        # Verify OTP
        if self._hash_otp(request.otp) != stored['otp_hash']:
            stored['attempts'] += 1
            remaining = self.max_otp_attempts - stored['attempts']
            return False, f"Invalid OTP. {remaining} attempts remaining."
        
        # Success - clear OTP
        del _otp_store[identifier]
        return True, "OTP verified successfully"
    
    # ==================== Token Methods ====================
    
    def create_access_token(self, user_id: str, data: Dict[str, Any] = None) -> str:
        """Create JWT access token"""
        to_encode = {
            "sub": user_id,
            "type": "access",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        if data:
            to_encode.update(data)
        
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        to_encode = {
            "sub": user_id,
            "type": "refresh",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            return None
    
    def create_tokens(self, user_id: str, role: UserRole = UserRole.REGISTERED) -> TokenResponse:
        """Create both access and refresh tokens"""
        access_token = self.create_access_token(user_id, {"role": role.value})
        refresh_token = self.create_refresh_token(user_id)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token,
            user_id=user_id
        )
    
    # ==================== Password Methods ====================
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password meets security requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        return True, "Password meets requirements"
    
    # ==================== Helper Methods ====================
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number to standard format"""
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        if cleaned.startswith('+91'):
            return cleaned
        if len(cleaned) == 10:
            return f'+91{cleaned}'
        return cleaned
    
    def _normalize_identifier(self, identifier: str) -> str:
        """Normalize identifier (phone or email)"""
        if '@' in identifier:
            return identifier.lower().strip()
        return self._normalize_phone(identifier)
    
    async def _send_sms(self, phone: str, otp: str) -> bool:
        """Send SMS via gateway (implement with MSG91/Twilio)"""
        # TODO: Integrate with SMS gateway
        # For development, always return True
        logger.info(f"SMS OTP sent to {phone}")
        return True
    
    async def _send_email(self, email: str, otp: str) -> bool:
        """Send email OTP (implement with SMTP/SendGrid)"""
        # TODO: Integrate with email service
        logger.info(f"Email OTP sent to {email}")
        return True
    
    def generate_user_id(self) -> str:
        """Generate unique user ID"""
        return f"USR-{secrets.token_hex(8).upper()}"
    
    def generate_session_id(self) -> str:
        """Generate session ID for anonymous users"""
        return f"SES-{secrets.token_hex(12)}"


# Singleton instance
auth_service = AuthService()
