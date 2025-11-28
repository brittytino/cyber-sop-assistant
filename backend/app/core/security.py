"""
Security Utilities
Authentication, authorization, and encryption
"""
import hashlib
import hmac
import secrets
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.core.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


def generate_request_id() -> str:
    """Generate a unique request ID"""
    return secrets.token_hex(16)


def hash_string(text: str) -> str:
    """Hash a string using SHA-256"""
    return hashlib.sha256(text.encode()).hexdigest()


def verify_signature(payload: str, signature: str, secret: Optional[str] = None) -> bool:
    """Verify HMAC signature"""
    secret_key = secret or settings.SECRET_KEY
    expected_signature = hmac.new(
        secret_key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)


def create_signature(payload: str, secret: Optional[str] = None) -> str:
    """Create HMAC signature"""
    secret_key = secret or settings.SECRET_KEY
    return hmac.new(
        secret_key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal"""
    # Remove any path separators
    safe_name = filename.replace("/", "_").replace("\\", "_")
    # Remove any non-alphanumeric characters except dots, dashes, underscores
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._-")
    return safe_name[:255]  # Limit length


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Sanitize user input"""
    # Remove null bytes
    text = text.replace("\x00", "")
    # Limit length
    text = text[:max_length]
    # Strip leading/trailing whitespace
    text = text.strip()
    return text
