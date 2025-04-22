# Secure Messaging API

This is a Flask-based secure messaging API that allows users to securely store and retrieve messages. The API uses AES-256-CBC encryption to protect message content.

## Design Decisions

### Encryption Method and Mode

I chose AES-256-CBC (Cipher Block Chaining) for this implementation because:

- **Security**: AES-256 provides a high level of security with a 256-bit key length.
- **Industry Standard**: It's widely accepted as a secure encryption method.
- **CBC Mode**: CBC mode requires an IV (Initialization Vector) which prevents identical plaintext blocks from producing identical ciphertext blocks, adding an extra layer of security.
- **Library Support**: It's well-supported by Python's cryptography library.

### Ensuring Only the Original User Can Access Their Messages

In this implementation:

- Messages are stored in a user-specific collection keyed by user ID.
- In a production environment, I would implement proper authentication using JWT tokens or similar.
- The API would validate the authenticated user ID against the requested user ID.
- Only messages created for a specific user ID can be retrieved by that user.

### IV Storage and Extraction

For each message:

1. A random 16-byte (128-bit) IV is generated.
2. The IV is prepended to the encrypted data.
3. The combined payload is encoded in base64.
4. During decryption, the first 16 bytes are extracted as the IV, and the rest is treated as the encrypted data.

This approach ensures:
- Each message has a unique IV
- The IV is securely stored with the encrypted data
- The IV is easily extractable for decryption

### Preventing User ID Spoofing

To prevent user ID spoofing:

1. **Authentication**: In a production application, I would implement JWT-based authentication.
2. **Authorization**: Middleware would validate that the authenticated user is only accessing their own messages.
3. **Server-side Validation**: User IDs would be validated from the authentication token, not from request parameters.
4. **Rate Limiting**: Implement rate limiting to prevent brute force attacks.

## Debug Task

The issue in the `broken_decrypt` function:

The function correctly extracts the IV from the first 16 bytes of the payload, but then it incorrectly uses the entire payload (including the IV) as the encrypted data. This is incorrect because the IV should not be part of the data to decrypt.

The fix involves:
1. Extracting the IV from the first 16 bytes
2. Using only the remaining bytes (excluding the IV) as the encrypted data

This issue is demonstrated in the test cases where the broken function fails to decrypt a message that was encrypted with our encryption service.

## Setup and Installation

### Prerequisites

- Python 3.8+
- PowerShell

### Installation

```powershell
# Clone the repository
git clone <repository-url>
cd secure-messaging-api

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Running Tests

```powershell
python test_api.py
```

## API Endpoints

### POST /messages

Store a new encrypted message for a user.

**Request Body:**
```json
{
  "userId": "user123",
  "message": "This is a secret message",
  "expiryMinutes": 10  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message_id": 0
}
```

### GET /messages/:userId

Retrieve all messages for a specific user (decrypted).

**Response:**
```json
[
  {
    "content": "This is a secret message",
    "timestamp": "2023-04-21T12:34:56.789"
  }
]
```

### POST /debug/decrypt

Test the fixed decryption function.

**Request Body:**
```json
{
  "payload": "base64EncodedEncryptedPayload",
  "key": "encryptionKey"
}
```

**Response:**
```json
{
  "broken_result": null,
  "broken_error": "Error message if broken function fails",
  "fixed_result": "Decrypted message",
  "explanation": "See comments in the fixed_decrypt function for detailed explanation."
}
```

## Assumptions and Constraints

1. This implementation uses in-memory storage for simplicity. In a production environment, a proper database would be used.
2. Proper authentication is simulated but not fully implemented as it wasn't a core requirement.
3. The encryption key is generated at runtime. In a production environment, a secure key management system would be used.
4. The optional message expiry feature is implemented using a timestamp-based approach.

## Author
Chumani (coding challenge solution)
