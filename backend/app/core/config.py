"""
Application Configuration
Loads environment variables and provides centralized settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Project Info
    PROJECT_NAME: str = "Cyber SOP Assistant"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "LLM-powered cybercrime reporting guidance system"
    
    # Server Config
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Security
    SECRET_KEY: str = Field(default="CHANGE_THIS_IN_PRODUCTION", env="SECRET_KEY")
    API_KEY: Optional[str] = Field(default=None, env="API_KEY")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./data/cyber_sop.db",
        env="DATABASE_URL"
    )
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    OLLAMA_MODEL: str = Field(default="mistral:7b-instruct", env="OLLAMA_MODEL")
    OLLAMA_TIMEOUT: int = Field(default=120, env="OLLAMA_TIMEOUT")
    
    # ChromaDB Configuration
    CHROMA_DB_PATH: str = Field(default="./data/vectorstore", env="CHROMA_DB_PATH")
    CHROMA_COLLECTION_NAME: str = Field(default="sop_documents", env="CHROMA_COLLECTION_NAME")
    
    # Embedding Model
    EMBEDDING_MODEL_PATH: str = Field(
        default="./models/embeddings/all-MiniLM-L6-v2",
        env="EMBEDDING_MODEL_PATH"
    )
    EMBEDDING_MODEL_NAME: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        env="EMBEDDING_MODEL_NAME"
    )
    
    # RAG Configuration
    RAG_TOP_K: int = Field(default=5, env="RAG_TOP_K")
    RAG_SCORE_THRESHOLD: float = Field(default=0.5, env="RAG_SCORE_THRESHOLD")
    
    # LLM Generation Parameters
    LLM_TEMPERATURE: float = Field(default=0.1, env="LLM_TEMPERATURE")
    LLM_MAX_TOKENS: int = Field(default=2048, env="LLM_MAX_TOKENS")
    LLM_TOP_P: float = Field(default=0.9, env="LLM_TOP_P")
    LLM_TOP_K: int = Field(default=40, env="LLM_TOP_K")
    LLM_REPEAT_PENALTY: float = Field(default=1.1, env="LLM_REPEAT_PENALTY")
    
    # Cache Configuration
    CACHE_ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    CACHE_PATH: str = Field(default="./data/cache", env="CACHE_PATH")
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="./data/logs/app.log", env="LOG_FILE")
    
    # Data Paths
    DATA_DIR: Path = Field(default=Path("./data"), env="DATA_DIR")
    RAW_DATA_DIR: Path = Field(default=Path("./data/raw"), env="RAW_DATA_DIR")
    PROCESSED_DATA_DIR: Path = Field(default=Path("./data/processed"), env="PROCESSED_DATA_DIR")
    MODELS_DIR: Path = Field(default=Path("./models"), env="MODELS_DIR")
    
    # Scraper Configuration
    SCRAPER_USER_AGENT: str = Field(
        default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        env="SCRAPER_USER_AGENT"
    )
    SCRAPER_DELAY: int = Field(default=2, env="SCRAPER_DELAY")
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = Field(
        default=["en", "hi", "ta", "te", "bn", "mr", "gu", "kn"],
        env="SUPPORTED_LANGUAGES"
    )
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in .env


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
Path(settings.CACHE_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
