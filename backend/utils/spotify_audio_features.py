import requests
from backend.utils.spotify_client import refresh_user_token_if_needed

def get_audio_features_user(track_id: str):
    token = refresh_user_token_if_needed()
    if not token:
        # not logged in
        return None, {"error": "no_user_token"}
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return None, {"status": res.status_code, "text": res.text}
    return res.json(), None
