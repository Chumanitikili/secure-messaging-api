# Secure Messaging API

A Flask-based API for secure, per-user message storage and retrieval, using AES-256-CBC encryption. Designed for clarity, modularity, and workplace security standards.

---

## Design Decisions & Implementation

### 1. What encryption method and mode did you choose, and why?
- **AES-256 in CBC mode** using the `cryptography` library.
    - **Why:** AES-256 is an industry-standard, secure symmetric cipher. CBC mode ensures ciphertext is unique per message via a random IV. The cryptography library provides robust, well-tested primitives.

### 2. How will you ensure only the original user can access their messages?
- **Per-user key derivation:** Each user's key is derived from their user ID (for demo; use a password or secret in production).
- **Token-based authentication:** (Bonus) Each user is assigned a token; endpoints require the correct token to access messages.
- **Access control:** The API only allows retrieval of messages for the authenticated user.

### 3. How do you plan to store and later extract the IV?
- **IV generation:** A random 16-byte IV is generated for each message.
- **IV storage:** The IV is prepended to the ciphertext and the combined bytes are base64-encoded.
- **IV extraction:** During decryption, the first 16 bytes (after base64 decoding) are extracted as the IV, and the rest is the ciphertext.

### 4. How would you prevent user ID spoofing to access other users' messages?
- **Authentication:** Endpoints require a valid token for the user ID.
- **Authorization:** The server checks that the token matches the user ID before allowing message access.
- **No trust in user input:** User IDs are not trusted from the client alone; server-side checks are enforced.

---

## Debug Task

### Broken Function: `broken_decrypt()` in `debug_code.py`
- **Issue:** The function incorrectly uses the entire payload (IV + ciphertext) as ciphertext, causing decryption to fail.
- **Fix:** Extract the IV from the first 16 bytes, and use only the remaining bytes as the ciphertext.
- **Test case:** See `test_debug.py` for a failing test with the broken function and a passing test with the fixed function.
- **Explanation:**
    - CBC mode requires the IV and ciphertext to be separate. Including the IV in the ciphertext causes padding errors or garbage output.
    - The fix properly separates IV and ciphertext, matching the encryption logic.

---

## Evaluation Criteria Addressed
- **Correct encryption/decryption**: AES-256-CBC, correct IV handling
- **Modular code**: All crypto in `encryption.py`, API in `app.py`, debug in `debug_code.py`, tests in `test_api.py`/`test_debug.py`
- **Secure per-user access**: Token-based authentication (bonus), per-user key
- **Clear answers & comments**: See above and code comments
- **Edge cases & errors**: API returns clear error messages for missing/invalid data
- **Bonus**: Message expiry, token-based authentication, unit tests

---

## Bonus Features
- **Message expiry:** Messages auto-delete after expiry (default 10 min, configurable).
- **Token-based authentication:** (Optional, see below)
- **Unit tests:** Provided for encryption, storage, and debug logic.

---

## Instructions

### Prerequisites
- Python 3.8+

### Installation
```sh
pip install -r requirements.txt
```

### Run the API
```sh
python app.py
```

### Run Tests
```sh
python test_api.py
python test_debug.py
```

---

## Assumptions & Constraints
- In-memory storage for demo; use a database for production.
- Key derivation from user ID is for demonstration only.
- Token authentication is basic; use JWT/OAuth for production.
- No real user registration implemented.

---

## Author
Chumani
