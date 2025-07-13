import os

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'app', 'app.db')

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Database wiped.")
else:
    print("Database file not found.")
