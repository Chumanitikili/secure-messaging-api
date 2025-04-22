import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def broken_decrypt(payload_b64, key_b64):
    """
    Broken decryption function: incorrectly uses the whole payload (IV + ciphertext) as ciphertext.
    """
    payload = base64.b64decode(payload_b64)
    key = base64.b64decode(key_b64)
    cipher = Cipher(algorithms.AES(key), modes.CBC(payload[:16]), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(payload) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode(errors='ignore')

def fixed_decrypt(payload_b64, key_b64):
    """
    Fixed decryption function: extracts IV and decrypts only the ciphertext.
    """
    payload = base64.b64decode(payload_b64)
    key = base64.b64decode(key_b64)
    iv = payload[:16]
    ciphertext = payload[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()
