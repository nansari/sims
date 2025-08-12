# app/config.py
"""
This module defines the configuration settings for the Flask application.

It includes settings for the secret key, database URI, and other
application-specific configurations. The values are sourced from environment
variables, with fallback values for development purposes.
"""
import secrets
import os
# import socket

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SECRET_KEY (str): A secret key for signing session cookies. It is
            sourced from the SECRET_KEY environment variable or a randomly
            generated hex token.
        SQLALCHEMY_DATABASE_URI (str): The database URI for SQLAlchemy. It is
            sourced from the DATABASE_URL environment variable or defaults to
            a local SQLite database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): A flag to disable SQLAlchemy's
            event system, which is not needed and adds overhead.
        GENDERS (list): A list of gender options for user registration.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///c:/Users/nasim/Documents/git/sims/database.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///c:/Users/nasim/Documents/git/sims/data/sqlite3_bin/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GENDERS = ['M', 'F']
    LOGFILE = os.path.join(basedir, 'sims.log')
    # Flask-Session-Captcha
    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 6
    CAPTCHA_WIDTH = 160
    CAPTCHA_HEIGHT = 60
    SESSION_TYPE = 'filesystem'
    DEVELOPMENT_SERVER = ('DESKTOP-RLGODEE', 'server-does-not-exit')