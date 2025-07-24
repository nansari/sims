# Gemini Code Assistant Workspace Context

This document provides context for the Gemini Code Assistant to understand the project structure, technologies used, and important commands.

## Project Overview

This project is a Flask-based web application for managing student registrations. It allows for user registration through a web form and also supports parsing registration data from WhatsApp messages. The application appears to be in the early stages of development.

## Key Technologies

*   **Backend:** Python, Flask
*   **Frontend:** HTML with Jinja2 templating
*   **Forms:** Flask-WTF
*   **Database:** The project is configured to use SQLAlchemy with SQLite.
*   **Dependencies:** See `requirement.txt` for a full list of Python dependencies.

## Project Structure
The project is organized as follows:

```
├── app.py                  # Main Flask application file
├── config.py               # Configuration settings
├── forms.py                # WTForms definitions
├── routers.py              # Route definitions
├── models.py               # Database models
├── requirement.txt         # Python dependencies
├── templates/              # Jinja2 templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   └── ...                 # Other application pages
├── static/                 # Static assets (CSS, JavaScript)
├── functions/              # Helper functions
│   └── parse_wa_text.py    # Parses WhatsApp registration text
├── tests/                  # Application tests
│   └── tests.py
└── ...                     # Other files and directories
```

## How to Run the Application

Never run application after making changes to code as I am running the flask in debug mode that restart itself on any code change.

# DOCUMENTATION
- Do not waste time in adding doc strings to module, function, class. Leave the doc strings wherever it is already added.

# IMPORTANT
- Keep security on priority to secure the web app from hackers

