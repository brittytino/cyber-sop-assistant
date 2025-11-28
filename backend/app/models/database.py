"""
SQLAlchemy Database Models
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from datetime import datetime

from app.db.base import Base
from app.models.enums import CrimeType, ComplaintStatus, Language


class Complaint(Base):
    """Complaint database model"""
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String(50), unique=True, index=True, nullable=False)
    crime_type = Column(SQLEnum(CrimeType), nullable=False)
    status = Column(SQLEnum(ComplaintStatus), default=ComplaintStatus.DRAFT, nullable=False)
    
    # Incident details
    incident_date = Column(DateTime, nullable=False)
    incident_description = Column(Text, nullable=False)
    amount_lost = Column(Float, nullable=True)
    
    # Victim details
    victim_name = Column(String(100), nullable=False)
    victim_email = Column(String(255), nullable=False)
    victim_phone = Column(String(20), nullable=False)
    victim_address = Column(Text, nullable=False)
    
    # Generated content
    draft_text = Column(Text, nullable=True)
    language = Column(SQLEnum(Language), default=Language.ENGLISH)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "complaint_id": self.complaint_id,
            "crime_type": self.crime_type.value,
            "status": self.status.value,
            "incident_date": self.incident_date.isoformat(),
            "amount_lost": self.amount_lost,
            "victim_name": self.victim_name,
            "language": self.language.value,
            "created_at": self.created_at.isoformat()
        }


class QueryLog(Base):
    """Query log database model"""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Query details
    query_text = Column(Text, nullable=False)
    language = Column(SQLEnum(Language), default=Language.ENGLISH)
    detected_crime_type = Column(SQLEnum(CrimeType), nullable=True)
    
    # Response details
    response_time_ms = Column(Float, nullable=False)
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # RAG details
    retrieved_docs = Column(JSON, nullable=True)
    sources_used = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "query_text": self.query_text,
            "language": self.language.value,
            "detected_crime_type": self.detected_crime_type.value if self.detected_crime_type else None,
            "response_time_ms": self.response_time_ms,
            "success": self.success,
            "created_at": self.created_at.isoformat()
        }


class CacheEntry(Base):
    """Cache entry database model"""
    __tablename__ = "cache_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, index=True, nullable=False)
    cache_value = Column(Text, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    access_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(DateTime, server_default=func.now(), nullable=False)
