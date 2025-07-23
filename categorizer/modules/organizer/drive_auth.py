# drive_auth.py
import os, json
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]
ENV = os.getenv("ENV", "development")
TOKEN_FILE = "token.json"
TOKEN_ENV_VAR = "GOOGLE_OAUTH_TOKEN_B64"


def drive_auth():
    creds = None
    # Production: load from env or fresh file
    if ENV == "production":
        # First try env var
        token_b64 = os.getenv(TOKEN_ENV_VAR)
        if token_b64:
            token_json = base64.b64decode(token_b64).decode("utf-8")
            creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)
        else:
            # Fallback to disk if present
            if os.path.exists(TOKEN_FILE):
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        # Dev: load or run OAuth flow locally
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh or error
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception(
                "No valid OAuth credentials. Please login via /auth/login"
            )
    # Build Drive service
    return build("drive", "v3", credentials=creds)

