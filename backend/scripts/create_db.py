import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "cyber_sop"

def create_database():
    """
    Connect to default 'postgres' database and create 'cyber_sop' if it doesn't exist.
    """
def create_database():
    """
    Connect to default 'postgres' database and create 'cyber_sop' if it doesn't exist.
    """
    try:
        # Connect to default database with known password
        password = "0000" 
        logger.info(f"Connecting to Postgres with password '{password}'...")
        con = psycopg2.connect(dbname='postgres', user=DB_USER, host=DB_HOST, password=password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            logger.info(f"Database '{DB_NAME}' not found. Creating...")
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            logger.info(f"Database '{DB_NAME}' created successfully.")
        else:
            logger.info(f"Database '{DB_NAME}' already exists.")
            
        cur.close()
        con.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        return False

if __name__ == "__main__":
    success = create_database()
    if not success:
        sys.exit(1)
