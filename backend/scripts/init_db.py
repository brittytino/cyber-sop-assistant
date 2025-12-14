"""
Initialize the database with sample data
Run this script after setting up the environment
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db import SessionLocal, init_db, engine
from app.models import Resource, PoliceStation, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database and add sample data"""
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if data already exists
        resource_count = db.query(Resource).count()
        police_count = db.query(PoliceStation).count()
        
        if resource_count > 0:
            logger.info(f"Resources already exist ({resource_count} resources)")
        else:
            logger.info("Adding sample resources...")
            resources = [
                Resource(
                    name="National Cyber Crime Reporting Portal (NCRP)",
                    url="https://cybercrime.gov.in",
                    category="Reporting",
                    description="Official portal to report all types of cybercrimes in India",
                    icon="🚨",
                    order=1
                ),
                Resource(
                    name="CEIR - Block Stolen/Lost Mobile",
                    url="https://ceir.gov.in",
                    category="Mobile Security",
                    description="Central Equipment Identity Register - Block lost/stolen mobile devices",
                    icon="📱",
                    order=2
                ),
                Resource(
                    name="Tafcop - Know Your Mobile Connections",
                    url="https://tafcop.dgt.gov.in",
                    category="Mobile Security",
                    description="Check mobile connections registered in your name",
                    icon="📞",
                    order=3
                ),
                Resource(
                    name="CERT-In",
                    url="https://www.cert-in.org.in",
                    category="Security Advisories",
                    description="Indian Computer Emergency Response Team - Security alerts",
                    icon="🛡️",
                    order=4
                ),
                Resource(
                    name="Chakshu - Report Fraud Calls/SMS",
                    url="https://sancharsaathi.gov.in/sfc",
                    category="Reporting",
                    description="Report suspected fraud calls and SMS",
                    icon="☎️",
                    order=5
                ),
                Resource(
                    name="National Helpline - 1930",
                    url="tel:1930",
                    category="Emergency",
                    description="Toll-free helpline for reporting cybercrimes",
                    icon="📞",
                    order=6
                )
            ]
            
            for resource in resources:
                db.add(resource)
            db.commit()
            logger.info(f"Added {len(resources)} resources")
        
        if police_count > 0:
            logger.info(f"Police stations already exist ({police_count} stations)")
        else:
            logger.info("Adding sample police stations...")
            stations = [
                PoliceStation(
                    state="Delhi",
                    district="Central Delhi",
                    city="Delhi",
                    name="Cyber Crime Cell - Delhi Police HQ",
                    address="I.P. Estate, New Delhi - 110002",
                    phone="011-23490000",
                    email="cybercrime@delhipolice.gov.in",
                    is_cyber_cell=True
                ),
                PoliceStation(
                    state="Maharashtra",
                    district="Mumbai City",
                    city="Mumbai",
                    name="Cyber Crime Cell - Mumbai",
                    address="BKC, Mumbai - 400051",
                    phone="022-22027990",
                    email="cybercell.mumbai@mahapolice.gov.in",
                    is_cyber_cell=True
                ),
                PoliceStation(
                    state="Karnataka",
                    district="Bangalore Urban",
                    city="Bengaluru",
                    name="CID Cyber Crime - Bangalore",
                    address="Carlton House, Palace Road, Bangalore - 560001",
                    phone="080-22942825",
                    email="ccb.cybercrime@ksp.gov.in",
                    is_cyber_cell=True
                ),
                PoliceStation(
                    state="Tamil Nadu",
                    district="Chennai",
                    city="Chennai",
                    name="Cyber Crime Cell - Tamil Nadu",
                    address="Police Commissioner Office, Chennai - 600034",
                    phone="044-23452377",
                    email="cybercrime.chennai@tnpolice.gov.in",
                    is_cyber_cell=True
                )
            ]
            
            for station in stations:
                db.add(station)
            db.commit()
            logger.info(f"Added {len(stations)} police stations")
        
        logger.info("✅ Database initialization complete!")
        logger.info("You can now start the backend server")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()
