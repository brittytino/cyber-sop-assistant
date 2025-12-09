"""
Multilingual LLM Service - Uses Local Ollama for All Operations
Handles RAG-based SOP generation with direct multilingual support
"""
import json
from typing import Dict, List, Optional, Any
from app.core.config import settings
from app.core.logging import logger
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service


class MultilingualLLMService:
    """
    Enhanced LLM service with multilingual support using local Ollama only
    - Uses local Ollama for both content generation and translation
    - Fast, privacy-focused, no external API calls
    """

    # Language names for better Ollama prompts
    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi (हिंदी)",
        "ta": "Tamil (தமிழ்)",
        "te": "Telugu (తెలుగు)",
        "bn": "Bengali (বাংলা)",
        "mr": "Marathi (मराठी)",
        "gu": "Gujarati (ગુજરાતી)",
        "kn": "Kannada (ಕನ್ನಡ)"
    }

    def __init__(self):
        self.local_llm = llm_service
        self.rag = rag_service

    async def generate_sop_response(
        self,
        query: str,
        language: str = "en",
        category: Optional[str] = None,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Generate SOP response with multilingual support using local Ollama
        
        Args:
            query: User's question
            language: Target language code (en, hi, ta, etc.)
            category: Optional crime category filter
            use_rag: Whether to use RAG for context retrieval
            
        Returns:
            Structured SOP response in target language
        """
        try:
            # Step 1: Retrieve relevant documents using RAG
            context_docs = []
            if use_rag:
                try:
                    search_results = await self.rag.search_documents(
                        query=query,
                        category=category,
                        limit=settings.RAG_TOP_K
                    )
                    context_docs = search_results.get("results", [])
                    logger.info(f"Retrieved {len(context_docs)} documents from RAG")
                except Exception as e:
                    logger.warning(f"RAG search failed: {e}, proceeding without context")

            # Step 2: Generate response directly in target language using Ollama
            response = await self._generate_multilingual_sop(
                query=query,
                language=language,
                context_docs=context_docs
            )
            
            return response

        except Exception as e:
            logger.error(f"Error in multilingual SOP generation: {e}", exc_info=True)
            return self._get_fallback_response(language)

    async def _generate_multilingual_sop(
        self,
        query: str,
        language: str,
        context_docs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate SOP directly in target language using local Ollama
        
        Args:
            query: User's question
            language: Target language code
            context_docs: Retrieved context from RAG
            
        Returns:
            SOP response in target language
        """
        # Build context from RAG documents
        context_text = ""
        if context_docs:
            context_text = "\n\n".join([
                f"Document {i+1}:\n{doc.get('content', '')}"
                for i, doc in enumerate(context_docs[:3])
            ])

        # Get language name
        lang_name = self.LANGUAGE_NAMES.get(language, "English")
        
        # Create multilingual prompt for Ollama
        prompt = f"""You are a cybercrime assistance expert. Respond in {lang_name}.

USER QUERY: {query}

CONTEXT FROM KNOWLEDGE BASE:
{context_text if context_text else "No specific context available."}

INSTRUCTIONS:
1. Analyze the user's cybercrime issue
2. Provide immediate actions they should take
3. List step-by-step reporting procedure
4. Include evidence collection checklist
5. Suggest relevant official platforms

Respond ONLY in {lang_name}. Be clear, actionable, and empathetic.

FORMAT YOUR RESPONSE AS JSON:
{{
    "immediate_actions": ["action 1", "action 2", "action 3"],
    "reporting_steps": ["step 1", "step 2", "step 3"],
    "evidence_checklist": ["item 1", "item 2", "item 3"],
    "official_links": [
        {{"name": "Platform Name", "url": "URL", "category": "reporting/help"}}
    ],
    "summary": "Brief summary of the situation and next steps"
}}"""

        try:
            # Call local Ollama
            response_text = await self.local_llm.generate_completion(
                prompt=prompt,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )

            # Try to parse JSON response
            try:
                # Extract JSON from response (Ollama might include extra text)
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                    parsed_response = json.loads(json_text)
                else:
                    raise ValueError("No JSON found in response")
                
                return parsed_response
                
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                # Return structured fallback
                return {
                    "immediate_actions": self._extract_list_items(response_text, "immediate"),
                    "reporting_steps": self._extract_list_items(response_text, "step"),
                    "evidence_checklist": self._extract_list_items(response_text, "evidence"),
                    "official_links": [],
                    "summary": response_text[:500] if len(response_text) > 500 else response_text
                }

        except Exception as e:
            logger.error(f"Error generating multilingual SOP: {e}", exc_info=True)
            return self._get_fallback_response(language)

    async def chat_with_language_awareness(
        self,
        message: str,
        language: str = "en",
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Have a conversational chat in the specified language
        
        Args:
            message: User's message
            language: Target language code
            conversation_history: Previous conversation context
            
        Returns:
            Response in target language
        """
        try:
            lang_name = self.LANGUAGE_NAMES.get(language, "English")
            
            # Build conversation context
            context = ""
            if conversation_history:
                context = "\n".join([
                    f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                    for msg in conversation_history[-5:]  # Last 5 messages
                ])

            prompt = f"""You are a helpful cybercrime assistant. Respond in {lang_name}.

{context}

USER: {message}

ASSISTANT (in {lang_name}):"""

            response = await self.local_llm.generate_completion(
                prompt=prompt,
                temperature=0.8,  # More creative for chat
                max_tokens=256
            )

            return response.strip()

        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)
            return self._get_fallback_message(language)

    def _extract_list_items(self, text: str, keyword: str) -> List[str]:
        """Extract list items from unstructured text"""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered or bulleted lists
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering/bullets
                cleaned = line.lstrip('0123456789.-•) ').strip()
                if cleaned and keyword.lower() in text.lower():
                    items.append(cleaned)
        
        return items[:10]  # Limit to 10 items

    def _get_fallback_response(self, language: str) -> Dict[str, Any]:
        """Get fallback response when generation fails"""
        fallbacks = {
            "en": {
                "immediate_actions": [
                    "Document all evidence (screenshots, messages, transaction details)",
                    "Stop all communication with the perpetrator",
                    "Change passwords for affected accounts"
                ],
                "reporting_steps": [
                    "Visit cybercrime.gov.in to file a complaint",
                    "Contact your bank if financial fraud occurred",
                    "Preserve all digital evidence"
                ],
                "evidence_checklist": [
                    "Screenshots of fraudulent messages or posts",
                    "Transaction IDs and bank statements",
                    "Email headers and sender information"
                ],
                "official_links": [
                    {"name": "National Cyber Crime Portal", "url": "https://cybercrime.gov.in", "category": "reporting"}
                ],
                "summary": "I apologize, but I'm having trouble generating a detailed response. Please file a complaint at cybercrime.gov.in for immediate assistance."
            },
            "hi": {
                "immediate_actions": [
                    "सभी साक्ष्यों को सुरक्षित करें (स्क्रीनशॉट, संदेश, लेनदेन विवरण)",
                    "अपराधी के साथ सभी संचार बंद करें",
                    "प्रभावित खातों के पासवर्ड बदलें"
                ],
                "reporting_steps": [
                    "शिकायत दर्ज करने के लिए cybercrime.gov.in पर जाएं",
                    "यदि वित्तीय धोखाधड़ी हुई है तो अपने बैंक से संपर्क करें",
                    "सभी डिजिटल साक्ष्य सुरक्षित रखें"
                ],
                "evidence_checklist": [
                    "धोखाधड़ी संदेशों या पोस्ट के स्क्रीनशॉट",
                    "लेनदेन आईडी और बैंक स्टेटमेंट",
                    "ईमेल हेडर और भेजने वाले की जानकारी"
                ],
                "official_links": [
                    {"name": "राष्ट्रीय साइबर अपराध पोर्टल", "url": "https://cybercrime.gov.in", "category": "reporting"}
                ],
                "summary": "मुझे खेद है, लेकिन मुझे विस्तृत प्रतिक्रिया उत्पन्न करने में समस्या हो रही है। तत्काल सहायता के लिए कृपया cybercrime.gov.in पर शिकायत दर्ज करें।"
            }
        }
        
        return fallbacks.get(language, fallbacks["en"])

    def _get_fallback_message(self, language: str) -> str:
        """Get fallback chat message"""
        messages = {
            "en": "I apologize, but I'm having trouble processing your request. Please try again or visit cybercrime.gov.in for assistance.",
            "hi": "मुझे खेद है, लेकिन मुझे आपके अनुरोध को संसाधित करने में समस्या हो रही है। कृपया पुनः प्रयास करें या सहायता के लिए cybercrime.gov.in पर जाएं।",
            "ta": "மன்னிக்கவும், உங்கள் கோரிக்கையை செயல்படுத்துவதில் சிக்கல் உள்ளது. மீண்டும் முயற்சிக்கவும் அல்லது உதவிக்கு cybercrime.gov.in ஐ பார்வையிடவும்.",
            "te": "క్షమించండి, మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో నాకు ఇబ్బంది ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి లేదా సహాయం కోసం cybercrime.gov.in ని సందర్శించండి."
        }
        return messages.get(language, messages["en"])

    async def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        return [
            {"code": code, "name": name, "native_name": name}
            for code, name in self.LANGUAGE_NAMES.items()
        ]


# Singleton instance
multilingual_llm_service = MultilingualLLMService()
