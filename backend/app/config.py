from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List
import json

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Database - Using PostgreSQL
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/cyber_sop"
    
    # Chroma Vector Store
    CHROMA_DIR: str = str(BASE_DIR.parent / "data" / "chroma_store")
    
    # Embedding Model (local sentence-transformers)
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    
    # LLM Configuration (Ollama local)
    LLM_ENDPOINT: str = "http://localhost:11434"
    LLM_MODEL: str = "mistral:instruct"
    
    # Groq Configuration for Transcription
    GROQ_API_KEY: str

    # OpenRouter Configuration (Multi-language fallback)
    OPENROUTER_API_KEY: str
    OPENROUTER_MODELS: str = '["google/gemma-3-27b-it:free", "meta-llama/llama-3.3-70b-instruct:free", "mistralai/mistral-small-3.1-24b-instruct:free", "google/gemini-2.0-flash-exp:free", "mistralai/mistral-7b-instruct:free", "meta-llama/llama-3.2-3b-instruct:free"]'

    @property
    def openrouter_models_list(self) -> List[str]:
        return json.loads(self.OPENROUTER_MODELS)

    # CORS Origins
    CORS_ORIGINS: str = '["http://localhost:5173"]'
    
    @property
    def cors_origins_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = 'utf-8'

settings = Settings()
