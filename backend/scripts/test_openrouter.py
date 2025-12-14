
import sys
import os
import requests
import json

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from app.config import settings
    print("Configuration loaded successfully.")
    print(f"API Key: {settings.OPENROUTER_API_KEY[:10]}...")
    print(f"Models: {settings.openrouter_models_list}")

    def test_openrouter():
        with open("test_output.txt", "w", encoding="utf-8") as f:
            f.write("--- Testing OpenRouter Models ---\n")
            param_models = settings.openrouter_models_list
            success = False
            
            for model in param_models:
                f.write(f"\nTesting Model: {model}...\n")
                print(f"Testing {model}...")
                
                headers = {
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5173",
                    "X-Title": "Cyber SOP Assistant Test"
                }
                
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": "Hello"}],
                    "temperature": 0.2
                }
                
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        f.write(f"✅ SUCCESS: {model}\n")
                        content = response.json()['choices'][0]['message']['content']
                        f.write(f"Response: {content}\n")
                        success = True
                    else:
                        f.write(f"❌ FAILED: {model} (Status: {response.status_code})\n")
                        f.write(f"Error: {response.text}\n")
                except Exception as e:
                     f.write(f"⚠️ EXCEPTION: {model} - {e}\n")
            
            return success

    if __name__ == "__main__":
        test_openrouter()

except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"Error: {e}")
