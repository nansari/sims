"""This is the main application package."""
# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


# these should be after app is created
from app import routes, models
