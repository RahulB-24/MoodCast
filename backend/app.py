from fastapi import FastAPI
from backend.routes.mood_routes import router as mood_router
from backend.routes.spotify_auth_routes import router as spotify_auth_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MoodCast backend is running"}

app.include_router(mood_router)
app.include_router(spotify_auth_router)
