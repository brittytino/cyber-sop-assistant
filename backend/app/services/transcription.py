from groq import Groq
import os
import logging
from ..config import settings

logger = logging.getLogger(__name__)

# Initialize Groq client
# Note: Ideally this should be initialized once, but for simplicity in this function-based approach
# we can instantiate it lazily or here.
_groq_client = None

def get_groq_client():
    global _groq_client
    if not _groq_client and settings.GROQ_API_KEY:
        _groq_client = Groq(api_key=settings.GROQ_API_KEY)
    return _groq_client

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file using Groq Whisper
    """
    try:
        client = get_groq_client()
        if not client:
            return "Error: GROQ_API_KEY not configured."

        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
                # language="en", # Removed to support auto-detection (multilingual)
                temperature=0.0
            )
            # verbose_json returns an object with 'text' and 'language' fields
            return {
                "text": transcription.text,
                "language": getattr(transcription, "language", "english")
            }
    except Exception as e:
        logger.error(f"Groq Transcription Error: {e}")
        return f"Error transcribing audio: {str(e)}"
