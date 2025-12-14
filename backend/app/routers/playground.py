from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging
from ..services.llm_client import generate_response

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Schemas ---
class ScenarioRequest(BaseModel):
    type: str # UPI, Phishing, Job, etc.
    difficulty: str # Beginner, Intermediate, Advanced
    channel: str # WhatsApp, SMS, Email
    language: str # English, Tamil, etc.

class ScenarioResponse(BaseModel):
    scenario_text: str
    sender_name: str
    context_notes: str

class EvaluateRequest(BaseModel):
    scenario_context: str
    user_action: str
    language: str

class EvaluateResponse(BaseModel):
    status: str # Safe, Risky, Dangerous
    explanation: str
    tips: List[str]

# --- Endpoints ---

@router.post("/generate_scenario", response_model=ScenarioResponse)
async def generate_scenario_endpoint(req: ScenarioRequest):
    """
    Generate a realistic scam scenario using OpenRouter (preferred) or Local LLM.
    """
    try:
        # Prompt Engineering
        prompt = f"""You are a Cyber Security Trainer. Generate a realistic {req.difficulty} level {req.type} scam message that would appear on {req.channel}.
Language: {req.language}.

STRICT CONTEXT RULES (MUST FOLLOW):
1. USE ONLY INDIAN NAMES (e.g., Rahul, Priya, Suresh, Anjali). NO foreign names like John/Smith.
2. USE INDIAN ENTITIES (e.g., SBI, HDFC, Paytm, Jio, Airtel, Mumbai Police).
3. USE INDIAN CURRENCY (Rs. / ₹, Lakhs, Crores).
4. Relate to common Indian situations (KYC update, Pan Card link, Electricity Bill, lottery).

Format your response exactly as:
SENDER: [Indian Name/Number/Bank]
MESSAGE: [The scam message content]
CONTEXT: [Brief styling note, e.g., "Contains a suspicious link"]

Make the message convincing but clearly a simulation.
"""
        response_text = ""
        used_model = "Local"
        
        # 1. Try OpenRouter First (Better creativity)
        try:
            from ..config import settings
            from ..services.llm_client import query_openrouter
            
            models = settings.openrouter_models_list
            for model in models:
                try:
                    logger.info(f"Playground: Trying OpenRouter {model}")
                    res = query_openrouter(prompt, model, temperature=0.8)
                    if res.status_code == 200:
                        data = res.json()
                        response_text = data["choices"][0]["message"]["content"]
                        used_model = f"OpenRouter ({model})"
                        break
                except Exception as e:
                    logger.warning(f"Playground OpenRouter try failed: {e}")
                    
        except Exception as e:
            logger.error(f"Playground OpenRouter Init Error: {e}")

        # 2. Fallback to Local LLM if OpenRouter failed
        if not response_text:
            logger.info("Playground: Falling back to Local LLM")
            response_text = generate_response(prompt, temperature=0.7, max_tokens=300, language=req.language)

        # Parse Response
        sender = "Unknown"
        message = response_text
        context = "Simulation"
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("SENDER:"):
                sender = line.replace("SENDER:", "").strip()
            elif line.startswith("MESSAGE:"):
                message = line.replace("MESSAGE:", "").strip()
            elif line.startswith("CONTEXT:"):
                context = line.replace("CONTEXT:", "").strip()
        
        # Cleanup artifacts if parsing failed slightly
        if "SENDER:" in message: message = message.split("SENDER:")[0].strip()

        return ScenarioResponse(
            scenario_text=message,
            sender_name=sender,
            context_notes=context
        )

    except Exception as e:
        logger.error(f"Error generating scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate_action", response_model=EvaluateResponse)
async def evaluate_action_endpoint(req: EvaluateRequest):
    """
    Evaluate the user's action against the scenario using OpenRouter.
    """
    try:
        prompt = f"""You are a Cyber Security Expert.
Scenario: {req.scenario_context}
User Action: {req.user_action}

Analyze this action. Is it Safe, Risky, or Dangerous?
Language: {req.language}.

Return ONLY a JSON string (no markdown). BE CONCISE.
{{
  "status": "Safe" | "Risky" | "Dangerous",
  "explanation": "1 sentence explaining why in {req.language}",
  "tips": ["Tip 1", "Tip 2"]
}}
"""
        response_text = ""
        
        # 1. Try OpenRouter First
        try:
            from ..config import settings
            from ..services.llm_client import query_openrouter
            
            models = settings.openrouter_models_list
            for model in models:
                try:
                    res = query_openrouter(prompt, model, temperature=0.2)
                    if res.status_code == 200:
                        data = res.json()
                        response_text = data["choices"][0]["message"]["content"]
                        break
                except:
                    pass
        except:
             pass

        # 2. Fallback
        if not response_text:
             response_text = generate_response(prompt, temperature=0.2, max_tokens=200, language=req.language)
        
        # Clean up code blocks
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        
        import json
        try:
            # Try finding start of JSON
            if "{" in clean_text:
                clean_text = clean_text[clean_text.find("{"):]
            if "}" in clean_text:
                clean_text = clean_text[:clean_text.rfind("}")+1]
                
            data = json.loads(clean_text)
            return EvaluateResponse(**data)
        except json.JSONDecodeError:
            logger.warning(f"LLM Invalid JSON: {clean_text}")
            return EvaluateResponse(
                status="Unknown", 
                explanation="Could not verify safety automatically. Please proceed with caution.", 
                tips=["Always verify sender identity.", "Don't click suspicious links."]
            )

    except Exception as e:
        logger.error(f"Error evaluating action: {e}")
        raise HTTPException(status_code=500, detail=str(e))
