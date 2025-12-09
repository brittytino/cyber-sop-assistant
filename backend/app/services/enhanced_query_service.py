"""
Enhanced Query Service - Production-Ready Multi-Intent Query Processing
Integrates crime classification, SOP generation, official links, and multi-language support
"""
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from app.core.logging import logger
from app.core.crime_types import (
    CrimeType, 
    classify_crime_type, 
    get_crime_display_name,
    CRIME_TYPE_DATABASE
)
from app.core.sop_templates import (
    generate_timeline_actions,
    generate_evidence_checklist,
    get_sop_template
)
from app.core.official_links import get_relevant_links
from app.services.rag_service import rag_service
from app.services.llm_service import llm_service


class EnhancedQueryService:
    """Enhanced query processing with multi-intent detection and comprehensive response generation"""
    
    def __init__(self):
        self.supported_languages = ["en", "hi", "ta", "te", "bn", "mr", "gu", "kn"]
    
    async def process_query(
        self,
        query: str,
        language: str = "en",
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Process user query with comprehensive multi-intent detection
        
        Args:
            query: User's question/complaint
            language: Language code (en, hi, ta, etc.)
            user_context: Additional context (location, previous queries, etc.)
        
        Returns:
            Comprehensive response with SOP, links, evidence checklist, disclaimer
        """
        start_time = time.time()
        
        try:
            # Step 1: Detect language if not provided
            detected_language = self._detect_language(query) if language == "auto" else language
            
            # Step 2: Classify primary crime type
            primary_crime = classify_crime_type(query, detected_language)
            
            # Step 3: Detect multiple intents (e.g., financial + harassment)
            detected_intents = self._detect_multiple_intents(query, detected_language)
            
            # Step 4: Retrieve relevant SOP documents
            rag_results = await rag_service.retrieve(query, top_k=3)
            
            # Step 5: Generate timeline-based action plan
            action_plan = generate_timeline_actions(primary_crime, detected_language)
            
            # Step 6: Generate evidence checklist
            evidence_checklist = generate_evidence_checklist(primary_crime, detected_language)
            
            # Step 7: Get relevant official links
            official_links = get_relevant_links(primary_crime.value, detected_language)
            
            # Step 8: Generate LLM response with context
            llm_response = await self._generate_llm_response(
                query=query,
                crime_type=primary_crime,
                rag_context=rag_results,
                language=detected_language
            )
            
            # Step 9: Get additional resources
            additional_resources = self._get_additional_resources(
                crime_type=primary_crime,
                detected_intents=detected_intents,
                user_context=user_context
            )
            
            # Step 10: Calculate response time
            response_time = (time.time() - start_time) * 1000  # ms
            
            # Step 11: Build comprehensive response
            response = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "response_time_ms": round(response_time, 2),
                "language": detected_language,
                "detected_crime_type": {
                    "code": primary_crime.value,
                    "display_name": get_crime_display_name(primary_crime, detected_language),
                    "category": CRIME_TYPE_DATABASE[primary_crime].category,
                    "severity": CRIME_TYPE_DATABASE[primary_crime].severity,
                    "typical_loss": CRIME_TYPE_DATABASE[primary_crime].typical_loss_range
                },
                "multiple_intents": detected_intents,
                "llm_response": {
                    "summary": llm_response.get("summary", ""),
                    "detailed_guidance": llm_response.get("detailed_guidance", ""),
                    "immediate_steps": llm_response.get("immediate_steps", [])
                },
                "action_plan": {
                    "immediate": action_plan["immediate"],
                    "within_24_hours": action_plan["within_24_hours"],
                    "within_7_days": action_plan["within_7_days"],
                    "ongoing": action_plan["ongoing"]
                },
                "evidence_checklist": evidence_checklist,
                "official_links": {
                    "primary_portals": [self._link_to_dict(link) for link in official_links["primary_portals"]],
                    "helplines": [self._link_to_dict(link) for link in official_links["helplines"]],
                    "platform_links": [self._link_to_dict(link) for link in official_links.get("platform_links", [])],
                    "advisories": [self._link_to_dict(link) for link in official_links.get("advisories", [])]
                },
                "additional_resources": additional_resources,
                "important_notes": self._get_important_notes(primary_crime, detected_language),
                "disclaimers": self._get_disclaimers(detected_language),
                "next_steps_summary": self._generate_next_steps_summary(action_plan, detected_language)
            }
            
            # Log successful query
            logger.info(f"Query processed successfully: {primary_crime.value} ({response_time:.2f}ms)")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback_message": self._get_fallback_message(language)
            }
    
    def _detect_language(self, query: str) -> str:
        """
        Detect language from query text
        Simple keyword-based detection for Indian languages
        """
        # Hindi keywords
        hindi_keywords = ["मैं", "मेरे", "को", "है", "में", "से", "का", "के", "पर", "यूपीआई", "बैंक"]
        # Tamil keywords
        tamil_keywords = ["நான்", "என்", "இல்", "உள்", "செய்", "வங்கி"]
        # Telugu keywords
        telugu_keywords = ["నేను", "నా", "లో", "కు", "బ్యాంక్"]
        # Bengali keywords
        bengali_keywords = ["আমি", "আমার", "এ", "ব্যাংক"]
        # Marathi keywords
        marathi_keywords = ["मी", "माझे", "मध्ये", "आहे", "बँक"]
        # Gujarati keywords  
        gujarati_keywords = ["હું", "મારા", "માં", "છે", "બેંક"]
        
        query_lower = query.lower()
        
        # Count keyword matches
        if any(keyword in query for keyword in hindi_keywords):
            return "hi"
        elif any(keyword in query for keyword in tamil_keywords):
            return "ta"
        elif any(keyword in query for keyword in telugu_keywords):
            return "te"
        elif any(keyword in query for keyword in bengali_keywords):
            return "bn"
        elif any(keyword in query for keyword in marathi_keywords):
            return "mr"
        elif any(keyword in query for keyword in gujarati_keywords):
            return "gu"
        
        # Default to English
        return "en"
    
    def _detect_multiple_intents(self, query: str, language: str) -> List[Dict]:
        """
        Detect multiple crime types in single query
        Example: "Someone took loan on my aadhar and also blackmailing me"
        -> [loan_fraud, identity_theft, blackmail]
        """
        detected_intents = []
        query_lower = query.lower()
        
        # Check against all crime types
        for crime_type, metadata in CRIME_TYPE_DATABASE.items():
            keywords = metadata.keywords if language == "en" else metadata.keywords_hi
            matches = sum(1 for kw in keywords if kw.lower() in query_lower)
            
            if matches > 0:
                detected_intents.append({
                    "crime_type": crime_type.value,
                    "display_name": get_crime_display_name(crime_type, language),
                    "confidence": min(matches * 20, 100),  # Rough confidence score
                    "keywords_matched": matches
                })
        
        # Sort by confidence
        detected_intents.sort(key=lambda x: x["confidence"], reverse=True)
        
        return detected_intents[:5]  # Return top 5 intents
    
    async def _generate_llm_response(
        self,
        query: str,
        crime_type: CrimeType,
        rag_context: List[Dict],
        language: str
    ) -> Dict:
        """Generate contextual LLM response"""
        
        # Build context from RAG results
        context_text = "\n\n".join([
            f"Document: {doc.get('metadata', {}).get('title', 'Unknown')}\n{doc.get('document', '')}"
            for doc in rag_context[:2]  # Use top 2 documents
        ])
        
        # Build prompt
        crime_display = get_crime_display_name(crime_type, language)
        
        if language == "hi":
            prompt = f"""आप एक साइबर अपराध सहायक हैं। उपयोगकर्ता को {crime_display} के बारे में मदद की आवश्यकता है।

उपयोगकर्ता का सवाल: {query}

संदर्भ जानकारी:
{context_text}

कृपया निम्नलिखित प्रारूप में एक व्यापक प्रतिक्रिया प्रदान करें:

1. सारांश (2-3 वाक्य)
2. विस्तृत मार्गदर्शन
3. तत्काल कदम (3-5 बिंदु)

स्पष्ट, संक्षिप्त और हिंदी में जवाब दें।"""
        else:
            prompt = f"""You are a cybercrime assistance AI. The user needs help with {crime_display}.

User's Question: {query}

Context Information:
{context_text}

Please provide a comprehensive response in the following format:

1. Summary (2-3 sentences)
2. Detailed Guidance
3. Immediate Steps (3-5 points)

Be clear, concise, and empathetic. Focus on actionable advice."""

        try:
            llm_result = await llm_service.generate(prompt, max_tokens=1000)
            
            # Parse LLM response (simple split for now)
            lines = llm_result.strip().split("\n")
            
            return {
                "summary": lines[0] if lines else "",
                "detailed_guidance": "\n".join(lines[1:]) if len(lines) > 1 else "",
                "immediate_steps": [line.strip("- ").strip() for line in lines if line.strip().startswith("-")][:5]
            }
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {
                "summary": f"Detected crime type: {crime_display}. Please follow the action plan below.",
                "detailed_guidance": "See detailed action plan and evidence checklist below.",
                "immediate_steps": []
            }
    
    def _get_additional_resources(
        self,
        crime_type: CrimeType,
        detected_intents: List[Dict],
        user_context: Optional[Dict]
    ) -> Dict:
        """Get additional contextual resources"""
        resources = {
            "emergency_contacts": [],
            "prevention_tips": [],
            "related_advisories": []
        }
        
        # Add emergency contacts based on crime type
        if crime_type in [CrimeType.SEXTORTION, CrimeType.REVENGE_PORN, CrimeType.ONLINE_HARASSMENT]:
            resources["emergency_contacts"].append({
                "name": "Women Helpline",
                "number": "1091",
                "available": "24x7"
            })
        
        if crime_type == CrimeType.CHILD_PORNOGRAPHY:
            resources["emergency_contacts"].append({
                "name": "Child Helpline",
                "number": "1098",
                "available": "24x7"
            })
        
        # Always include cybercrime helpline
        resources["emergency_contacts"].append({
            "name": "National Cybercrime Helpline",
            "number": "1930",
            "available": "24x7"
        })
        
        # Add prevention tips
        resources["prevention_tips"] = self._get_prevention_tips(crime_type)
        
        return resources
    
    def _get_prevention_tips(self, crime_type: CrimeType) -> List[str]:
        """Get crime-specific prevention tips"""
        tips_database = {
            CrimeType.UPI_FRAUD: [
                "Never share UPI PIN or OTP with anyone",
                "Verify recipient details before transferring money",
                "Enable transaction alerts on your mobile",
                "Use official banking apps only",
                "Report suspicious messages to 1930"
            ],
            CrimeType.SOCIAL_MEDIA_HACKING: [
                "Enable two-factor authentication on all accounts",
                "Use strong, unique passwords",
                "Don't click suspicious links in messages",
                "Regularly check login activity",
                "Never share OTP with anyone claiming to be support"
            ],
        }
        
        return tips_database.get(crime_type, [
            "Stay vigilant against suspicious communications",
            "Verify before sharing personal information",
            "Report incidents immediately to 1930",
            "Keep software and apps updated",
            "Use strong passwords and 2FA"
        ])
    
    def _get_important_notes(self, crime_type: CrimeType, language: str) -> List[str]:
        """Get important notes from SOP template"""
        template = get_sop_template(crime_type)
        return template.important_notes if language == "en" else template.important_notes_hi
    
    def _get_disclaimers(self, language: str) -> List[Dict]:
        """Get comprehensive disclaimers"""
        if language == "hi":
            return [
                {
                    "type": "portal_filing",
                    "text": "cybercrime.gov.in पर शिकायत दर्ज करना अधिकांश मामलों में FIR के बराबर है",
                    "emphasis": "high"
                },
                {
                    "type": "ai_limitation",
                    "text": "यह AI सहायक मार्गदर्शन प्रदान करता है, कानूनी सलाह नहीं। सभी चरणों को आधिकारिक स्रोतों से सत्यापित करें।",
                    "emphasis": "high"
                },
                {
                    "type": "privacy",
                    "text": "आपका डेटा सुरक्षित रूप से संग्रहीत है और किसी तीसरे पक्ष के साथ साझा नहीं किया जाता है।",
                    "emphasis": "medium"
                },
                {
                    "type": "no_guarantee",
                    "text": "धन वसूली की गारंटी नहीं है, लेकिन समय पर कार्रवाई से संभावना बढ़ जाती है।",
                    "emphasis": "medium"
                }
            ]
        else:
            return [
                {
                    "type": "portal_filing",
                    "text": "Filing complaint on cybercrime.gov.in is equivalent to FIR in most cases. However, for serious crimes, also visit police station for physical FIR.",
                    "emphasis": "high"
                },
                {
                    "type": "ai_limitation",
                    "text": "This is an AI assistant providing guidance, NOT legal advice. Always verify steps with official sources. For legal representation, consult a qualified lawyer.",
                    "emphasis": "high"
                },
                {
                    "type": "privacy",
                    "text": "Your data is stored securely and encrypted. We do not share information with third parties without your consent.",
                    "emphasis": "medium"
                },
                {
                    "type": "no_guarantee",
                    "text": "Recovery of lost funds is not guaranteed. However, timely action significantly increases chances of resolution.",
                    "emphasis": "medium"
                }
            ]
    
    def _generate_next_steps_summary(self, action_plan: Dict, language: str) -> str:
        """Generate brief next steps summary"""
        immediate_count = len(action_plan.get("immediate", []))
        h24_count = len(action_plan.get("within_24_hours", []))
        
        if language == "hi":
            return f"तत्काल {immediate_count} कदम उठाएं, फिर 24 घंटे के भीतर {h24_count} और कार्य पूरे करें।"
        else:
            return f"Take {immediate_count} immediate actions, then complete {h24_count} more tasks within 24 hours."
    
    def _link_to_dict(self, link) -> Dict:
        """Convert OfficialLink object to dict"""
        return {
            "url": link.url,
            "title": link.title,
            "title_hi": link.title_hi,
            "description": link.description,
            "description_hi": link.description_hi,
            "last_verified": link.last_verified
        }
    
    def _get_fallback_message(self, language: str) -> str:
        """Get fallback error message"""
        if language == "hi":
            return "क्षमा करें, हमें आपके अनुरोध को संसाधित करने में त्रुटि हुई। कृपया 1930 पर कॉल करें या cybercrime.gov.in पर जाएं।"
        else:
            return "Sorry, we encountered an error processing your request. Please call 1930 or visit cybercrime.gov.in for immediate assistance."


# Initialize service instance
enhanced_query_service = EnhancedQueryService()
