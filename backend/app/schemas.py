from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Message Schemas
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(BaseModel):
    content: str

class MessageOut(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Chat Schemas
class ChatCreate(BaseModel):
    title: str = "New Chat"

class ChatOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True

class ChatListItem(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Chat Request/Response

class ChatMessageRequest(BaseModel):
    chat_id: Optional[int] = None
    message: str
    image: Optional[str] = None  # Base64 encoded image
    language: Optional[str] = None # Explicit language code


class SourceReference(BaseModel):
    id: str
    content: str
    source: str
    metadata: dict = {}

class ChatMessageResponse(BaseModel):
    chat_id: int
    message_id: int
    answer: str
    sources: List[SourceReference] = []

# Resource Schemas
class ResourceOut(BaseModel):
    id: int
    name: str
    url: str
    category: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0

    class Config:
        from_attributes = True

class ResourceCreate(BaseModel):
    name: str
    url: str
    category: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0

# Police Station Schemas
class PoliceSearchRequest(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None

class PoliceStationOut(BaseModel):
    id: int
    state: str
    district: Optional[str] = None
    city: Optional[str] = None
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_cyber_cell: bool = False

    class Config:
        from_attributes = True

class PoliceStationCreate(BaseModel):
    state: str
    district: Optional[str] = None
    city: Optional[str] = None
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_cyber_cell: bool = False

# Document Schemas
class DocumentOut(BaseModel):
    id: int
    source: str
    url: Optional[str] = None
    title: Optional[str] = None
    section: Optional[str] = None
    category: Optional[str] = None
    content: str
    chunk_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentCreate(BaseModel):
    source: str
    url: Optional[str] = None
    title: Optional[str] = None
    section: Optional[str] = None
    category: Optional[str] = None
    content: str
    chunk_id: Optional[str] = None

# Admin Schemas
class StatsResponse(BaseModel):
    total_chats: int
    total_messages: int
    total_documents: int
    total_chunks: int
    total_resources: int
    total_police_stations: int

# Auth Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None

