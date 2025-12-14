
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from app.services.llm_client import generate_response

if __name__ == "__main__":
    print("Testing LLM connection...")
    try:
        response = generate_response("Hello, are you ready for cybercrime assistance?")
        print(f"LLM Response: {response}")
    except Exception as e:
        print(f"LLM Test Failed: {e}")
