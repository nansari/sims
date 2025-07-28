# sims.py
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db

app = create_app()
from app.models import User, Password, Contact


@app.shell_context_processor
def make_shell_context():
    """Provide a shell context for the Flask application."""
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Password': Password, 'Contact': Contact}