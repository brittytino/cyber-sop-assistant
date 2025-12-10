"""
Local Ollama Multilingual Service
Uses only local Ollama for all AI operations with native multilingual support
"""
import httpx
import asyncio
from typing import Dict, Any, Optional, List
from app.core.config import settings
from app.core.logging import logger
from app.services.rag_service import rag_service


class LocalOllamaService:
    """Service for local Ollama LLM with multilingual support"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        
        # Language configuration
        self.language_names = {
            "en": "English",
            "hi": "Hindi (हिंदी)",
            "ta": "Tamil (தமிழ்)",
            "te": "Telugu (తెలుగు)",
            "bn": "Bengali (বাংলা)",
            "mr": "Marathi (मराठी)",
            "gu": "Gujarati (ગુજરાતી)",
            "kn": "Kannada (ಕನ್ನಡ)"
        }
    
    async def generate_response(
        self,
        prompt: str,
        language: str = "en",
        system_message: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Generate response using local Ollama
        
        Args:
            prompt: User prompt
            language: Target language code
            system_message: Optional system message
            context: Optional context from RAG
            
        Returns:
            Generated response text
        """
        try:
            # Build the full prompt with language instruction
            lang_name = self.language_names.get(language, "English")
            
            if system_message is None:
                system_message = f"""You are a helpful cybercrime SOP assistant. 
Respond in {lang_name} language.
Be concise, accurate, and helpful.
Provide actionable steps when relevant."""
            
            # Add context if provided
            full_prompt = prompt
            if context:
                full_prompt = f"""Context from knowledge base:
{context}

User query: {prompt}

Please provide a helpful response based on the context above."""
            
            # Add language instruction
            if language != "en":
                full_prompt += f"\n\nIMPORTANT: Respond entirely in {lang_name}."
            
            # Call Ollama API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "system": system_message,
                        "stream": False,
                        "options": {
                            "temperature": settings.LLM_TEMPERATURE,
                            "top_p": settings.LLM_TOP_P,
                            "top_k": settings.LLM_TOP_K,
                            "num_predict": settings.LLM_MAX_TOKENS,
                            "num_ctx": getattr(settings, 'OLLAMA_NUM_CTX', 4096),
                            "repeat_penalty": settings.LLM_REPEAT_PENALTY,
                        }
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Ollama error: {response.status_code} - {response.text}")
                    raise Exception(f"Ollama API error: {response.status_code}")
                
                result = response.json()
                return result.get("response", "").strip()
                
        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            raise
    
    async def chat_with_language_awareness(
        self,
        message: str,
        language: str = "en",
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Chat with language-aware context
        
        Args:
            message: User message
            language: Target language code
            conversation_history: Previous conversation
            
        Returns:
            Chat response in target language
        """
        try:
            # Build conversation context
            context = ""
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    context += f"{role.title()}: {content}\n"
            
            # Add current message
            full_prompt = f"{context}\nUser: {message}\nAssistant:"
            
            lang_name = self.language_names.get(language, "English")
            system_msg = f"""You are a helpful cybercrime SOP assistant helping users in {lang_name}.
Maintain conversation context and respond naturally.
Provide clear, actionable guidance."""
            
            response = await self.generate_response(
                prompt=full_prompt,
                language=language,
                system_message=system_msg
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Chat error: {e}", exc_info=True)
            raise
    
    async def generate_sop_response(
        self,
        query: str,
        language: str = "en",
        category: Optional[str] = None,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Generate structured SOP guidance using RAG + Ollama
        
        Args:
            query: User query
            language: Target language
            category: Optional category filter
            use_rag: Whether to use RAG retrieval
            
        Returns:
            Structured SOP response matching ChatResponse schema
        """
        try:
            # Retrieve relevant documents from RAG
            context = ""
            sources = []
            
            if use_rag:
                try:
                    from app.services.rag_service import rag_service
                    if rag_service.is_loaded():
                        rag_results = await rag_service.retrieve(query, top_k=5)
                        if rag_results:
                            context = "\n\n".join([
                                f"Reference {i+1} ({doc.get('source', 'Unknown')}):\n{doc.get('content', '')}"
                                for i, doc in enumerate(rag_results)
                            ])
                            sources = [doc.get("source", "Unknown") for doc in rag_results]
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {e}")
            
            # Generate structured SOP response
            lang_name = self.language_names.get(language, "English")
            
            sop_prompt = f"""You are an expert on Indian cybercrime reporting procedures. Based on the user's query, provide a comprehensive Standard Operating Procedure (SOP) in {lang_name}.

User Query: {query}
{f"Category: {category}" if category else ""}

{f"Reference Documents:{context}" if context else ""}

Provide your response with the following sections:

**IMMEDIATE ACTIONS** (to do right now):
List 3-5 immediate critical steps the victim should take within the next hour.

**REPORTING STEPS** (within 24-48 hours):
Provide step-by-step instructions for official reporting:
1. Where to report (cybercrime portal, police station, etc.)
2. What documents/information to prepare
3. How to file the complaint

**EVIDENCE CHECKLIST**:
List all types of evidence to collect and preserve (screenshots, messages, transaction records, etc.)

**OFFICIAL LINKS AND CONTACTS**:
Provide:
- National Cyber Crime Reporting Portal: https://cybercrime.gov.in
- Helpline: 1930 (24x7)
- Email: complaints@cybercrime.gov.in
- Other relevant portals/helplines

**PLATFORM-SPECIFIC GUIDANCE** (if applicable):
If the crime involves specific platforms (WhatsApp, Instagram, bank, UPI, etc.), provide platform-specific reporting steps.

Ensure all guidance is:
- Specific to Indian jurisdiction
- Actionable and practical
- In {lang_name} language
- Empathetic and supportive"""
            
            response_text = await self.generate_response(
                prompt=sop_prompt,
                language=language,
                system_message=f"You are a helpful cybercrime guidance assistant. Always respond in {lang_name}."
            )
            
            # Parse the LLM response into structured format
            # For now, we'll create a basic structure and let the LLM response be displayed
            immediate_actions = []
            reporting_steps = []
            evidence_checklist = []
            
            # Try to extract sections from the response
            lines = response_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                upper_line = line.upper()
                if 'IMMEDIATE' in upper_line and 'ACTION' in upper_line:
                    current_section = 'immediate'
                elif 'REPORTING' in upper_line and 'STEP' in upper_line:
                    current_section = 'reporting'
                elif 'EVIDENCE' in upper_line and 'CHECKLIST' in upper_line:
                    current_section = 'evidence'
                elif 'OFFICIAL' in upper_line or 'CONTACT' in upper_line:
                    current_section = 'links'
                elif 'PLATFORM' in upper_line:
                    current_section = 'platform'
                elif line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
                    # Extract bullet point
                    cleaned = line.lstrip('-•*123456789. ')
                    if current_section == 'immediate' and cleaned:
                        immediate_actions.append(cleaned)
                    elif current_section == 'reporting' and cleaned:
                        reporting_steps.append(cleaned)
                    elif current_section == 'evidence' and cleaned:
                        evidence_checklist.append(cleaned)
            
            # If parsing failed, provide fallback structure
            if not immediate_actions:
                immediate_actions = [response_text[:500] + "..."] if len(response_text) > 500 else [response_text]
            
            # Return structured response matching ChatResponse schema
            return {
                "immediate_actions": immediate_actions[:5],  # Max 5
                "reporting_steps": reporting_steps[:10] if reporting_steps else [
                    f"1. Visit National Cyber Crime Reporting Portal: https://cybercrime.gov.in",
                    f"2. Register your complaint with all evidence",
                    f"3. Note down your complaint number for follow-up",
                    f"4. If urgent, call helpline 1930"
                ],
                "evidence_checklist": evidence_checklist[:15] if evidence_checklist else [
                    "Screenshots of fraudulent messages/posts",
                    "Transaction IDs and bank statements",
                    "URLs and account details of perpetrators",
                    "Communication records (emails, chats)",
                    "Timestamps of all incidents"
                ],
                "official_links": [
                    {
                        "name": "National Cyber Crime Reporting Portal",
                        "url": "https://cybercrime.gov.in",
                        "category": "reporting",
                        "description": "Official portal to report cybercrimes in India"
                    },
                    {
                        "name": "Citizen Financial Cyber Fraud Reporting",
                        "url": "https://cybercrime.gov.in/Webform/Crime_AuthoLogin.aspx",
                        "category": "reporting",
                        "description": "Report financial frauds and track complaints"
                    }
                ],
                "emergency_contacts": [
                    {
                        "name": "Cyber Crime Helpline",
                        "number": "1930",
                        "description": "24x7 National Helpline for all cybercrimes",
                        "available_24x7": True
                    },
                    {
                        "name": "Women Helpline",
                        "number": "181",
                        "description": "24x7 Women Safety Helpline",
                        "available_24x7": True
                    }
                ],
                "platform_specific": {
                    "platform": self._detect_platform(query),
                    "additional_guidance": response_text
                },
                "sources": sources if sources else ["Cybercrime.gov.in", "MeitY Guidelines", "IT Act 2000"]
            }
            
        except Exception as e:
            logger.error(f"SOP generation error: {e}", exc_info=True)
            # Return minimal fallback response
            return {
                "immediate_actions": [
                    "Stop all communication with the perpetrator immediately",
                    "Do not delete any evidence (messages, emails, screenshots)",
                    "Note down all details: dates, times, amounts, account numbers",
                    "Call Cyber Crime Helpline: 1930 for immediate assistance"
                ],
                "reporting_steps": [
                    "Visit https://cybercrime.gov.in to file online complaint",
                    "Visit nearest police station with all evidence",
                    "Keep copies of all documents and complaint numbers"
                ],
                "evidence_checklist": [
                    "Screenshots of messages/transactions",
                    "Bank statements and transaction IDs",
                    "Email/message headers",
                    "URLs and account details of scammers"
                ],
                "official_links": [],
                "emergency_contacts": [],
                "platform_specific": None,
                "sources": []
            }
    
    def _detect_platform(self, query: str) -> Optional[str]:
        """Detect platform mentioned in query"""
        query_lower = query.lower()
        platforms = {
            "whatsapp": ["whatsapp", "watsapp"],
            "instagram": ["instagram", "insta"],
            "facebook": ["facebook", "fb"],
            "twitter": ["twitter", "x.com"],
            "upi": ["upi", "paytm", "phonepe", "googlepay", "gpay"],
            "bank": ["bank", "account", "atm"],
            "email": ["email", "gmail", "mail"]
        }
        
        for platform, keywords in platforms.items():
            if any(keyword in query_lower for keyword in keywords):
                return platform
        return None
    
    async def translate_content(
        self,
        content: str,
        target_language: str,
        context: Optional[str] = None
    ) -> str:
        """
        Translate content to target language
        
        Args:
            content: Content to translate
            target_language: Target language code
            context: Optional context about the content
            
        Returns:
            Translated content
        """
        try:
            lang_name = self.language_names.get(target_language, "English")
            
            translate_prompt = f"""Translate the following text to {lang_name}.
Maintain the meaning, tone, and technical accuracy.

Text to translate:
{content}"""
            
            if context:
                translate_prompt += f"\n\nContext: {context}"
            
            translated = await self.generate_response(
                prompt=translate_prompt,
                language=target_language,
                system_message="You are a professional translator. Provide accurate translations while preserving meaning and context."
            )
            
            return translated
            
        except Exception as e:
            logger.error(f"Translation error: {e}", exc_info=True)
            raise
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        return [
            {
                "code": code,
                "name": name.split(" (")[0],
                "native_name": name.split(" (")[1].rstrip(")") if " (" in name else name
            }
            for code, name in self.language_names.items()
        ]
    
    async def check_health(self) -> Dict[str, Any]:
        """Check Ollama service health"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m.get("name") for m in models]
                    
                    return {
                        "status": "healthy",
                        "ollama_url": self.base_url,
                        "configured_model": self.model,
                        "model_available": any(self.model in m for m in model_names),
                        "available_models": model_names
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status_code}"
                    }
                    
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global service instance
local_ollama_service = LocalOllamaService()
