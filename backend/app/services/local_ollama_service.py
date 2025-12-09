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
        Generate SOP guidance using RAG + Ollama
        
        Args:
            query: User query
            language: Target language
            category: Optional category filter
            use_rag: Whether to use RAG retrieval
            
        Returns:
            Structured SOP response
        """
        try:
            # Retrieve relevant documents from RAG
            context = ""
            sources = []
            
            if use_rag:
                try:
                    rag_results = rag_service.search(query, top_k=settings.RAG_TOP_K)
                    if rag_results:
                        context = "\n\n".join([
                            f"Document {i+1}:\n{doc['content']}"
                            for i, doc in enumerate(rag_results)
                        ])
                        sources = [
                            {
                                "title": doc.get("metadata", {}).get("title", "Unknown"),
                                "source": doc.get("metadata", {}).get("source", "Unknown"),
                                "relevance_score": doc.get("score", 0.0)
                            }
                            for doc in rag_results
                        ]
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {e}")
            
            # Generate structured SOP response
            lang_name = self.language_names.get(language, "English")
            
            sop_prompt = f"""Based on the user's query about cybercrime reporting, provide a structured Standard Operating Procedure (SOP) in {lang_name}.

User Query: {query}

Provide your response in the following structure:

1. IMMEDIATE ACTIONS (to do right now):
   - List specific immediate steps

2. WITHIN 24 HOURS:
   - List actions to take within a day

3. WITHIN 7 DAYS:
   - List follow-up actions

4. ONGOING MEASURES:
   - List preventive and monitoring steps

5. IMPORTANT CONTACTS:
   - List relevant helplines, portals, and authorities

Keep each point concise and actionable."""
            
            response_text = await self.generate_response(
                prompt=sop_prompt,
                language=language,
                context=context
            )
            
            return {
                "sop_guidance": response_text,
                "sources": sources,
                "language": language,
                "category": category,
                "used_rag": use_rag and len(sources) > 0
            }
            
        except Exception as e:
            logger.error(f"SOP generation error: {e}", exc_info=True)
            raise
    
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
