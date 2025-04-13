import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEYS = os.getenv("VALID_API_KEYS", "abc123").split(",")
    HMAC_SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "s3cret").encode()
    ALLOWED_IPS = os.getenv("ALLOWED_IPS", "127.0.0.1,172.20.0.5").split(",")
    SWAGGER = {
        "title": "Text-to-Speech API",
        "description": "A simple API to convert text to speech using gTTS",
        "version": "1.0.0",
        "swagger": "2.0",
        "static_url_path": "/flasgger_static",
        "specs_route": "/swagger/",
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "headers": []
}