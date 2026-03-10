import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Number of iterations for key derivation - higher = more secure but slower
ITERATIONS = 200_000
SALT_SIZE = 16   # bytes
NONCE_SIZE = 12  # bytes for AES-GCM

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from a password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode())

def encrypt_data(data: bytes, password: str) -> bytes:
    """
    Encrypt data using AES-256-GCM with a password.
    Returns: salt + nonce + ciphertext (all combined into one bytes object)
    """
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    # Combine salt + nonce + ciphertext so we can decrypt later
    return salt + nonce + ciphertext

def decrypt_data(encrypted_data: bytes, password: str) -> bytes:
    """
    Decrypt data using AES-256-GCM with a password.
    Expects: salt + nonce + ciphertext (as produced by encrypt_data)
    """
    salt = encrypted_data[:SALT_SIZE]
    nonce = encrypted_data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = encrypted_data[SALT_SIZE + NONCE_SIZE:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        return aesgcm.decrypt(nonce, ciphertext, None)
    except Exception:
        raise ValueError("Decryption failed — wrong password or corrupted data!")