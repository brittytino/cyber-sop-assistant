import sys
import os
import logging
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import engine, Base, init_db
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """
    Standalone script to initialize the database tables.
    Useful if the main app doesn't trigger it or for troubleshooting.
    """
    logger.info(f"Connecting to Database at: {settings.DATABASE_URL}")
    
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
        
        # Create Tables
        logger.info("Creating tables...")
        init_db()
        logger.info("Tables created successfully.")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Existing tables: {tables}")
        
    except Exception as e:
        logger.error(f"Database Error: {e}")
        logger.error("Please ensure PostgreSQL is running and the credentials in .env are correct.")
        
if __name__ == "__main__":
    setup_database()
