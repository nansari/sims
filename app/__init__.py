# app/__init__.py

from flask import Flask
from .config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY


from app import routes # this should be last line
