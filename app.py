from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from encryption import encrypt_message, decrypt_message

app = Flask(__name__)

# In-memory message storage: {user_id: [ {content, timestamp, expiry} ] }
messages = {}

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    user_id = data.get('userId')
    message = data.get('message')
    expiry_minutes = data.get('expiryMinutes', 10)
    if not (user_id and message):
        return jsonify({'success': False, 'error': 'Missing userId or message'}), 400
    encrypted = encrypt_message(message, user_id)
    now = datetime.utcnow()
    expiry = now + timedelta(minutes=expiry_minutes)
    messages.setdefault(user_id, []).append({
        'content': encrypted,
        'timestamp': now.isoformat(),
        'expiry': expiry.isoformat()
    })
    return jsonify({'success': True, 'message_id': len(messages[user_id])-1})

@app.route('/messages/<user_id>', methods=['GET'])
def get_user_messages(user_id):
    now = datetime.utcnow()
    user_messages = messages.get(user_id, [])
    # Remove expired messages
    valid = []
    for msg in user_messages:
        if now < datetime.fromisoformat(msg['expiry']):
            valid.append(msg)
    messages[user_id] = valid
    result = []
    for msg in valid:
        try:
            content = decrypt_message(msg['content'], user_id)
        except Exception:
            content = None
        result.append({
            'content': content,
            'timestamp': msg['timestamp']
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
