from fastapi import FastAPI

from backend.routes.mood_routes import router as mood_router
from backend.routes.spotify_auth_routes import router as spotify_auth_router
from backend.routes.spotify_search_routes import router as spotify_search_router
from backend.routes.spotify_recommend_v3_routes import router as rec_v3_router

app = FastAPI()

app.include_router(mood_router)
app.include_router(spotify_auth_router)
app.include_router(spotify_search_router)
app.include_router(rec_v3_router)

@app.get("/")
def root():
    return {"message": "MoodCast backend is running"}
