import hashlib

CHUNK_SIZE = 8192  # Read file in chunks to handle large videos efficiently

def compute_hash(file_path: str) -> str:
    """
    Compute SHA-256 hash of a file.
    Returns the hash as a hex string.
    """
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)

    return sha256.hexdigest()

def verify_integrity(file_path: str, original_hash: str) -> bool:
    """
    Verify a file's integrity by comparing its current hash
    to the original hash stored during embedding.
    Returns True if intact, False if tampered or corrupted.
    """
    current_hash = compute_hash(file_path)
    return current_hash == original_hash

def get_file_signature(file_path: str) -> dict:
    """
    Returns a dictionary with the file hash and size.
    Used to give the user a full integrity report.
    """
    import os
    file_hash = compute_hash(file_path)
    file_size = os.path.getsize(file_path)

    return {
        'hash': file_hash,
        'size': file_size,
        'algorithm': 'SHA-256'
    }