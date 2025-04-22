from datetime import datetime, timedelta
from collections import defaultdict, deque

# In-memory message storage: {user_id: deque([(encrypted_message, timestamp)])}
messages = defaultdict(deque)
MESSAGE_EXPIRY_MINUTES = 10  # Bonus: message expiry

def store_message(user_id, encrypted_message):
    now = datetime.utcnow()
    messages[user_id].append((encrypted_message, now))
    # Remove expired messages
    while messages[user_id] and now - messages[user_id][0][1] > timedelta(minutes=MESSAGE_EXPIRY_MINUTES):
        messages[user_id].popleft()

def get_messages(user_id):
    now = datetime.utcnow()
    # Remove expired messages
    while messages[user_id] and now - messages[user_id][0][1] > timedelta(minutes=MESSAGE_EXPIRY_MINUTES):
        messages[user_id].popleft()
    return [msg for msg, ts in messages[user_id]]
