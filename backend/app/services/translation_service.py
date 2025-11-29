"""
Translation Service - Multi-language Support
Simple translation mappings for common phrases
"""
from typing import Dict
from app.models.enums import Language
from app.core.logging import logger


class TranslationService:
    """Translation service for multi-language support"""
    
    def __init__(self):
        # Common translations for UI elements
        self.translations = {
            "immediate_actions": {
                Language.ENGLISH: "Immediate Actions",
                Language.HINDI: "तत्काल कार्रवाई",
                Language.TAMIL: "உடனடி நடவடிக்கைகள்",
                Language.TELUGU: "తక్షణ చర్యలు"
            },
            "reporting_steps": {
                Language.ENGLISH: "Reporting Steps",
                Language.HINDI: "रिपोर्टिंग चरण",
                Language.TAMIL: "அறிக்கை படிகள்",
                Language.TELUGU: "నివేదన దశలు"
            },
            "evidence_checklist": {
                Language.ENGLISH: "Evidence Checklist",
                Language.HINDI: "साक्ष्य सूची",
                Language.TAMIL: "ஆதார சரிபார்ப்பு பட்டியல்",
                Language.TELUGU: "సాక్ష్యం జాబితా"
            },
            "call_helpline": {
                Language.ENGLISH: "Call helpline 1930 immediately",
                Language.HINDI: "तुरंत 1930 हेल्पलाइन पर कॉल करें",
                Language.TAMIL: "உடனடியாக 1930 எண்ணை அழைக்கவும்",
                Language.TELUGU: "వెంటనే 1930 హెల్ప్‌లైన్‌కు కాల్ చేయండి"
            },
            "visit_portal": {
                Language.ENGLISH: "Visit https://cybercrime.gov.in",
                Language.HINDI: "https://cybercrime.gov.in पर जाएं",
                Language.TAMIL: "https://cybercrime.gov.in ஐப் பார்வையிடவும்",
                Language.TELUGU: "https://cybercrime.gov.in ను సందర్శించండి"
            }
        }
    
    def translate(self, key: str, language: Language) -> str:
        """
        Get translation for key in specified language
        
        Args:
            key: Translation key
            language: Target language
            
        Returns:
            Translated text or English fallback
        """
        translations = self.translations.get(key, {})
        return translations.get(language, translations.get(Language.ENGLISH, key))
    
    def translate_dict(self, data: Dict, language: Language) -> Dict:
        """
        Translate common keys in dictionary
        
        Args:
            data: Dictionary with translatable keys
            language: Target language
            
        Returns:
            Dictionary with translated keys
        """
        if language == Language.ENGLISH:
            return data
        
        # For now, return as-is
        # In production, integrate with Google Translate API or similar
        logger.debug(f"Translation to {language} not implemented for complex data")
        return data


# Global instance
translation_service = TranslationService()
