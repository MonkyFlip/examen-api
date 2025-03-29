from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.db import db
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Habilitar CORS
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos si no existen
    app.register_blueprint(routes)  # Registrar el Blueprint de rutas
    return app
