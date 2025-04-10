import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    API_KEY = os.getenv('API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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