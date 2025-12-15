# MoodCast

**AI-Powered Mood Classification and Music Discovery**

MoodCast is an intelligent music exploration system that analyzes audio samples to detect mood, identify language, and generate personalized music recommendations. The system uses machine learning models for mood prediction and integrates with Spotify's API to deliver relevant track suggestions.

**Core Components:**
- FastAPI backend with ML inference pipeline
- React + Vite frontend with animated UI
- Librosa for audio feature extraction
- RandomForest model for valence and arousal prediction
- Faster Whisper for language detection
- Spotify Search API integration
- Custom scoring engine for track ranking

---

## Live Deployment

The application is publicly accessible worldwide using a **fully free-tier cloud deployment**.

### Frontend
- **Platform**: Vercel
- **URL**: https://mood-cast-xi.vercel.app/
- **Details**:
  - Global CDN with HTTPS by default
  - Always-on (no cold starts)
  - Static React + Vite build

### Backend
- **Platform**: Render (Free Tier)
- **API Base URL**: https://moodcast-backend-qsjk.onrender.com
- **Details**:
  - Dockerized FastAPI service
  - Hosts ML inference, audio processing, and Spotify integration
  - Free-tier instances **sleep after inactivity**
  - First request after idle may take ~30–60 seconds (cold start)

> The frontend communicates with the backend over HTTPS. No user authentication is required.

---
<img width="3199" height="1837" alt="Image" src="https://github.com/user-attachments/assets/a8a660de-82dd-435c-a5df-2265294ed04c" />

## Features

### Mood Classification

Users upload an audio file, and MoodCast processes **only a 10-second segment from the middle of the track** to ensure fast and reliable inference on free-tier infrastructure.

Librosa extracts acoustic features, and a trained RandomForest model predicts valence and arousal values, which are then mapped to discrete mood categories such as:
- happy energetic
- sad calm
- neutral
- melancholic

### Language Detection

Faster Whisper (tiny model) analyzes the trimmed audio segment to detect the primary language. The detected language is used to refine Spotify search queries for more relevant track results.

### Music Search Pipeline

The system supports two search modes:

1. **Classify and Search** Upload audio to automatically detect mood and receive song recommendations  
2. **Search by Mood** Manually specify mood, language, genres, keywords, artist names, or track names

### Track Scoring and Ranking

Results are ranked using a custom scoring engine that considers:
- Mood matching using valence and arousal
- Keyword relevance
- Language preference
- Track and artist text similarity
- Spotify popularity metrics

### Frontend Interface

Built with React and Vite, featuring:
- Gradient themed UI with coral and electric blue
- Animated logo and transitions
- Music themed animations like rotating vinyl and folder to music note transitions
- Navigation pages including Home, Detect Mood, Search by Mood, Explore, About

### External Integration

Clicking a track redirects to YouTube search results:

```
https://www.youtube.com/results?search_query=<track+name>
```

---
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/f62b97ba-7ca9-4db7-90c5-fd70d52793a2" width="500"></td>
    <td><img src="https://github.com/user-attachments/assets/f13040ab-aece-4c54-890d-74178372590d" width="500"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/7f2b0403-02db-4780-8f7a-fcd708aef4e1" width="500"></td>
    <td><img src="https://github.com/user-attachments/assets/a9070208-c7a0-469d-a18b-9ff07ecda1ee" width="500"></td>
  </tr>
</table>

## Tech Stack

### Backend
- Python, FastAPI, Uvicorn
- Librosa for audio feature extraction
- Scikit Learn for RandomForest regression
- Faster Whisper for language detection
- Requests for API calls
- Deployed on Render (Dockerized)

### Frontend
- React with Vite
- CSS Modules with global styles
- Framer Motion for animations
- React Icons
- Deployed on Vercel

### Machine Learning
- Librosa for MFCCs, spectral features, tempo
- RandomForest for valence and arousal prediction
- Custom mood mapping rules
- Faster Whisper for multilingual transcription

### APIs
- Spotify Web API for search and audio features
- YouTube for external redirect

<img width="2114" height="1022" alt="Image" src="https://github.com/user-attachments/assets/1fd37c22-5ea4-4d77-a531-5bf2cbd3ca92" />

---

## Project Structure

```
Moodcast/
├── docker-compose.yml
├── requirements.txt
├── training/
├── models/
├── DEAM/
│
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   ├── routes/
│   │   ├── mood_routes.py
│   │   ├── spotify_auth_routes.py
│   │   ├── spotify_search_routes.py
│   │   └── spotify_recommend_v3_routes.py
│   ├── utils/
│   │   ├── inference.py
│   │   ├── language_detection.py
│   │   ├── spotify_client.py
│   │   ├── spotify_audio_features.py
│   │   └── mood_ranker.py
│   ├── training/
│   ├── models/
│   ├── DEAM/
│   └── .env
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── styles/
│   │   ├── api/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   └── nginx.conf
│
└── README.md
```

---

## API Endpoints

### POST /classify

Accepts an audio file and returns mood classification results.

**Example Response**

```json
{
  "valence": 5.4,
  "arousal": 5.8,
  "mood": "happy energetic",
  "language": "ta",
  "language_confidence": 0.76
}
```

### `POST /recommend_v3/classify_and_search`

Classifies uploaded audio and returns ranked Spotify tracks based on detected mood.

### `POST /recommend_v3/search_by_mood`

Searches for tracks based on specified parameters without audio upload.

**Request Body:**

```json
{
  "mood": "sad calm",
  "language": "ta",
  "keywords": ["lofi"],
  "artist_names": ["Arijit Singh"]
}
```

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/RahulB-24/MoodCast
cd Moodcast
```

### 2. Backend Setup

Create and activate a virtual environment:

```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
SPOTIFY_USER_TOKEN_PATH=backend/utils/user_token.json
HF_HOME=~/.cache/huggingface
```

Start the backend server:

```bash
uvicorn backend.app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## Cloud Deployment

### Backend Deployment (Render)

The backend is containerized using Docker and deployed on **Render's free tier**.

**Dockerfile:**

```dockerfile
FROM python:3.11-slim-buster
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY models/ ./models/
COPY training/ ./training/

ENV HF_HOME=/tmp/huggingface

EXPOSE 10000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "10000"]
```

**Deployment Steps:**
1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Configure environment variables (Spotify credentials)
5. Render automatically builds and deploys from the Dockerfile

**Notes:**
- ML models are bundled directly into the Docker image
- Free-tier instances sleep after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds (cold start)

### Frontend Deployment (Vercel)

The frontend is deployed directly from GitHub to **Vercel**.

**Deployment Steps:**
1. Push your frontend code to GitHub
2. Import project in Vercel
3. Configure build settings:
   - Framework Preset: Vite
   - Root Directory: `frontend`
4. Add environment variable:
   ```
   VITE_BACKEND_URL=https://moodcast-backend-qsjk.onrender.com
   ```
5. Deploy

**Features:**
- Automatic deployments on git push
- Global CDN distribution
- HTTPS enabled by default
- Zero cold starts (always available)

---

## Docker Compose (Local Development)

For local development with Docker:

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: moodcast-backend
    volumes:
      - ./models:/app/models
      - ./DEAM:/app/DEAM
      - ./backend/utils/user_token.json:/app/backend/utils/user_token.json
    ports:
      - "8000:8000"
    environment:
      SPOTIFY_CLIENT_ID: ${SPOTIFY_CLIENT_ID}
      SPOTIFY_CLIENT_SECRET: ${SPOTIFY_CLIENT_SECRET}
      SPOTIFY_REDIRECT_URI: ${SPOTIFY_REDIRECT_URI}
      SPOTIFY_USER_TOKEN_PATH: /app/backend/utils/user_token.json
      HF_HOME: /root/.cache/huggingface
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
      args:
        VITE_BACKEND_URL: ${VITE_BACKEND_URL}
    container_name: moodcast-frontend
    ports:
      - "5173:80"
    restart: unless-stopped
```

### Running with Docker Compose

Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/auth/callback
VITE_BACKEND_URL=http://localhost:8000
```

Build and start containers:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

Access the application:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

---

## Author

**Rahul Balachandar**  
AI/ML Engineer and Full-Stack Developer

- Email: [rahulbalachandar24@gmail.com](mailto:rahulbalachandar24@gmail.com)
- GitHub: [github.com/RahulB-24](https://github.com/RahulB-24)
- LinkedIn: [linkedin.com/in/rahulbalachandar](https://linkedin.com/in/rahulbalachandar)

---

## License

This project is licensed under the MIT License.

---

## Contributing

Issues and pull requests are welcome. Feel free to contribute improvements or report bugs.