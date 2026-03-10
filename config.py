import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 500)) * 1024 * 1024

    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv'}
    ALLOWED_FILE_EXTENSIONS = {'pdf', 'txt', 'docx', 'png', 'jpg', 'jpeg', 'zip', 'gif', 'webp', 'bmp', 'mp3', 'wav', 'xlsx', 'csv'}