from flasgger import Swagger
import cloudinary
from flask_sqlalchemy import SQLAlchemy

swagger = Swagger()
db = SQLAlchemy()

def init_extensions(app):
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )
    db.init_app(app)