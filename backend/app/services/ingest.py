"""
Data Ingestion Script
Populates ChromaDB with Cyber SOPs and PostgreSQL with Police Stations
"""
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

from app.db import SessionLocal, init_db, engine
from app.models import PoliceStation, Document, Resource
from app.services.embedding_client import embed_text
from app.services.rag import get_collection
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split text into chunks"""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
        
    return chunks

def ingest_document(doc: Document):
    """
    Ingest a document into ChromaDB (assuming it's already in SQL)
    """
    try:
        collection = get_collection()
        chunks = chunk_text(doc.content)
        
        if not chunks:
            return
            
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        batch_embeddings = embed_text(chunks)
        
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            documents.append(chunk)
            # embeddings.append(batch_embeddings[i]) # handled by collection.add usually, but we pre-computed
            
            metadatas.append({
                "source": doc.source,
                "title": doc.title or "",
                "section": doc.section or "",
                "url": doc.url or "",
                "doc_id": doc.id,
                "chunk_index": i
            })
            
        collection.add(
            ids=ids,
            embeddings=batch_embeddings,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"Ingested document {doc.id} with {len(chunks)} chunks")
        
    except Exception as e:
        logger.error(f"Error ingesting document {doc.id}: {e}")

def ingest_sops():
    """Ingest standard Cyber SOPs into ChromaDB"""
    logger.info("Ingesting Cyber SOPs...")
    
    # Real content from cybercrime.gov.in and other official sources
    sops = [
        {
            "source": "cybercrime.gov.in",
            "title": "Social Media Fraud Reporting",
            "section": "Reporting",
            "content": "To report social media fraud (fake profiles, hacking, harassment): 1. Take screenshots of the fake profile/posts immediately as evidence. 2. Visit https://cybercrime.gov.in. 3. Select 'Report Other Cyber Crimes' -> 'Social Media Crimes'. 4. Login/Register with mobile number. 5. Fill details: Candidate's details, Incident details (date/time, platform), Suspect details (if any). 6. Upload screenshots. 7. Submit complaint. You will receive an acknowledgement number."
        },
        {
            "source": "cybercrime.gov.in",
            "title": "Financial Fraud (Citizen Financial Cyber Fraud Reporting Management System)",
            "section": "Financial",
            "content": "For immediate financial fraud reporting (UPI fraud, credit card fraud), call **1930** immediately. This connects to the Citizen Financial Cyber Fraud Reporting Management System (CFCFRMS). Speed is critical to freeze the money. Alternatively, file a complaint at cybercrime.gov.in under 'Financial Fraud'. Required details: Bank account number, transaction ID, date of transaction, and evidence (SMS/screenshot)."
        },
        {
            "source": "CERT-In",
            "title": "Ransomware Prevention & Handling",
            "section": "Malware",
            "content": "If infected by Ransomware: 1. Disconnect the infected system from the network/internet immediately to prevent spread. 2. Do NOT pay the ransom; it does not guarantee decryption. 3. Report the incident to clean@cert-in.org.in. 4. Restore data from offline backups if available. 5. Scan systems with updated antivirus. To prevent: Keep OS/software updated, use strong passwords, and maintain offline backups."
        },
        {
            "source": "TAFCOP",
            "title": "Check Registered Mobile Connections",
            "section": "Telecom",
            "content": "To check mobile numbers registered in your name: 1. Visit TAFCOP portal (https://tafcop.sancharsaathi.gov.in). 2. Enter your mobile number and valid Captcha. 3. Enter OTP received. 4. The dashboard will show all numbers linked to your Aadhaar. 5. Select numbers that are not yours or not required and click 'Report' to block them."
        },
        {
            "source": "CEIR",
            "title": "Lost/Stolen Mobile Blocking",
            "section": "Telecom",
            "content": "To block a lost/stolen mobile: 1. File a police complaint (online/offline) and keep the FIR/Ack number. 2. Get a duplicate SIM for your number. 3. Visit https://ceir.sancharsaathi.gov.in -> 'Block Stolen/Lost Mobile'. 4. Upload Police Complaint and Invoice. 5. Enter device IMEI (if known). 6. Submit. The IMEI will be blacklisted across all Indian networks."
        },
        {
            "source": "NCRP",
            "title": "Evidence Requirements",
            "section": "General",
            "content": "Critical evidence for cybercrime reporting: 1. URL of the fake profile/website. 2. Screenshots of chats, profiles, or emails (capture full screen with date/time). 3. Transaction IDs (UTR number) for financial fraud. 4. Email headers (for email spoofing/spam). 5. Saved files/logs if applicable. Do not delete any data properly until investigation is complete."
        }
    ]
    
    db = SessionLocal()
    count = 0
    
    for sop in sops:
        # Check if already exists in DB to avoid duplicates
        existing = db.query(Document).filter(Document.title == sop["title"]).first()
        if existing:
            continue
            
        # Add to SQL DB
        doc = Document(
            source=sop["source"],
            title=sop["title"],
            section=sop["section"],
            content=sop["content"],
            category="SOP"
        )
        db.add(doc)
        db.commit() # Commit to get ID
        db.refresh(doc)
        
        ingest_document(doc)
        count += 1
    
    logger.info(f"Ingested {count} new SOP documents")

def ingest_resources():
    """Ingest standard Resources"""
    logger.info("Ingesting Resources...")
    resources = [
        {"name": "National Cyber Crime Reporting Portal", "url": "https://cybercrime.gov.in", "category": "Reporting"},
        {"name": "NCIIPC (Critical Infra)", "url": "https://nciipc.gov.in", "category": "Security"},
        {"name": "CERT-In", "url": "https://www.cert-in.org.in", "category": "Advisory"},
        {"name": "Sanchar Saathi (CEIR/TAFCOP)", "url": "https://sancharsaathi.gov.in", "category": "Telecom"},
        {"name": "Cyber Swachhta Kendra", "url": "https://www.csk.gov.in", "category": "Tools"},
    ]
    
    db = SessionLocal()
    for res in resources:
        existing = db.query(Resource).filter(Resource.url == res["url"]).first()
        if not existing:
            db.add(Resource(**res))
    db.commit()
    logger.info("Resources ingested")

def ingest_police():
    """Ingest sample Police Stations (expanded list)"""
    logger.info("Ingesting Police Stations...")
    
    stations = [
         {
            "state": "Maharashtra",
            "district": "Pune",
            "city": "Pune",
            "name": "Cyber Crime Police Station, Pune City",
            "address": "Shivajinagar, Pune, Maharashtra 411005",
            "phone": "020-29710097",
            "email": "crimecyber.pune@nic.in",
            "is_cyber_cell": True
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "city": "Pune",
            "name": "Shivajinagar Police Station",
            "address": "Shivajinagar, Pune, Maharashtra 411005",
            "phone": "020-25536263", 
            "is_cyber_cell": False
        },
        {
            "state": "Karnataka",
            "district": "Bangalore",
            "city": "Bengaluru",
            "name": "CEN Crime Police Station",
            "address": "Infantry Road, Bengaluru",
            "phone": "112",
            "is_cyber_cell": True
        }
    ]
    
    db = SessionLocal()
    for st in stations:
        existing = db.query(PoliceStation).filter(PoliceStation.name == st["name"]).first()
        if not existing:
            db.add(PoliceStation(**st))
    db.commit()
    logger.info("Police stations ingested")

if __name__ == "__main__":
    init_db()
    ingest_sops()
    ingest_resources()
    ingest_police()
    logger.info("Ingestion complete!")
