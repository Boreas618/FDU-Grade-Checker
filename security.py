from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    hash = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hash)

def encrypt(text: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(text.encode())

def decrypt(encrypted_data: bytes, key: bytes) -> int:
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()