import os
import struct
from stego.encrypt import encrypt_data
from stego.integrity import compute_hash

MARKER = b'STEGO_VAULT_v1'  # Unique marker to identify our hidden data

def embed_file(video_path: str, secret_path: str, password: str, output_path: str) -> dict:
    """
    Embed a secret file inside a video file.
    
    Process:
    1. Read the original video and compute its hash
    2. Read and encrypt the secret file
    3. Append encrypted data after video content with a marker
    4. Save as new output video
    """

    # Step 1 — Read original video bytes
    with open(video_path, 'rb') as f:
        video_data = f.read()

    # Step 2 — Compute hash of original video (before embedding)
    original_hash = compute_hash(video_path)

    # Step 3 — Read secret file
    with open(secret_path, 'rb') as f:
        secret_data = f.read()

    # Step 4 — Encrypt the secret file with the password
    encrypted_secret = encrypt_data(secret_data, password)

    # Step 5 — Get original filename to restore it during extraction
    original_filename = os.path.basename(secret_path).encode('utf-8')
    filename_length = struct.pack('>I', len(original_filename))  # 4 bytes

    # Step 6 — Get encrypted data length
    secret_length = struct.pack('>I', len(encrypted_secret))  # 4 bytes

    # Step 7 — Encode original hash as bytes
    hash_bytes = original_hash.encode('utf-8')  # 64 bytes (SHA-256 hex)

    # Step 8 — Build the final stego video:
    # video_data + MARKER + hash(64 bytes) + filename_length(4) + filename + secret_length(4) + encrypted_secret
    stego_data = (
        video_data +
        MARKER +
        hash_bytes +
        filename_length +
        original_filename +
        secret_length +
        encrypted_secret
    )

    # Step 9 — Write the stego video to output path
    with open(output_path, 'wb') as f:
        f.write(stego_data)

    return {
        'success': True,
        'output_path': output_path,
        'original_hash': original_hash,
        'secret_filename': os.path.basename(secret_path),
        'video_size': len(video_data),
        'secret_size': len(secret_data),
        'output_size': len(stego_data)
    }