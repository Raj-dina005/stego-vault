import os
import struct
from stego.encrypt import decrypt_data
from stego.integrity import compute_hash

MARKER = b'STEGO_VAULT_v1'  # Same marker used during embedding
HASH_SIZE = 64               # SHA-256 hex string is always 64 characters

def extract_file(stego_video_path: str, password: str, output_folder: str) -> dict:
    """
    Extract a hidden file from a stego video.

    Process:
    1. Read the stego video and find the marker
    2. Verify video integrity using stored hash
    3. Decrypt the hidden data using the password
    4. Restore the original file with its original filename
    """

    # Step 1 — Read the stego video
    with open(stego_video_path, 'rb') as f:
        stego_data = f.read()

    # Step 2 — Find the marker
    marker_pos = stego_data.rfind(MARKER)
    if marker_pos == -1:
        raise ValueError("No hidden data found in this video!")

    # Step 3 — Extract the original video hash (64 bytes after marker)
    hash_start = marker_pos + len(MARKER)
    stored_hash = stego_data[hash_start:hash_start + HASH_SIZE].decode('utf-8')

    # Step 4 — Verify video integrity
    # Compute hash of original video portion only (before the marker)
    original_video_data = stego_data[:marker_pos]
    temp_video_path = stego_video_path + '.tmp'

    with open(temp_video_path, 'wb') as f:
        f.write(original_video_data)

    current_hash = compute_hash(temp_video_path)
    os.remove(temp_video_path)

    if current_hash != stored_hash:
        raise ValueError("Integrity check failed — video may have been tampered with!")

    # Step 5 — Extract filename length and filename
    filename_length_start = hash_start + HASH_SIZE
    filename_length = struct.unpack('>I', stego_data[filename_length_start:filename_length_start + 4])[0]

    filename_start = filename_length_start + 4
    original_filename = stego_data[filename_start:filename_start + filename_length].decode('utf-8')

    # Step 6 — Extract encrypted secret data
    secret_length_start = filename_start + filename_length
    secret_length = struct.unpack('>I', stego_data[secret_length_start:secret_length_start + 4])[0]

    secret_start = secret_length_start + 4
    encrypted_secret = stego_data[secret_start:secret_start + secret_length]

    # Step 7 — Decrypt the secret data
    try:
        decrypted_data = decrypt_data(encrypted_secret, password)
    except ValueError:
        raise ValueError("Wrong password or corrupted data — extraction failed!")

    # Step 8 — Save the extracted file to output folder
    output_path = os.path.join(output_folder, original_filename)
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

    return {
        'success': True,
        'output_path': output_path,
        'original_filename': original_filename,
        'file_size': len(decrypted_data),
        'integrity_verified': True
    }