# auth.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os, json

router = APIRouter()
SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRETS_FILE = os.getenv("CREDENTIALS_FILE", "credentials.json")
# Redirect URI for OAuth flow
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "https://google-drive-organizer.onrender.com/api/auth/callback")
TOKEN_FILE = "token.json"

# Initialize flow
def get_flow(state: str = None):
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
    )

@router.get("/login")
def login():
    flow = get_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    # Save state to file/session (here simple file)
    with open(".oauth_state", "w") as f: f.write(state)
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(request: Request):
    # Read saved state
    if not os.path.exists(".oauth_state"):
        raise HTTPException(400, "OAuth state missing")
    state = open(".oauth_state").read()
    flow = get_flow(state)
    flow.fetch_token(authorization_response=str(request.url))

    creds = flow.credentials
    # Save credentials to file with restricted permissions
    data = creds.to_json()
    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(data)
    os.chmod(TOKEN_FILE, 0o600)

    return JSONResponse({"status": "success", "message": "Google OAuth successful"})
