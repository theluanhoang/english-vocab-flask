from flask import Flask
from app.config import Config
from app.extensions import swagger, init_extensions, db
from app.api.tts.routes import tts_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    init_extensions(app)
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])


    swagger.init_app(app)

    app.register_blueprint(tts_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()

    return app