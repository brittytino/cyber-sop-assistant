"""
Base Repository - Common Database Operations
"""
from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.exc import SQLAlchemyError

from app.db.base import Base
from app.core.logging import logger

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def create(self, **kwargs) -> ModelType:
        """Create a new record"""
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get record by ID"""
        try:
            result = await self.session.execute(
                select(self.model).where(self.model.id == id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching {self.model.__name__} by id: {e}")
            return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        try:
            result = await self.session.execute(
                select(self.model).offset(skip).limit(limit)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all {self.model.__name__}: {e}")
            return []
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update a record"""
        try:
            await self.session.execute(
                update(self.model).where(self.model.id == id).values(**kwargs)
            )
            await self.session.commit()
            return await self.get_by_id(id)
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error updating {self.model.__name__}: {e}")
            raise
    
    async def delete(self, id: int) -> bool:
        """Delete a record"""
        try:
            await self.session.execute(
                delete(self.model).where(self.model.id == id)
            )
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            return False
    
    async def count(self) -> int:
        """Count total records"""
        try:
            result = await self.session.execute(
                select(func.count()).select_from(self.model)
            )
            return result.scalar() or 0
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            return 0
