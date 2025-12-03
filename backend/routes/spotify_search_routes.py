from fastapi import APIRouter, HTTPException
import requests
from backend.utils.spotify_client import get_client_credentials_token

router = APIRouter(prefix="/search")

@router.get("/tracks")
def search_tracks(query: str):
    token = get_client_credentials_token()
    if not token:
        raise HTTPException(status_code=500, detail="Failed to get Spotify token")

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 10}

    res = requests.get(url, headers=headers, params=params).json()
    items = res.get("tracks", {}).get("items", [])
    out = []
    for t in items:
        out.append({
            "id": t["id"],
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None
        })
    return out

@router.get("/artists")
def search_artists(query: str):
    token = get_client_credentials_token()
    if not token:
        raise HTTPException(status_code=500, detail="Failed to get Spotify token")

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "artist", "limit": 10}

    res = requests.get(url, headers=headers, params=params).json()
    items = res.get("artists", {}).get("items", [])
    out = []
    for a in items:
        out.append({
            "id": a["id"],
            "name": a["name"],
            "image": a["images"][0]["url"] if a["images"] else None
        })
    return out

@router.get("/genres")
def get_genres():
    token = get_client_credentials_token()
    if not token:
        raise HTTPException(status_code=500, detail="Failed to get Spotify token")

    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {"Authorization": f"Bearer {token}"}

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {"error": "Could not fetch genres"}

    return {"genres": res.json().get("genres", [])}
