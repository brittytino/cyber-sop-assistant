"""
Classifier Service - Crime Type Classification
Simple keyword-based classifier for crime type detection
"""
from typing import Optional
import re

from app.models.enums import CrimeType
from app.utils.constants import CRIME_KEYWORDS
from app.core.logging import logger


class ClassifierService:
    """Crime type classifier service"""
    
    def __init__(self):
        self.keywords = CRIME_KEYWORDS
    
    async def classify(self, query: str) -> Optional[CrimeType]:
        """
        Classify query into crime type based on keywords
        
        Args:
            query: User query text
            
        Returns:
            Detected crime type or None
        """
        query_lower = query.lower()
        
        # Score each crime type
        scores = {}
        
        for crime_type, keywords in self.keywords.items():
            score = 0
            for keyword in keywords:
                # Check for exact word match
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, query_lower))
                score += matches
            
            if score > 0:
                scores[crime_type] = score
        
        # Return highest scoring crime type
        if scores:
            best_match = max(scores, key=scores.get)
            logger.info(f"Classified query as: {best_match} (score: {scores[best_match]})")
            
            try:
                return CrimeType(best_match)
            except ValueError:
                logger.warning(f"Unknown crime type: {best_match}")
                return None
        
        logger.debug("Could not classify crime type from query")
        return None


# Global instance
classifier_service = ClassifierService()
