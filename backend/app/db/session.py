"""
Database Session Management
Optional async SQLite database for analytics
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings
from app.db.base import Base
from app.core.logging import logger

try:
    # Convert SQLite URL to async format
    database_url = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

    # Create async engine
    engine = create_async_engine(
        database_url,
        echo=settings.DEBUG,
        future=True,
        poolclass=NullPool if "sqlite" in database_url else None
    )

    # Create async session factory
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    
    DB_AVAILABLE = True
    logger.info("Database engine created successfully")
    
except Exception as e:
    logger.warning(f"Database engine creation failed: {e}")
    logger.warning("App will work without database (analytics disabled)")
    engine = None
    AsyncSessionLocal = None
    DB_AVAILABLE = False


async def get_db():
    """Get database session (optional)"""
    if not DB_AVAILABLE or AsyncSessionLocal is None:
        logger.warning("Database not available - skipping database dependency")
        # Yield None for routes that optionally use DB
        yield None
    else:
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()


async def init_db():
    """Initialize database (optional)"""
    if not DB_AVAILABLE or engine is None:
        logger.warning("Skipping database initialization - DB not available")
        return
        
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Don't raise - app can work without DB
