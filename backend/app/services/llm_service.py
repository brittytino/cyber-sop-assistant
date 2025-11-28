"""
LLM Service - Ollama Integration
Handles communication with local Ollama LLM
"""
import json
import httpx
from typing import Dict, List, Optional, Any
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import OllamaConnectionError
from app.utils.prompt_templates import SYSTEM_PROMPT, format_sop_prompt


class LLMService:
    """Ollama LLM service"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def check_connection(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                logger.info(f"Available Ollama models: {[m['name'] for m in models]}")
                return True
            return False
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False
    
    async def generate_sop(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate SOP response using RAG context
        
        Args:
            query: User query
            context_docs: Retrieved context documents from RAG
            language: Response language code
            
        Returns:
            Structured SOP response
        """
        try:
            # Build context from retrieved documents
            context_text = self._build_context(context_docs)
            
            # Build prompt
            prompt = format_sop_prompt(query, context_text, language)
            
            # Generate response
            response = await self._generate(prompt)
            
            # Parse JSON response
            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("LLM response is not valid JSON, attempting to extract")
                parsed_response = self._extract_json_from_text(response)
            
            # Add sources
            parsed_response["sources"] = [doc.get("source", "Unknown") for doc in context_docs]
            
            return parsed_response
            
        except Exception as e:
            logger.error(f"Error generating SOP: {e}", exc_info=True)
            raise OllamaConnectionError(f"Failed to generate response: {str(e)}")
    
    async def _generate(self, prompt: str) -> str:
        """
        Generate text from Ollama
        
        Args:
            prompt: Full prompt including system and user messages
            
        Returns:
            Generated text
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": settings.LLM_TEMPERATURE,
                "top_p": settings.LLM_TOP_P,
                "top_k": settings.LLM_TOP_K,
                "num_predict": settings.LLM_MAX_TOKENS
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code != 200:
                raise OllamaConnectionError(
                    f"Ollama API returned status {response.status_code}: {response.text}"
                )
            
            result = response.json()
            return result.get("response", "")
            
        except httpx.TimeoutException:
            raise OllamaConnectionError("Ollama request timed out")
        except httpx.RequestError as e:
            raise OllamaConnectionError(f"Ollama request failed: {str(e)}")
    
    def _build_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        if not context_docs:
            return "No specific documents retrieved."
        
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            content = doc.get("content", "")
            source = doc.get("source", "Unknown")
            date = doc.get("date", "N/A")
            
            context_parts.append(
                f"Document {i}:\n"
                f"Source: {source}\n"
                f"Date: {date}\n"
                f"Content: {content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text that might have extra content"""
        try:
            # Try to find JSON between braces
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to extract JSON: {e}")
        
        # Return fallback structure
        return {
            "immediate_actions": ["Contact national cybercrime helpline 1930"],
            "reporting_steps": ["Visit https://cybercrime.gov.in and file a complaint"],
            "evidence_checklist": ["Screenshots", "Transaction IDs", "Chat logs"],
            "official_links": [
                {"name": "National Cyber Crime Portal", "url": "https://cybercrime.gov.in", "category": "reporting"}
            ],
            "emergency_contacts": [
                {"name": "Cyber Fraud Helpline", "number": "1930", "description": "24x7 helpline for financial fraud"}
            ],
            "platform_specific": {}
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.client.aclose()


# Global instance
llm_service = LLMService()
