"""Configuration file."""
import secrets
import os
# import socket

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BATCHES = [ 'GLB-B03', 'HYD-B10', 'KARAMA-08']
    STATUS = ['CallOut', 'Active', 'Drop-Out', 'Graduated', 'NextBatch', 'On-Hold', 'Pending',]
    NATURE = ['Exited', 'Soft',]
    COUNTRIES = ['India', 'USA', 'UK', 'Canada', 'Singapore', 'Australia', 'KSA', 'UAE', 'Qatar', 'China', 'Japan', 'Malaysia', 'Philippines', 'Thailand', 'Vietnam', 'Indonesia', 'Pakistan', 'Other']
    


