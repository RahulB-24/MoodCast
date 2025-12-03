from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from backend.utils.spotify_client import build_auth_url, save_user_token
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/auth")

@router.get("/login")
def login():
    return {"auth_url": build_auth_url()}

@router.get("/callback")
def callback(request: Request):
    # Spotify sends ?code=...&state=...
    code = request.query_params.get("code")
    error = request.query_params.get("error")
    if error:
        return JSONResponse({"error": error}, status_code=400)
    if not code:
        return JSONResponse({"error": "no_code"}, status_code=400)

    # Exchange code for tokens
    from backend.utils.spotify_client import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    if resp.status_code != 200:
        return JSONResponse({"error": "token_exchange_failed", "detail": resp.text}, status_code=500)

    data = resp.json()
    # save tokens
    save_user_token(data)
    # redirect to a small success page or return json
    return JSONResponse({"status": "ok", "message": "Spotify login success. You can close this tab."})
