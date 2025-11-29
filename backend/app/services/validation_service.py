"""
Validation Service - Input Validation & Sanitization
"""
import re
from typing import Optional
from app.core.logging import logger
from app.core.security import sanitize_input


class ValidationService:
    """Input validation service"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Indian phone number"""
        # Remove spaces and dashes
        phone = re.sub(r'[\s-]', '', phone)
        
        # Check format: +91XXXXXXXXXX or XXXXXXXXXX
        pattern = r'^(\+91)?[6-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_upi_id(upi_id: str) -> bool:
        """Validate UPI ID format"""
        # Format: username@bankname
        pattern = r'^[\w\.\-]+@[\w]+$'
        return bool(re.match(pattern, upi_id))
    
    @staticmethod
    def validate_transaction_id(txn_id: str) -> bool:
        """Validate transaction ID"""
        # Typically 12-16 alphanumeric characters
        if len(txn_id) < 10 or len(txn_id) > 20:
            return False
        return txn_id.isalnum()
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """Sanitize user query"""
        # Remove excessive whitespace
        query = ' '.join(query.split())
        
        # Remove null bytes
        query = query.replace('\x00', '')
        
        # Limit length
        max_length = 2000
        if len(query) > max_length:
            logger.warning(f"Query truncated from {len(query)} to {max_length} chars")
            query = query[:max_length]
        
        return query.strip()
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def extract_phone_numbers(text: str) -> list:
        """Extract phone numbers from text"""
        # Indian phone number patterns
        patterns = [
            r'\+91[\s-]?\d{10}',
            r'\b[6-9]\d{9}\b'
        ]
        
        numbers = []
        for pattern in patterns:
            numbers.extend(re.findall(pattern, text))
        
        return list(set(numbers))  # Remove duplicates
    
    @staticmethod
    def extract_transaction_ids(text: str) -> list:
        """Extract potential transaction IDs from text"""
        # Look for 12-16 character alphanumeric strings
        pattern = r'\b[A-Z0-9]{12,16}\b'
        return re.findall(pattern, text)


# Global instance
validation_service = ValidationService()
