"""
Authentication Endpoints
OTP-based authentication for automated complaint filing
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime

from app.services.auth_service import auth_service
from app.models.user import (
    PhoneOTPRequest, EmailOTPRequest, VerifyOTPRequest,
    UserRegistration, UserLogin, UserProfileUpdate, PasswordSetup,
    OTPResponse, TokenResponse, UserProfile, UserDashboard,
    UserRole, UserStatus
)
from app.core.logging import logger

router = APIRouter()
security = HTTPBearer(auto_error=False)

# In-memory user store (use database in production)
_users_db: dict = {}


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Get current authenticated user from JWT token"""
    if not credentials:
        return None
    
    payload = auth_service.verify_token(credentials.credentials)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if user_id and user_id in _users_db:
        return _users_db[user_id]
    
    return None


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Require authentication - raises 401 if not authenticated"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    payload = auth_service.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_id = payload.get("sub")
    if not user_id or user_id not in _users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return _users_db[user_id]


# ==================== OTP Endpoints ====================

@router.post("/otp/phone", response_model=OTPResponse)
async def request_phone_otp(request: PhoneOTPRequest):
    """
    Request OTP for phone number authentication
    
    - Rate limited to 1 request per 60 seconds
    - OTP expires in 5 minutes
    - Maximum 3 verification attempts
    """
    logger.info(f"OTP requested for phone: {request.phone[:4]}****")
    return await auth_service.send_phone_otp(request)


@router.post("/otp/email", response_model=OTPResponse)
async def request_email_otp(request: EmailOTPRequest):
    """
    Request OTP for email authentication
    
    - Rate limited to 1 request per 60 seconds
    - OTP expires in 5 minutes
    """
    logger.info(f"OTP requested for email: {request.email[:4]}****")
    return await auth_service.send_email_otp(request)


@router.post("/otp/verify")
async def verify_otp(request: VerifyOTPRequest):
    """
    Verify OTP and authenticate user
    
    Returns JWT tokens on success
    """
    success, message = await auth_service.verify_otp(request)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Check if user exists
    identifier = request.identifier
    existing_user = None
    for user_id, user in _users_db.items():
        if user.get('phone') == identifier or user.get('email') == identifier:
            existing_user = user
            break
    
    if existing_user:
        # Existing user - return tokens
        tokens = auth_service.create_tokens(
            existing_user['user_id'],
            UserRole(existing_user.get('role', 'registered'))
        )
        return {
            "success": True,
            "message": "Login successful",
            "is_new_user": False,
            **tokens.model_dump()
        }
    else:
        # New user - create temporary session for registration
        session_token = auth_service.generate_session_id()
        return {
            "success": True,
            "message": "OTP verified. Please complete registration.",
            "is_new_user": True,
            "registration_token": session_token,
            "verified_identifier": identifier
        }


# ==================== Registration & Login ====================

@router.post("/register", response_model=TokenResponse)
async def register_user(registration: UserRegistration):
    """
    Register new user after OTP verification
    
    Required: name, phone (verified via OTP)
    Optional: email, address, ID details
    """
    # Check if phone already registered
    for user in _users_db.values():
        if user.get('phone') == registration.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
    
    # Create user
    user_id = auth_service.generate_user_id()
    user_data = {
        "user_id": user_id,
        "phone": registration.phone,
        "email": registration.email,
        "name": registration.name,
        "address": registration.address,
        "city": registration.city,
        "state": registration.state,
        "pincode": registration.pincode,
        "id_type": registration.id_type,
        "id_number": registration.id_number,  # Encrypt in production
        "role": UserRole.REGISTERED.value,
        "status": UserStatus.ACTIVE.value,
        "has_password": False,
        "email_verified": False,
        "phone_verified": True,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "preferred_language": "en",
        "total_complaints": 0
    }
    
    _users_db[user_id] = user_data
    logger.info(f"New user registered: {user_id}")
    
    return auth_service.create_tokens(user_id, UserRole.REGISTERED)


@router.post("/login")
async def login_user(login: UserLogin):
    """
    Login with phone/email + OTP or password
    
    If use_otp=True, triggers OTP flow
    If use_otp=False, validates password
    """
    identifier = login.identifier
    
    # Find user
    user = None
    for u in _users_db.values():
        if u.get('phone') == identifier or u.get('email') == identifier:
            user = u
            break
    
    if login.use_otp:
        # Trigger OTP flow
        if '@' in identifier:
            otp_response = await auth_service.send_email_otp(
                EmailOTPRequest(email=identifier)
            )
        else:
            otp_response = await auth_service.send_phone_otp(
                PhoneOTPRequest(phone=identifier)
            )
        
        return {
            "requires_otp": True,
            "otp_sent": otp_response.success,
            "message": otp_response.message,
            "expires_in_seconds": otp_response.expires_in_seconds
        }
    else:
        # Password login
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not user.get('has_password') or not user.get('password_hash'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password not set. Please use OTP login."
            )
        
        if not auth_service.verify_password(login.password, user['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        return auth_service.create_tokens(user['user_id'], UserRole(user['role']))


# ==================== Profile Management ====================

@router.get("/profile", response_model=UserProfile)
async def get_profile(user: dict = Depends(require_auth)):
    """Get current user's profile"""
    return UserProfile(
        user_id=user['user_id'],
        phone=user['phone'],
        email=user.get('email'),
        name=user['name'],
        address=user.get('address'),
        city=user.get('city'),
        state=user.get('state'),
        pincode=user.get('pincode'),
        role=UserRole(user['role']),
        status=UserStatus(user['status']),
        has_password=user.get('has_password', False),
        email_verified=user.get('email_verified', False),
        phone_verified=user.get('phone_verified', False),
        created_at=datetime.fromisoformat(user['created_at']),
        updated_at=datetime.fromisoformat(user['updated_at']),
        preferred_language=user.get('preferred_language', 'en'),
        total_complaints=user.get('total_complaints', 0)
    )


@router.patch("/profile", response_model=UserProfile)
async def update_profile(
    updates: UserProfileUpdate,
    user: dict = Depends(require_auth)
):
    """Update user profile"""
    user_id = user['user_id']
    
    if updates.name:
        _users_db[user_id]['name'] = updates.name
    if updates.email:
        _users_db[user_id]['email'] = updates.email
        _users_db[user_id]['email_verified'] = False
    if updates.address:
        _users_db[user_id]['address'] = updates.address
    if updates.city:
        _users_db[user_id]['city'] = updates.city
    if updates.state:
        _users_db[user_id]['state'] = updates.state
    if updates.pincode:
        _users_db[user_id]['pincode'] = updates.pincode
    if updates.preferred_language:
        _users_db[user_id]['preferred_language'] = updates.preferred_language
    
    _users_db[user_id]['updated_at'] = datetime.utcnow().isoformat()
    
    return await get_profile(user=_users_db[user_id])


@router.post("/password/set")
async def set_password(
    password_data: PasswordSetup,
    user: dict = Depends(require_auth)
):
    """Set or update password for account"""
    user_id = user['user_id']
    
    # Validate password strength
    is_valid, message = auth_service.validate_password_strength(password_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Hash and store password
    _users_db[user_id]['password_hash'] = auth_service.hash_password(password_data.password)
    _users_db[user_id]['has_password'] = True
    _users_db[user_id]['updated_at'] = datetime.utcnow().isoformat()
    
    return {"success": True, "message": "Password set successfully"}


# ==================== Session Management ====================

@router.post("/refresh")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Refresh access token using refresh token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required"
        )
    
    payload = auth_service.verify_token(credentials.credentials)
    if not payload or payload.get('type') != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get('sub')
    if not user_id or user_id not in _users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    user = _users_db[user_id]
    return auth_service.create_tokens(user_id, UserRole(user['role']))


@router.post("/logout")
async def logout(user: dict = Depends(require_auth)):
    """Logout and invalidate tokens"""
    # In production, add token to blacklist
    logger.info(f"User logged out: {user['user_id']}")
    return {"success": True, "message": "Logged out successfully"}


# ==================== Anonymous Session ====================

@router.post("/session/anonymous")
async def create_anonymous_session(request: Request):
    """
    Create anonymous session for users who don't want to sign up
    
    Allows full use of chat and complaint drafting without registration
    """
    session_id = auth_service.generate_session_id()
    
    return {
        "session_id": session_id,
        "is_anonymous": True,
        "message": "Anonymous session created. Your data will be deleted after 24 hours.",
        "features_available": [
            "chat_assistance",
            "complaint_drafting",
            "evidence_checklist",
            "emergency_contacts",
            "nearby_stations"
        ],
        "features_requiring_login": [
            "automated_filing",
            "complaint_tracking",
            "save_drafts",
            "notification_alerts"
        ]
    }
