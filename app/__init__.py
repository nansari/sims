"""This is the main application package."""
# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config
from flask_session_captcha import FlaskSessionCaptcha

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
captcha = FlaskSessionCaptcha()

def create_app():
    """Create and configure the Flask application."""""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'login'
    captcha.init_app(app)

    with app.app_context():
        from app import routes, models

    return app