"""
Analytics Repository - Query Log & Statistics Operations
"""
from typing import Dict, Any, Optional, List
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.repositories.base import BaseRepository
from app.models.database import QueryLog
from app.models.enums import CrimeType, Language
from app.core.logging import logger


class AnalyticsRepository(BaseRepository[QueryLog]):
    """Repository for analytics operations"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(QueryLog, session)
    
    async def log_query(
        self,
        request_id: str,
        query: str,
        language: str,
        response_time_ms: float,
        success: bool,
        crime_type: Optional[CrimeType] = None,
        error_message: Optional[str] = None
    ) -> QueryLog:
        """Log a query"""
        return await self.create(
            request_id=request_id,
            query_text=query,
            language=Language(language),
            detected_crime_type=crime_type,
            response_time_ms=response_time_ms,
            success=success,
            error_message=error_message
        )
    
    async def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for last N days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total queries
            total_result = await self.session.execute(
                select(func.count(QueryLog.id)).where(QueryLog.created_at >= cutoff_date)
            )
            total_queries = total_result.scalar() or 0
            
            # Success rate
            success_result = await self.session.execute(
                select(func.count(QueryLog.id)).where(
                    QueryLog.created_at >= cutoff_date,
                    QueryLog.success == True
                )
            )
            successful_queries = success_result.scalar() or 0
            success_rate = (successful_queries / total_queries * 100) if total_queries > 0 else 0
            
            # Average response time
            avg_time_result = await self.session.execute(
                select(func.avg(QueryLog.response_time_ms)).where(
                    QueryLog.created_at >= cutoff_date,
                    QueryLog.success == True
                )
            )
            avg_response_time = avg_time_result.scalar() or 0
            
            # Crime type distribution
            crime_type_result = await self.session.execute(
                select(
                    QueryLog.detected_crime_type,
                    func.count(QueryLog.id).label('count')
                ).where(
                    QueryLog.created_at >= cutoff_date,
                    QueryLog.detected_crime_type.isnot(None)
                ).group_by(QueryLog.detected_crime_type).order_by(desc('count'))
            )
            crime_types = [
                {"type": row[0].value if row[0] else "unknown", "count": row[1]}
                for row in crime_type_result.all()
            ]
            
            # Language distribution
            language_result = await self.session.execute(
                select(
                    QueryLog.language,
                    func.count(QueryLog.id).label('count')
                ).where(
                    QueryLog.created_at >= cutoff_date
                ).group_by(QueryLog.language)
            )
            languages = {
                row[0].value: row[1] for row in language_result.all()
            }
            
            return {
                "total_queries": total_queries,
                "total_complaints_generated": 0,  # From complaint repository
                "most_common_crime_types": crime_types[:10],
                "language_distribution": languages,
                "average_response_time_ms": round(avg_response_time, 2),
                "success_rate": round(success_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Error fetching statistics: {e}", exc_info=True)
            return {
                "total_queries": 0,
                "total_complaints_generated": 0,
                "most_common_crime_types": [],
                "language_distribution": {},
                "average_response_time_ms": 0,
                "success_rate": 0
            }
    
    async def get_recent_queries(self, limit: int = 100) -> List[QueryLog]:
        """Get recent queries"""
        try:
            result = await self.session.execute(
                select(QueryLog).order_by(desc(QueryLog.created_at)).limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching recent queries: {e}")
            return []
