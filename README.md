# 🎵 MoodCast  
**AI-powered Mood Classification and Music Discovery**

MoodCast is an intelligent music exploration system that analyzes an audio sample, detects the user's mood using a custom-trained ML model, identifies the language in the audio, and then generates optimized Spotify-style search queries to return high-quality music recommendations.

It combines:
- A FastAPI backend  
- A full ML pipeline (Librosa + RandomForest + Faster-Whisper)  
- A React + Vite frontend with animated, music-themed UI  
- Spotify Search API  
- A scoring engine for ranking and filtering tracks  

---

## 🌟 Features

### 🎧 **AI Mood Classification**
- Upload an audio file; the system extracts features using Librosa.
- A trained RandomForest model predicts **valence** and **arousal**.
- Predictions are mapped to discrete moods like:
  - *happy energetic*  
  - *sad calm*  
  - *neutral*  
  - *melancholic*  
  and more.

### 🗣️ **Language Detection**
- Faster-Whisper detects the primary spoken or sung language.
- Detected language influences Spotify search queries.

### 🔍 **Music Search Pipeline**
Supports:
1. **Classify + Search** (upload audio → get songs instantly)  
2. **Search by Mood Only** (keywords, artists, mood, no audio)

Query generation uses:
- mood  
- language  
- genres  
- keywords  
- artist names  
- track names  

### 🎼 **Scoring Engine**
Tracks are ranked based on:
- mood matching  
- keyword matching  
- language-based bias  
- track or artist text relevance  
- Spotify popularity  

### 🖥️ **Modern React Frontend (Vite)**
- Soft gradient UI  
- Animated logo (Coral + Electric Blue theme)  
- Music animations:
  - Folder → folder-music-note transition  
  - Rotating vinyl during search  
- Pages:
  - Home  
  - Detect Mood  
  - Search by Mood  
  - Explore  
  - About  

### 🌐 **YouTube Integration**
Clicking a track opens:  
https://www.youtube.com/results?search_query=<track+name>

### ❤️ **About Page**
Includes:
- Project details  
- Developer info  
- Skills, experience, achievements  
- GitHub, LinkedIn, Email links  
- Source code link  

---

## 🧠 Tech Stack

### **Backend**
- Python  
- FastAPI  
- Librosa  
- RandomForest Regressor  
- Scikit-Learn  
- Faster-Whisper  
- Requests  
- Uvicorn  

### **Frontend**
- React (Vite)  
- CSS Modules + Global Styles  
- Framer Motion  
- React Icons  

### **AI / ML**
- Librosa: feature extraction  
- RandomForest: mood regression  
- Faster-Whisper: language detection  
- Custom mapping: valence + arousal → mood  

### **Other**
- Spotify Web API  
- Axios  
- YouTube Redirect  

---

# 📁 Project Structure
```bash
Moodcast/
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── mood_routes.py
│   │   ├── spotify_auth_routes.py
│   │   ├── spotify_search_routes.py
│   │   ├── spotify_recommend_v3_routes.py
│   ├── utils/
│   │   ├── inference.py
│   │   ├── language_detection.py
│   │   ├── spotify_client.py
│   │   ├── spotify_audio_features.py
│   │   ├── mood_ranker.py
│   ├── training/
│   ├── models/
│   ├── DEAM/
│   ├── .env
│
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── styles/
│   │   ├── api/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── index.css
│
└── README.md
```


---

# 📡 Backend API Endpoints

### **1. POST /classify**

```json
{
  "valence": 5.4,
  "arousal": 5.8,
  "mood": "happy energetic",
  "language": "ta",
  "language_confidence": 0.76
}
```

### **2. POST /recommend_v3/classify_and_search**

Audio → mood → ranked tracks.

### **3. POST /recommend_v3/search_by_mood**

```json
{
  "mood": "sad calm",
  "language": "ta",
  "keywords": ["lofi"],
  "artist_names": ["Arijit Singh"]
}
```

### **4. GET /search/genres**

Returns Spotify genre seeds.

---

# 🎨 Frontend UI Pages

### **Home**

Branding, navigation.

### **Detect Mood**

Upload audio → ML inference → show mood → discover music.

### **Search by Mood**

Enter mood/language/keywords → ranked tracks.

### **Explore**

Search Spotify directly.

### **About**

Developer profile + project info + links.

---

# 🏗️ Local Development Setup

## **1. Clone the Repo**

```bash
git clone https://github.com/RahulB-24/MoodCast
cd Moodcast
```

## **2. Backend Setup**

```bash
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
pip install -r requirements.txt
```

### Add `.env`:

```ini
SPOTIFY_CLIENT_ID=xxxx
SPOTIFY_CLIENT_SECRET=xxxx
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
SPOTIFY_USER_TOKEN_PATH=backend/utils/user_token.json
HF_HOME=~/.cache/huggingface
```

### Run Backend

```bash
uvicorn backend.app:app --reload
```

## **3. Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

Visit:

```
http://localhost:5173
```

---

# 🐳 Docker Setup

## **Backend Dockerfile**

```dockerfile
FROM python:3.11-slim-buster
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/
COPY models/ ./models/
COPY DEAM/ ./DEAM/
ENV HF_HOME=/root/.cache/huggingface
EXPOSE 8000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port",  "8000"]
```

## **Frontend Dockerfile**

```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
RUN npm run build

FROM nginx:alpine
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## **docker-compose.yml**

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
      SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
      SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
      SPOTIFY_REDIRECT_URI=${SPOTIFY_REDIRECT_URI}
      SPOTIFY_USER_TOKEN_PATH=/app/backend/utils/user_token.json
      HF_HOME=/root/.cache/huggingface
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
      args:
        VITE_BACKEND_URL=${VITE_BACKEND_URL}
    container_name: moodcast-frontend
    ports:
      - "5173:80"
    restart: unless-stopped
```

---

# 🚀 Production Deployment

## **.env**

```ini
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://<public-ip>:8000/auth/callback
VITE_BACKEND_URL=http://<public-ip>:8000
```

## **Build and Run**

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

Frontend:
http://<public-ip>:5173
Backend:
http://<public-ip>:8000

---

# 👤 Author

**Rahul Balachandar**
AI/ML Engineer and Full-Stack Developer

Email: [rahulbalachandar24@gmail.com](mailto:rahulbalachandar24@gmail.com)
GitHub: [https://github.com/RahulB-24](https://github.com/RahulB-24)
LinkedIn: [https://linkedin.com/in/](https://linkedin.com/in/)

---

# 📄 License

The MoodCast project is released under the MIT License.

---

# ⭐ Contribute

Issues and PRs welcome.

🎵 **MoodCast**
AI. Music. Mood. Discovery.

