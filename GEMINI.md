# Gemini Code Assistant Workspace Context

This document provides context for the Gemini Code Assistant to understand the project structure, technologies used, and important commands.

## Project Overview

This project is a Flask-based web application for managing student registrations. It allows for user registration through a web form and also supports parsing registration data from WhatsApp messages. The application appears to be in the early stages of development.

## Key Technologies

*   **Backend:** Python, Flask
*   **Frontend:** HTML with Jinja2 templating
*   **Forms:** Flask-WTF
*   **Database:** The project is configured to use SQLAlchemy, but it is currently commented out in `app.py`. The `sqlite_demo` directory suggests that SQLite is the intended database.
*   **Dependencies:** See `requirement.txt` for a full list of Python dependencies.

## Project Structure

The project is organized as follows:

```
├── app.py                  # Main Flask application file
├── config.py               # Configuration settings
├── forms.py                # WTForms definitions
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

To run the application, you can use the following command:

```bash
flask run
```

Alternatively, you can run the `app.py` file directly:

```bash
python app.py
```

## Available Commands

*   **Run tests:**
    ```bash
    python -m unittest discover tests
    ```
