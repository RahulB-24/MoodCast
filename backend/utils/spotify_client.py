import os
import time
import base64
import json
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
USER_TOKEN_PATH = os.getenv("SPOTIFY_USER_TOKEN_PATH", "backend/utils/user_token.json")

SCOPES = "playlist-read-private playlist-modify-private playlist-modify-public user-read-playback-state user-read-email user-read-private"

# ------------------------
# Client Credentials Token (for search/basic operations)
# ------------------------
_client_token_cache = {"token": None, "expires_at": 0}

def get_client_credentials_token() -> Optional[str]:
    if _client_token_cache["token"] and _client_token_cache["expires_at"] > time.time() + 60:
        return _client_token_cache["token"]

    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
    )
    if resp.status_code != 200:
        print("client_credentials token error", resp.status_code, resp.text)
        return None
    data = resp.json()
    _client_token_cache["token"] = data["access_token"]
    _client_token_cache["expires_at"] = time.time() + data.get("expires_in", 3600)
    return _client_token_cache["token"]

# ------------------------
# Authorization Code Flow user token persistence
# ------------------------
def build_auth_url(state: str = "moodcast_state"):
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "show_dialog": "true"
    }
    qs = "&".join([f"{k}={requests.utils.quote(v)}" for k, v in params.items()])
    return f"https://accounts.spotify.com/authorize?{qs}"

def save_user_token(data: dict):
    # expected fields: access_token, refresh_token, expires_in, obtained_at
    data["obtained_at"] = time.time()
    with open(USER_TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_user_token() -> Optional[dict]:
    if not os.path.exists(USER_TOKEN_PATH):
        return None
    try:
        with open(USER_TOKEN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def refresh_user_token_if_needed() -> Optional[str]:
    tok = load_user_token()
    if not tok:
        return None
    expires_in = tok.get("expires_in", 3600)
    obtained = tok.get("obtained_at", 0)
    if time.time() < obtained + expires_in - 60:
        return tok.get("access_token")

    # refresh
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": tok.get("refresh_token"),
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    if resp.status_code != 200:
        print("refresh failed", resp.status_code, resp.text)
        return None
    new = resp.json()
    # maintain refresh_token if not returned
    if "refresh_token" not in new:
        new["refresh_token"] = tok.get("refresh_token")
    save_user_token(new)
    return new.get("access_token")
