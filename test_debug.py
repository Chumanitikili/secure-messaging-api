import base64
from debug_code import broken_decrypt, fixed_decrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

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

if __name__ == '__main__':
    test_broken_and_fixed()
