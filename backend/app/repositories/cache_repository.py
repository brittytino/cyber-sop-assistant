"""
Cache Repository - Database-backed Cache Operations
"""
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.repositories.base import BaseRepository
from app.models.database import CacheEntry
from app.core.logging import logger


class CacheRepository(BaseRepository[CacheEntry]):
    """Repository for database cache operations"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(CacheEntry, session)
    
    async def get_cached(self, cache_key: str) -> Optional[str]:
        """Get cached value if not expired"""
        try:
            result = await self.session.execute(
                select(CacheEntry).where(
                    CacheEntry.cache_key == cache_key,
                    CacheEntry.expires_at > datetime.utcnow()
                )
            )
            entry = result.scalar_one_or_none()
            
            if entry:
                # Update access stats
                entry.access_count += 1
                entry.last_accessed = datetime.utcnow()
                await self.session.commit()
                return entry.cache_value
            
            return None
        except Exception as e:
            logger.error(f"Error getting cached value: {e}")
            return None
    
    async def set_cached(
        self,
        cache_key: str,
        cache_value: str,
        ttl_seconds: int = 3600
    ) -> bool:
        """Set cached value"""
        try:
            expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
            
            # Check if exists
            existing = await self.session.execute(
                select(CacheEntry).where(CacheEntry.cache_key == cache_key)
            )
            entry = existing.scalar_one_or_none()
            
            if entry:
                # Update existing
                entry.cache_value = cache_value
                entry.expires_at = expires_at
                entry.last_accessed = datetime.utcnow()
            else:
                # Create new
                entry = CacheEntry(
                    cache_key=cache_key,
                    cache_value=cache_value,
                    expires_at=expires_at
                )
                self.session.add(entry)
            
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error setting cached value: {e}")
            return False
    
    async def cleanup_expired(self) -> int:
        """Remove expired cache entries"""
        try:
            result = await self.session.execute(
                delete(CacheEntry).where(CacheEntry.expires_at < datetime.utcnow())
            )
            await self.session.commit()
            return result.rowcount
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error cleaning up cache: {e}")
            return 0
