import base64
from debug_code import broken_decrypt, fixed_decrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import pytest
from encryption import derive_key, encrypt_message

def test_broken_and_fixed():
    key = os.urandom(32)
    iv = os.urandom(16)
    message = b"Hello, world!"
    padder = padding.PKCS7(128).padder()
    padded = padder.update(message) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    key_b64 = base64.b64encode(key).decode()
    iv_b64 = base64.b64encode(iv).decode()
    ct_b64 = base64.b64encode(ciphertext).decode()
    broken = broken_decrypt(ct_b64, key_b64, iv_b64)
    fixed = fixed_decrypt(ct_b64, key_b64, iv_b64)
    assert fixed == message.decode()
    assert fixed != broken

def test_broken_decrypt_fails():
    user_id = "testuser"
    key = base64.b64encode(derive_key(user_id)).decode()
    payload = encrypt_message("SecretMsg", user_id)
    # Broken function should not return correct plaintext
    result = broken_decrypt(payload, key)
    assert result != "SecretMsg", "broken_decrypt should not correctly decrypt the message"

def test_fixed_decrypt_succeeds():
    user_id = "testuser"
    key = base64.b64encode(derive_key(user_id)).decode()
    payload = encrypt_message("SecretMsg", user_id)
    result = fixed_decrypt(payload, key)
    assert result == "SecretMsg", "fixed_decrypt should correctly decrypt the message"

def test_debug_comment():
    """
    The bug in broken_decrypt is that it tries to decrypt the entire payload (IV + ciphertext) as ciphertext,
    instead of splitting out the IV and only decrypting the ciphertext. CBC mode requires the IV to be passed
    to the cipher, and the ciphertext to be decrypted. The fix extracts the IV (first 16 bytes) and passes only
    the remaining bytes to the decryptor, matching the encryption logic.
    """
    pass

if __name__ == '__main__':
    test_broken_and_fixed()
