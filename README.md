# StegoVault

> Conceal. Encrypt. Protect.

A secure web application that hides confidential files inside ordinary video files using steganography combined with AES-256 encryption. The resulting video plays normally while secretly containing the hidden data — retrievable only with the correct password.

🔗 **Live Demo:** [https://stego-vault-mzef.onrender.com](https://stego-vault-mzef.onrender.com)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Security](#security)
- [License](#license)
- [Author](#author)

---

## Overview

StegoVault is a full-stack web application that implements **video steganography** — the practice of concealing information within a non-secret medium. Unlike traditional encryption which makes data unreadable, steganography makes the very existence of the data undetectable.

StegoVault combines two layers of protection:

1. **Steganography** — the secret file is invisibly embedded inside a normal video file
2. **AES-256 Encryption** — the file is encrypted before embedding, so even if discovered, it cannot be read without the correct password

---

## Features

- 🔐 AES-256-GCM military-grade encryption
- 🎭 Video steganography — hidden data is completely invisible during playback
- 🛡️ SHA-256 integrity verification — detects any tampering before extraction
- 🔑 Password-based key derivation using PBKDF2 (200,000 iterations)
- 📁 Supports multiple file formats (PDF, DOCX, TXT, PNG, JPG, MP3, ZIP, and more)
- 🎬 Supports MP4, AVI, MKV video formats as carrier files
- 🖥️ Clean, responsive web interface with real-time progress tracking
- 🚫 Zero data storage — all files are processed in memory and deleted immediately
- 🌐 Deployment-ready with Gunicorn and environment-based configuration

---

## How It Works

### Embedding Process

```
Original Video + Secret File + Password
        ↓
Secret file is encrypted using AES-256-GCM
        ↓
SHA-256 hash of original video is computed
        ↓
Encrypted data is appended to video binary:
[ Video Data ] + [ STEGO_VAULT_v1 marker ] + [ SHA-256 hash ] + [ filename ] + [ encrypted data ]
        ↓
Output: Stego Video (plays normally in any video player)
```

### Extraction Process

```
Stego Video + Password
        ↓
Locate STEGO_VAULT_v1 marker in binary
        ↓
Verify SHA-256 hash — detect tampering
        ↓
Decrypt data using AES-256-GCM + password
        ↓
Output: Original secret file restored
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Encryption | AES-256-GCM via `cryptography` library |
| Integrity | SHA-256 via `hashlib` |
| Video Processing | OpenCV, NumPy |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Production Server | Gunicorn |
| Deployment | Render |
| Version Control | Git, GitHub |

---

## Installation

### Prerequisites

- Python 3.9 or higher
- Git

### Steps

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/stego-vault.git
cd stego-vault
```

**2. Create and activate virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file in root directory:**
```env
FLASK_ENV=development
SECRET_KEY=your_super_secret_key_here
MAX_CONTENT_LENGTH=500
```

**5. Run the application:**
```bash
python app.py
```

**6. Open in browser:**
```
http://127.0.0.1:5000
```

---

## Usage

### Hiding a File in a Video

1. Navigate to the **Embed** tab
2. Upload a cover video (MP4, AVI, or MKV)
3. Upload the secret file you want to hide
4. Enter a strong password
5. Click **Embed & Encrypt**
6. Download the stego video

### Extracting a Hidden File

1. Navigate to the **Extract** tab
2. Upload the stego video
3. Enter the correct password
4. Click **Extract & Decrypt**
5. Download the recovered file

---

## Project Structure

```
stego_vault/
├── app.py                  # Flask application and routes
├── config.py               # Environment-based configuration
├── Procfile                # Render deployment config
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── .gitignore              # Git ignore rules
├── stego/
│   ├── __init__.py
│   ├── embed.py            # Steganography embedding logic
│   ├── extract.py          # Steganography extraction logic
│   ├── encrypt.py          # AES-256-GCM encryption/decryption
│   └── integrity.py        # SHA-256 integrity verification
├── static/
│   ├── css/
│   │   ├── style.css       # App page styles
│   │   └── landing.css     # Landing page styles
│   └── js/
│       └── main.js         # Frontend logic
├── templates/
│   ├── landing.html        # Landing page
│   └── index.html          # Main app page
├── uploads/                # Temporary upload storage
└── outputs/                # Temporary output storage
```

---

## Screenshots

> Add screenshots of your landing page and app page here.

| Landing Page | App — Embed | App — Extract |
|-------------|-------------|---------------|
| _(screenshot)_ | _(screenshot)_ | _(screenshot)_ |

---

## Security

| Feature | Implementation |
|---------|---------------|
| Encryption | AES-256-GCM — authenticated encryption |
| Key Derivation | PBKDF2-HMAC-SHA256 with 200,000 iterations |
| Salt | 16-byte random salt per encryption |
| Nonce | 12-byte random nonce per encryption |
| Integrity | SHA-256 hash verification before extraction |
| Storage | No files or passwords are ever stored |
| Transport | HTTPS enforced on Render deployment |

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Raj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Author

**Raj**

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

> This project was built for educational purposes to demonstrate the combination of steganography and cryptography for secure data concealment.
