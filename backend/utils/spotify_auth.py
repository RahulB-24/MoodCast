import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_auth_url():
    scope = (
        "user-read-email "
        "playlist-read-private "
        "playlist-modify-private "
        "playlist-modify-public "
        "user-read-private "
        "user-read-playback-state "
    )

    return (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={scope.replace(' ', '%20')}"
        f"&redirect_uri={REDIRECT_URI}"
    )


def get_tokens_from_code(code: str):
    """
    Exchange Spotify authorization code for access + refresh token.
    """
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    return response.json()


def refresh_access_token(refresh_token: str):
    """
    Generate a new access token using refresh token.
    """
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    return response.json()
