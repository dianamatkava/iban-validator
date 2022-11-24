import os
from environs import Env
from flask import Flask
from extensions import db, migrate
from iban_validator.views import ibanb 
from iban_validator.models import *


env = Env()
env.read_env()


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configs
    app.config.from_mapping(
        FLASK_APP = env.str('FLASK_APP', default='app.py'),
        FLASK_DEBUG = env.str('FLASK_DEBUG', default='development'),
        SECRET_KEY = env.str(
            'SECRET_KEY', default='5af1dcd9351c49963a6a32d5bc66ff4b'
        ),
        SQLALCHEMY_DATABASE_URI = env.str(
            'SQLALCHEMY_DATABASE_URI', default='sqlite:///iban.sqlite3'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS = True,
    )
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register apps
    app.register_blueprint(ibanb)
    
    # Registered extensions
    with app.app_context():
        db.init_app(app)
        db.create_all()
        
        
    migrate.init_app(app, db, render_as_batch=True)
    
    
    return app

app = create_app()
