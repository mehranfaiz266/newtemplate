# Simple Flask Credential Manager

This project provides a minimal Flask application that allows users to register, log in, and securely store API credentials. Secrets are encrypted using Fernet before being saved in the database.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set environment variables as needed (see `env.sample`). For development you can simply set `SECRET_KEY` and optionally `DATABASE_URL`.

3. Run the application:
   ```bash
   flask --app run.py run
   ```

4. Visit `http://localhost:5000` to register a new user and add API credentials.

## Security Notes

- API secrets are encrypted before being stored in the database using a key derived from `SECRET_KEY`.
- For production usage make sure to set a strong `SECRET_KEY` and store the encryption key securely.
