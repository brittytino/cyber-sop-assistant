import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000/api"

def test_health():
    logger.info("--- Testing Health Endpoint ---")
    try:
        r = requests.get(f"{BASE_URL}/health")
        r.raise_for_status()
        logger.info(f"Health Status: {r.status_code}")
        logger.info(f"Response: {r.json()}")
    except Exception as e:
        logger.error(f"Health check failed: {e}")

def test_chat_continuity():
    logger.info("--- Testing Chat Continuity ---")
    
    # 1. Start a new chat
    payload_1 = {
        "message": "Hello, this is a test.",
        "language": "English"
    }
    
    chat_id = None
    
    logger.info("Sending first message...")
    try:
        r = requests.post(f"{BASE_URL}/chat/message", json=payload_1, stream=True)
        r.raise_for_status()
        
        for line in r.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if data.get("type") == "meta":
                        chat_id = data.get("chat_id")
                        logger.info(f"Captured Query 1 Chat ID: {chat_id}")
                    elif data.get("type") == "content":
                        print(data.get("data"), end="", flush=True)
                except:
                    pass
        print("\n")
        
        if not chat_id:
            logger.error("Failed to capture Chat ID from first response!")
            return

        # 2. Continue the chat
        logger.info(f"Sending follow-up to Chat ID {chat_id}...")
        payload_2 = {
            "message": "What did I just say?",
            "chat_id": chat_id,
            "language": "English"
        }
        
        r2 = requests.post(f"{BASE_URL}/chat/message", json=payload_2, stream=True)
        r2.raise_for_status()
        
        new_chat_id = None
        response_content = ""
        
        for line in r2.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if data.get("type") == "meta":
                        new_chat_id = data.get("chat_id")
                    elif data.get("type") == "content":
                        response_content += data.get("data")
                except:
                    pass
        
        if new_chat_id == chat_id:
             logger.info("SUCCESS: Chat ID preserved across requests!")
        else:
             logger.error(f"FAILURE: Chat ID changed! Original: {chat_id}, New: {new_chat_id}")

    except Exception as e:
        logger.error(f"Chat test failed: {e}")

def main():
    test_health()
    test_chat_continuity()

if __name__ == "__main__":
    main()
