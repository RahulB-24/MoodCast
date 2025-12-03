from fastapi import APIRouter, Request
from backend.utils.spotify_auth import get_auth_url, get_tokens_from_code

router = APIRouter()

@router.get("/auth/login")
def auth_login():
    """
    Returns URL to redirect user to Spotify login.
    """
    return {"auth_url": get_auth_url()}


@router.get("/auth/callback")
def auth_callback(code: str):
    """
    Spotify redirects here with authorization code.
    Exchange it for access+refresh tokens.
    """
    tokens = get_tokens_from_code(code)
    return tokens
