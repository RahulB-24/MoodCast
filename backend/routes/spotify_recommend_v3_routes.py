from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import shutil
import os

from backend.utils.spotify_client import get_client_credentials_token
from backend.utils.inference import run_inference  # ML mood prediction

router = APIRouter(prefix="/recommend_v3", tags=["recommend_v3"])


# ---------------------------------------------------------
# Language → Search Keyword Mapping
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
# User Search Request Model
# ---------------------------------------------------------
class SearchReq(BaseModel):
    mood: Optional[str] = ""
    valence: Optional[float] = 5.0
    arousal: Optional[float] = 5.0
    language: Optional[str] = "none"
    genres: List[str] = []
    artist_names: List[str] = []
    track_names: List[str] = []
    keywords: List[str] = []  # NEW


# ---------------------------------------------------------
# Suggested keywords to show in UI
# ---------------------------------------------------------
SUGGESTED_KEYWORDS = [
    "lofi", "romantic", "acoustic", "melancholic", "energetic",
    "chill", "workout", "party", "study", "sad remix", "instrumental"
]


# ---------------------------------------------------------
# Query Builder (Main Logic) – FIXED
# ---------------------------------------------------------
def build_queries(mood: str, language: str, genres: list, artists: list, tracks: list, keywords: list):
    qlist = []

    mood = mood.lower().strip() if mood else ""
    lang_word = LANGSEARCH.get(language.lower(), "") if language else ""

    # -----------------------------------------------------
    # Helper to safely add a query (prevents 'string' or empty)
    # -----------------------------------------------------
    def add(q):
        q = q.strip()
        if q and q.lower() != "string":
            qlist.append(q)

    # -----------------------------------------------------
    # ARTIST QUERIES
    # -----------------------------------------------------
    for a in artists[:3]:
        if a.strip():
            add(f"{a} {mood}")
            add(f"{a} {lang_word} {mood}")

    # -----------------------------------------------------
    # TRACK QUERIES
    # -----------------------------------------------------
    for t in tracks[:3]:
        if t.strip():
            add(f"{t} {mood}")
            add(f"{t} {lang_word} {mood}")

    # -----------------------------------------------------
    # GENRE QUERIES
    # -----------------------------------------------------
    for g in genres[:3]:
        if g.strip():
            add(f"{mood} {g} {lang_word}")
            add(f"{g} {lang_word}")

    # -----------------------------------------------------
    # KEYWORD QUERIES (NEW)
    # -----------------------------------------------------
    for kw in keywords[:5]:
        if kw.strip():
            add(f"{kw} {mood} {lang_word}")
            add(f"{kw} {lang_word}")

    # -----------------------------------------------------
    # MOOD + LANGUAGE TOP QUERIES
    # -----------------------------------------------------
    if mood:
        add(f"{mood} {lang_word} songs")
        add(f"{mood} songs")
        add(f"{mood} mix")

    # -----------------------------------------------------
    # FALLBACKS — ensure we always have meaningful search terms
    # -----------------------------------------------------
    if lang_word:
        add(f"{lang_word} {mood}".strip())
        add(f"{lang_word} top hits")

    if not qlist:
        # absolute fallback
        add(f"{mood} songs" if mood else "top hits")

    add("top hits")

    # -----------------------------------------------------
    # DEDUPE + LIMIT
    # -----------------------------------------------------
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
# Spotify Search Helper
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
# Simple Scoring System
# ---------------------------------------------------------
def score_track(track: dict, mood: str, language: str, genres: list, keywords: list):
    name = (track.get("name") or "").lower()
    artists = " ".join([a.get("name", "").lower() for a in track.get("artists", [])])
    popularity = track.get("popularity", 0)
    pop_score = popularity / 100.0

    text_score = 0.0

    # match mood
    if mood.lower() in name or mood.lower() in artists:
        text_score += 0.35

    # match language keyword
    lang_word = LANGSEARCH.get(language.lower(), "")
    if lang_word and lang_word in name:
        text_score += 0.20

    # match genres
    for g in genres:
        if g.lower() in name:
            text_score += 0.15

    # match custom keywords (NEW)
    for kw in keywords:
        if kw.lower() in name or kw.lower() in artists:
            text_score += 0.25

    if text_score > 1.0:
        text_score = 1.0

    final_score = 0.6 * text_score + 0.4 * pop_score
    return final_score


# ---------------------------------------------------------
# Apply scoring to multiple tracks
# ---------------------------------------------------------
def score_and_sort(all_tracks, mood, language, genres, keywords):
    scored = []
    for tid, t in all_tracks.items():
        s = score_track(t, mood, language, genres, keywords)
        scored.append((s, t))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "id": t["id"],
            "name": t["name"],
            "artist": t["artists"][0]["name"] if t.get("artists") else None,
            "image": t.get("album", {}).get("images", [{}])[0].get("url"),
            "preview_url": t.get("preview_url"),
            "score": round(s, 4),
            "popularity": t.get("popularity")
        }
        for s, t in scored
    ]


# ---------------------------------------------------------
# 1. CLASSIFY + SEARCH
# ---------------------------------------------------------
@router.post("/classify_and_search")
def classify_and_search(
    file: UploadFile = File(...),
    language: Optional[str] = "none",
    genres: Optional[List[str]] = None,
    artist_names: Optional[List[str]] = None,
    track_names: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None,
    limit_results: int = 30
):
    genres = genres or []
    artist_names = artist_names or []
    track_names = track_names or []
    keywords = keywords or []

    temp = f"temp_{file.filename}"
    with open(temp, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        ml = run_inference(temp)  # must return keys: mood, valence, arousal, language, language_confidence (if available)
    finally:
        try:
            os.remove(temp)
        except OSError:
            pass

    # detected language (from ML) and confidence
    detected_lang = ml.get("language")  # e.g. "ta" or "en" or None
    detected_conf = ml.get("language_confidence")

    # if the user explicitly sent a language other than "none"/""/"auto", respect it
    # otherwise fall back to detected language
    if language is None or str(language).strip().lower() in ("", "none", "auto"):
        language_used = detected_lang or "none"
        language_source = "detected"
    else:
        language_used = language
        language_source = "user"

    mood = ml.get("mood", "")

    queries = build_queries(mood, language_used, genres, artist_names, track_names, keywords)

    token = get_client_credentials_token()
    if not token:
        raise HTTPException(status_code=500, detail="Spotify token error")

    all_tracks = {}
    for q in queries:
        items = search_tracks(token, q)
        for t in items:
            all_tracks[t["id"]] = t

    results = score_and_sort(all_tracks, mood, language_used, genres, keywords)

    return {
        "mood_detected": mood,
        "valence": ml.get("valence"),
        "arousal": ml.get("arousal"),
        "detected_language": detected_lang,
        "detected_language_confidence": detected_conf,
        "language_used": language_used,
        "language_source": language_source,
        "queries_used": queries,
        "suggested_keywords": SUGGESTED_KEYWORDS,
        "results": results[:limit_results]
    }


# ---------------------------------------------------------
# 2. SEARCH BY MOOD (NO FILE UPLOAD)
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
