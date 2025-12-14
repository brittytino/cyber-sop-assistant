"""
LLM Client - Connects to Ollama for local LLM inference and OpenRouter for Multi-language
"""
import requests
import json
from ..config import settings
import logging

logger = logging.getLogger(__name__)

def query_openrouter(prompt: str, model: str, stream: bool = False, temperature: float = 0.2):
    """Query OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
         "HTTP-Referer": "http://localhost:5173", # Required by OpenRouter
        "X-Title": "Cyber SOP Assistant"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "stream": stream
    }
    
    return requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        stream=stream,
        timeout=60
    )

def generate_response(prompt: str, temperature: float = 0.2, max_tokens: int = 2000, language: str = "English") -> str:
    """
    Generate a response using OpenRouter (Non-English) or Ollama (English/Fallback)
    """
    # 1. Try OpenRouter for Non-English
    if language.lower() not in ["english", "en"]:
        try:
            logger.info(f"Non-English ({language}) detected. Attempting OpenRouter...")
            models_to_try = settings.openrouter_models_list
            
            for model in models_to_try:
                try:
                    logger.info(f"Trying OpenRouter model: {model}")
                    response = query_openrouter(prompt, model, stream=False, temperature=temperature)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data["choices"][0]["message"]["content"]
                        logger.info(f"OpenRouter Success ({model})")
                        return answer
                    else:
                        logger.warning(f"OpenRouter Error ({model}): {response.status_code} - {response.text}")
                except Exception as e:
                    logger.error(f"OpenRouter Exception ({model}): {e}")
            
            logger.warning("All OpenRouter models failed. Falling back to Local LLM.")
        except Exception as e:
            logger.error(f"OpenRouter Global Error: {e}")

    # 2. Local LLM (Ollama) - Default / Fallback
    try:
        url = f"{settings.LLM_ENDPOINT}/api/generate"
        
        # Add system instruction for language if local LLM is used
        final_prompt = prompt
        if language.lower() not in ["english", "en"]:
            final_prompt = f"[SYSTEM: Respond strictly in {language} language.]\n\n{prompt}"

        payload = {
            "model": settings.LLM_MODEL,
            "prompt": final_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "repeat_penalty": 1.1,
            }
        }
        
        logger.info(f"Sending request to Ollama: {settings.LLM_MODEL}")
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        answer = result.get("response", "").strip()
        
        logger.info(f"Received response from Ollama ({len(answer)} chars)")
        return answer
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama.")
        return "Error: Cannot connect to the local LLM. Please ensure Ollama is running."
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f"Error generating response: {str(e)}"

def generate_streaming_response(prompt: str, temperature: float = 0.2, max_tokens: int = 4000, language: str = "English"):
    """
    Generate a streaming response using OpenRouter or Ollama
    """
    # 1. Try OpenRouter for Non-English
    if language.lower() not in ["english", "en"]:
        try:
            logger.info(f"Non-English ({language}) Stream. Attempting OpenRouter...")
            
            # Iterate through models for fallback
            models_to_try = settings.openrouter_models_list
            stream_connected = False
            
            for model in models_to_try:
                if stream_connected: break
                
                try:
                    logger.info(f"Trying OpenRouter Stream: {model}")
                    response = query_openrouter(prompt, model, stream=True, temperature=temperature)
                    
                    if response.status_code == 200:
                        logger.info(f"OpenRouter Stream Connected ({model})")
                        stream_connected = True
                        
                        for line in response.iter_lines():
                            if line:
                                decoded = line.decode('utf-8')
                                # logger.info(f"RAW CHUNK: {decoded}") # DEBUG LOG
                                
                                if decoded.startswith('data: '):
                                    try:
                                        json_str = decoded[6:] # key 'data: '
                                        if json_str.strip() == '[DONE]': break
                                        
                                        chunk = json.loads(json_str)
                                        content = chunk['choices'][0]['delta'].get('content', '')
                                        if content:
                                            yield content
                                    except:
                                        pass
                                elif decoded.startswith(':') or not decoded.strip():
                                    continue # Keep-alive or empty
                                else:
                                    logger.warning(f"Unexpected Line format: {decoded}")
                        return # Exit if successful (generator exhausted)
                    else:
                        logger.warning(f"OpenRouter Stream Failed ({model}): {response.status_code}")
                except Exception as e:
                    logger.error(f"OpenRouter Stream Exception ({model}): {e}")
            
            if not stream_connected:
                logger.warning("All OpenRouter streaming models failed. Falling back to Local LLM.")

        except Exception as e:
            logger.error(f"OpenRouter Stream Error: {e}")
        
    # 2. Local LLM Fallback / Default
    try:
        url = f"{settings.LLM_ENDPOINT}/api/generate"
        
        final_prompt = prompt
        if language.lower() not in ["english", "en"]:
            final_prompt = f"[SYSTEM: Respond strictly in {language} language.]\n\n{prompt}"

        payload = {
            "model": settings.LLM_MODEL,
            "prompt": final_prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "repeat_penalty": 1.1,
            }
        }
        
        logger.info(f"Stream request to Ollama: {settings.LLM_MODEL}")
        
        with requests.post(url, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
                        if chunk.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
                        
    except Exception as e:
        logger.error(f"Error streaming response: {str(e)}")
        yield f"Error: {str(e)}"

def check_ollama_health() -> dict:
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get(f"{settings.LLM_ENDPOINT}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            return {
                "status": "healthy",
                "available_models": model_names,
                "configured_model": settings.LLM_MODEL
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "configured_model": settings.LLM_MODEL
        }
