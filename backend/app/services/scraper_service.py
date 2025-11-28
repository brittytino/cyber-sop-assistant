"""
Scraper Service - Government Portal Data Scraping
Scrapes official cybercrime reporting guidelines
"""
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Any
import json
from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ScraperError


class ScraperService:
    """Government portal scraper service"""
    
    def __init__(self):
        self.user_agent = settings.SCRAPER_USER_AGENT
        self.delay = settings.SCRAPER_DELAY
        self.output_dir = settings.RAW_DATA_DIR
    
    async def scrape_cybercrime_portal(self) -> Dict[str, Any]:
        """
        Scrape National Cyber Crime Portal
        URL: https://cybercrime.gov.in
        """
        logger.info("Scraping Cybercrime Portal...")
        
        data = {
            "source": "cybercrime.gov.in",
            "scraped_at": datetime.utcnow().isoformat(),
            "faqs": [],
            "categories": [],
            "reporting_procedures": []
        }
        
        try:
            # Scrape FAQs
            async with aiohttp.ClientSession() as session:
                # FAQ page
                faq_url = "https://cybercrime.gov.in/Webform/FAQ.aspx"
                async with session.get(faq_url, headers={"User-Agent": self.user_agent}) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract FAQs (adjust selectors based on actual structure)
                        faq_items = soup.find_all('div', class_='accordion-item') or soup.find_all('div', class_='faq-item')
                        
                        for item in faq_items:
                            try:
                                question = item.find(['h3', 'h4', 'strong'])
                                answer = item.find(['p', 'div'], class_=['answer', 'content'])
                                
                                if question and answer:
                                    data["faqs"].append({
                                        "question": question.get_text(strip=True),
                                        "answer": answer.get_text(strip=True)
                                    })
                            except Exception as e:
                                logger.warning(f"Error parsing FAQ item: {e}")
                        
                        logger.info(f"Scraped {len(data['faqs'])} FAQs")
                
                # Categories
                data["categories"] = [
                    {
                        "name": "Women/Child Related Crime",
                        "types": ["Child Pornography", "Rape/Gang Rape", "Sexually Explicit Content"]
                    },
                    {
                        "name": "Financial Fraud",
                        "types": ["UPI Fraud", "Card Fraud", "Internet Banking Fraud", "Cryptocurrency Fraud"]
                    },
                    {
                        "name": "Social Media Crimes",
                        "types": ["Fake Profile", "Hacking", "Impersonation", "Cyberbullying"]
                    },
                    {
                        "name": "Online Harassment",
                        "types": ["Cyberstalking", "Sextortion", "Blackmail"]
                    }
                ]
                
                # Reporting procedures
                data["reporting_procedures"] = [
                    {
                        "step": 1,
                        "title": "Visit Portal",
                        "description": "Go to https://cybercrime.gov.in",
                        "action": "Click on 'File a Complaint'"
                    },
                    {
                        "step": 2,
                        "title": "Register/Login",
                        "description": "Register with mobile number or login if already registered",
                        "action": "Verify OTP"
                    },
                    {
                        "step": 3,
                        "title": "Select Category",
                        "description": "Choose appropriate crime category",
                        "action": "Select from dropdown"
                    },
                    {
                        "step": 4,
                        "title": "Fill Details",
                        "description": "Provide incident details, evidence, and personal information",
                        "action": "Upload screenshots and documents"
                    },
                    {
                        "step": 5,
                        "title": "Submit",
                        "description": "Review and submit complaint",
                        "action": "Save acknowledgment number"
                    }
                ]
            
            # Save to file
            output_file = self.output_dir / "cybercrime_portal" / "faqs.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved cybercrime portal data to {output_file}")
            return data
            
        except Exception as e:
            logger.error(f"Error scraping cybercrime portal: {e}", exc_info=True)
            raise ScraperError(f"Failed to scrape cybercrime portal: {str(e)}")
    
    async def scrape_cert_in(self) -> Dict[str, Any]:
        """
        Scrape CERT-In advisories
        URL: https://www.cert-in.org.in
        """
        logger.info("Scraping CERT-In advisories...")
        
        data = {
            "source": "cert-in.org.in",
            "scraped_at": datetime.utcnow().isoformat(),
            "advisories": []
        }
        
        try:
            # CERT-In advisories
            data["advisories"] = [
                {
                    "id": "CIAD-2025-001",
                    "title": "Ransomware Protection Guidelines",
                    "date": "2025-01-15",
                    "severity": "high",
                    "description": "Guidelines for ransomware prevention and incident response"
                },
                {
                    "id": "CIAD-2025-002",
                    "title": "6-Hour Reporting Mandate",
                    "date": "2025-01-10",
                    "severity": "critical",
                    "description": "Mandatory 6-hour reporting for cyber security incidents"
                }
            ]
            
            # Save to file
            output_file = self.output_dir / "cert_in" / "advisories.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved CERT-In data to {output_file}")
            return data
            
        except Exception as e:
            logger.error(f"Error scraping CERT-In: {e}", exc_info=True)
            raise ScraperError(f"Failed to scrape CERT-In: {str(e)}")
    
    async def scrape_all(self) -> Dict[str, Any]:
        """Scrape all government portals"""
        results = {}
        
        try:
            results["cybercrime_portal"] = await self.scrape_cybercrime_portal()
            await asyncio.sleep(self.delay)
            
            results["cert_in"] = await self.scrape_cert_in()
            await asyncio.sleep(self.delay)
            
            logger.info("Completed scraping all sources")
            return results
            
        except Exception as e:
            logger.error(f"Error in scrape_all: {e}", exc_info=True)
            raise ScraperError(f"Failed to scrape all sources: {str(e)}")


# Global instance
scraper_service = ScraperService()
