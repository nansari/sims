# sims.py
import socket
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db

app = create_app()
from app.models import User, Password, Contact


@app.shell_context_processor
def make_shell_context():
    """Provide a shell context for the Flask application."""
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Password': Password, 'Contact': Contact}

if __name__ == '__main__':
    IPAddr = socket.gethostbyname(socket.gethostname())
    app.run(host=IPAddr, ssl_context='adhoc')
