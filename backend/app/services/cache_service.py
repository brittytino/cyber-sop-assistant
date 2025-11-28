"""
Cache Service - Response Caching
Disk-based caching for LLM responses
"""
from diskcache import Cache
from typing import Optional, Any
import hashlib
import json
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.logging import logger


class CacheService:
    """Disk cache service"""
    
    def __init__(self):
        self.cache_enabled = settings.CACHE_ENABLED
        self.cache_path = settings.CACHE_PATH
        self.ttl = settings.CACHE_TTL
        self.cache: Optional[Cache] = None
        
        if self.cache_enabled:
            self.cache = Cache(self.cache_path)
            logger.info(f"Cache initialized at {self.cache_path}")
    
    def _generate_key(self, query: str, language: str) -> str:
        """Generate cache key from query and language"""
        content = f"{query}:{language}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, query: str, language: str) -> Optional[Any]:
        """Get cached response"""
        if not self.cache_enabled or not self.cache:
            return None
        
        try:
            key = self._generate_key(query, language)
            cached_value = self.cache.get(key)
            
            if cached_value:
                logger.debug(f"Cache HIT for query: {query[:50]}...")
                return cached_value
            else:
                logger.debug(f"Cache MISS for query: {query[:50]}...")
                return None
                
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, query: str, language: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set cached response"""
        if not self.cache_enabled or not self.cache:
            return False
        
        try:
            key = self._generate_key(query, language)
            expire_time = ttl or self.ttl
            self.cache.set(key, value, expire=expire_time)
            logger.debug(f"Cached response for query: {query[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        if not self.cache_enabled or not self.cache:
            return False
        
        try:
            self.cache.clear()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.cache_enabled or not self.cache:
            return {"enabled": False}
        
        try:
            return {
                "enabled": True,
                "size": len(self.cache),
                "volume": self.cache.volume(),
                "hits": getattr(self.cache, 'hits', 0),
                "misses": getattr(self.cache, 'misses', 0)
            }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"enabled": True, "error": str(e)}


# Global instance
cache_service = CacheService()
