
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def run_debug():
    print("--- Starting Auth Debug ---")
    
    # 1. Signup
    print("\n1. Testing Signup...")
    username = "test_user_debug"
    password = "password123"
    
    try:
        signup_res = requests.post(f"{BASE_URL}/auth/signup", json={"username": username, "password": password})
        print(f"Signup Status: {signup_res.status_code}")
        if signup_res.status_code not in [200, 400]: # 400 if exists is fine for now
            print(f"Signup Failed: {signup_res.text}")
    except Exception as e:
        print(f"Signup Exception: {e}")
        return

    # 2. Login
    print("\n2. Testing Login...")
    try:
        login_res = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        print(f"Login Status: {login_res.status_code}")
        
        if login_res.status_code != 200:
            print(f"Login Failed: {login_res.text}")
            return
            
        token = login_res.json()["access_token"]
        print("Login Success. Token received.")
    except Exception as e:
        print(f"Login Exception: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Test get_chats (Protected GET)
    print("\n3. Testing GET /chat/chats (Protected)...")
    try:
        chats_res = requests.get(f"{BASE_URL}/chat/chats", headers=headers)
        print(f"Get Chats Status: {chats_res.status_code}")
        if chats_res.status_code != 200:
             print(f"Get Chats Failed: {chats_res.text}")
    except Exception as e:
        print(f"Get Chats Exception: {e}")

    # 4. Test send_message (Protected POST)
    print("\n4. Testing POST /chat/message (Protected)...")
    try:
        msg_payload = {
            "message": "Hello from debug",
            "chat_id": None,
            "language": "English"
        }
        msg_res = requests.post(f"{BASE_URL}/chat/message", json=msg_payload, headers=headers, stream=True)
        print(f"Send Message Status: {msg_res.status_code}")
        
        if msg_res.status_code == 200:
            print("Stream started successfully.")
            # Consume a bit of stream
            for chunk in msg_res.iter_lines():
                if chunk:
                    print(f"Chunk received: {len(chunk)} bytes")
                    break # Just need one to prove it works
        else:
             print(f"Send Message Failed: {msg_res.text}")

    except Exception as e:
        print(f"Send Message Exception: {e}")

if __name__ == "__main__":
    run_debug()
