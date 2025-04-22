import requests
import base64
from encryption import derive_key, encrypt_message

BASE_URL = "http://localhost:5000"

user_id = "user123"
message = "This is a secret message"
expiry_minutes = 1

# Test POST /messages
post_data = {
    "userId": user_id,
    "message": message,
    "expiryMinutes": expiry_minutes
}
response = requests.post(f"{BASE_URL}/messages", json=post_data)
print("POST /messages response:", response.status_code, response.json())

# Test GET /messages/:userId
response = requests.get(f"{BASE_URL}/messages/{user_id}")
print("GET /messages/:userId response:", response.status_code, response.json())

# Test POST /debug/decrypt
payload = encrypt_message("DebugTest", user_id)
key = base64.b64encode(derive_key(user_id)).decode()
debug_data = {
    "payload": payload,
    "key": key
}
response = requests.post(f"{BASE_URL}/debug/decrypt", json=debug_data)
print("POST /debug/decrypt response:", response.status_code, response.json())
