from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import shutil
import os

from backend.utils.spotify_client import get_client_credentials_token
from backend.utils.inference import run_inference

# ---------------------------------------------------------
# Router with prefix
# ---------------------------------------------------------
router = APIRouter(
    prefix="/recommend_v3",
    tags=["recommend_v3"]
)

# ---------------------------------------------------------
# Language → search keyword map
# ---------------------------------------------------------
LANGSEARCH = {
    "ta": "tamil",
    "te": "telugu",
    "hi": "hindi",
    "ml": "malayalam",
    "kn": "kannada",
    "en": "english",
    "es": "spanish",
    "ko": "korean"
}

# ---------------------------------------------------------
# Request Model
# ---------------------------------------------------------
class SearchReq(BaseModel):
    mood: Optional[str] = ""
    valence: Optional[float] = 5.0
    arousal: Optional[float] = 5.0
    language: Optional[str] = "none"
    genres: List[str] = []
    artist_names: List[str] = []
    track_names: List[str] = []
    keywords: List[str] = []

# ---------------------------------------------------------
# Suggested keywords
# ---------------------------------------------------------
SUGGESTED_KEYWORDS = [
    "lofi", "romantic", "acoustic", "melancholic", "energetic",
    "chill", "workout", "party", "study", "sad remix", "instrumental"
]

# ---------------------------------------------------------
# Query builder
# ---------------------------------------------------------
def build_queries(mood, language, genres, artists, tracks, keywords):
    qlist = []
    mood = mood.lower().strip() if mood else ""
    lang_word = LANGSEARCH.get(language.lower(), "") if language else ""

    def add(q):
        q = q.strip()
        if q and q.lower() != "string":
            qlist.append(q)

    # artists
    for a in artists[:3]:
        add(f"{a} {mood}")
        add(f"{a} {lang_word} {mood}")

    # tracks
    for t in tracks[:3]:
        add(f"{t} {mood}")
        add(f"{t} {lang_word} {mood}")

    # genres
    for g in genres[:3]:
        add(f"{mood} {g} {lang_word}")
        add(f"{g} {lang_word}")

    # keywords
    for kw in keywords[:5]:
        add(f"{kw} {mood} {lang_word}")
        add(f"{kw} {lang_word}")

    # mood + language combos
    if mood:
        add(f"{mood} {lang_word} songs")
        add(f"{mood} songs")
        add(f"{mood} mix")

    if lang_word:
        add(f"{lang_word} {mood}".strip())
        add(f"{lang_word} top hits")

    if not qlist:
        add(f"{mood} songs" if mood else "top hits")

    add("top hits")

    # dedupe + limit
    seen = set()
    out = []
    for q in qlist:
        if q.lower() not in seen:
            seen.add(q.lower())
            out.append(q)
        if len(out) >= 10:
            break

    return out

# ---------------------------------------------------------
# Spotify search
# ---------------------------------------------------------
def search_tracks(token: str, query: str, limit: int = 25):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": limit}

    r = requests.get(url, headers=headers, params=params, timeout=10)
    if r.status_code != 200:
        return []
    return r.json().get("tracks", {}).get("items", [])

# ---------------------------------------------------------
# Scoring
# ---------------------------------------------------------
def score_track(track, mood, language, genres, keywords):
    name = (track.get("name") or "").lower()
    artists = " ".join([a.get("name", "").lower() for a in track.get("artists", [])])
    popularity = track.get("popularity", 0)
    pop_score = popularity / 100.0

    text_score = 0.0

    if mood.lower() in name or mood.lower() in artists:
        text_score += 0.35

    lang_word = LANGSEARCH.get(language.lower(), "")
    if lang_word and lang_word in name:
        text_score += 0.20

    for g in genres:
        if g.lower() in name:
            text_score += 0.15

    for kw in keywords:
        if kw.lower() in name or kw.lower() in artists:
            text_score += 0.25

    if text_score > 1:
        text_score = 1

    return 0.6 * text_score + 0.4 * pop_score

def score_and_sort(all_tracks, mood, language, genres, keywords):
    scored = []
    for tid, t in all_tracks.items():
        s = score_track(t, mood, language, genres, keywords)
        scored.append((s, t))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [{
        "id": t["id"],
        "name": t["name"],
        "artist": t["artists"][0]["name"] if t.get("artists") else None,
        "image": t.get("album", {}).get("images", [{}])[0].get("url"),
        "preview_url": t.get("preview_url"),
        "score": round(s, 4),
        "popularity": t.get("popularity")
    } for s, t in scored]

# ---------------------------------------------------------
# OPTIONS handler for CORS preflight
# ---------------------------------------------------------
@router.options("/search_by_mood")
async def options_search_by_mood():
    return {"status": "ok"}

# ---------------------------------------------------------
# POST: /recommend_v3/search_by_mood
# ---------------------------------------------------------
@router.post("/search_by_mood")
def search_by_mood(req: SearchReq):

    mood = req.mood or ""
    language = req.language or "none"

    queries = build_queries(
        mood, language,
        req.genres, req.artist_names,
        req.track_names, req.keywords
    )

    token = get_client_credentials_token()
    if not token:
        raise HTTPException(status_code=500, detail="Spotify token error")

    all_tracks = {}
    for q in queries:
        items = search_tracks(token, q)
        for t in items:
            all_tracks[t["id"]] = t

    results = score_and_sort(all_tracks, mood, language, req.genres, req.keywords)

    return {
        "mood_used": mood,
        "queries_used": queries,
        "suggested_keywords": SUGGESTED_KEYWORDS,
        "results": results[:30]
    }
