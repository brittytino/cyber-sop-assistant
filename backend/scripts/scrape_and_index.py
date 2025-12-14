import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import logging
import time
import urllib3

# Add backend directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal
from app.models import Document
from app.services.ingest import ingest_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URLS_TO_SCRAPE = [
    {
        "url": "https://cybercrime.gov.in/Web/CyberCrimeUnit.aspx",
        "source": "NCRP",
        "category": "Reporting"
    },
    {
        "url": "https://cybercrime.gov.in/Web/CyberCrimeUnit.aspx", # Simulating Hindi version scrape if available
        "source": "NCRP (Hindi Setup)", 
        "category": "Reporting",
        "lang": "hi" # We'd rely on langdetect or manual tagging
    },
    {
        "url": "https://www.cert-in.org.in/",
        "source": "CERT-In",
        "category": "Advisory"
    },
    {
        "url": "https://www.ceir.gov.in/Home/index.jsp",
        "source": "CEIR",
        "category": "Lost Phone"
    },
    {
        "url": "https://tafcop.sancharsaathi.gov.in/telecomUser/",
        "source": "TAFCOP",
        "category": "Fraud"
    }
]

def scrape_url(url: str) -> str:
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return ""

def main():
    db = SessionLocal()
    try:
        for item in URLS_TO_SCRAPE:
            logger.info(f"Scraping {item['url']}...")
            content = scrape_url(item['url'])
            
            if content:
                logger.info(f"Extracted {len(content)} chars. Indexing...")
                
                # Check for existing
                existing = db.query(Document).filter(Document.source == item['source']).first()
                if existing:
                    logger.info("Updating existing document...")
                    # In real app, we might update. Here we skip or update content.
                    existing.content = content
                    db.commit()
                    # Re-ingest chunks? Skipping for speed in this demo
                    continue

                doc = Document(
                    source=item['source'],
                    url=item['url'],
                    category=item['category'],
                    content=content,
                    title=f"Scraped content from {item['source']}"
                )
                db.add(doc)
                db.commit()
                db.refresh(doc)
                
                ingest_document(doc)
                
            else:
                logger.warning(f"No content found for {item['url']}")
            
            time.sleep(1) 
            
    except Exception as e:
        logger.error(f"Global error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
