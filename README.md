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
- Faster-Whisper detects the primary spoken/sung language in the audio.
- Language is used to bias search queries (e.g., *tamil sad*, *hindi romantic*, etc.).

### 🔍 **Music Search Pipeline**
MoodCast supports:
1. **Classify + Search** (upload audio → get songs instantly)  
2. **Search by Mood Only** (no audio, user enters mood, keywords, artists, tracks)

Queries are intelligently generated using:
- mood  
- language  
- genres  
- keywords  
- artist names  
- track names  

### 🎼 **Scoring Engine**
Each found track is scored using:
- mood matching  
- keyword matching  
- language keyword  
- track/artist text relevance  
- Spotify popularity score  

Tracks are sorted and returned with preview URLs, images, and metadata.

### 🖥️ **Modern React Frontend (Vite)**
- Soft gradient background  
- Animated logo with warm/cool color theme (Coral + Electric Blue)  
- Music-themed animations:
  - Folder → folder music note transition during upload  
  - Rotating vinyl during search  
- Clean, intuitive pages:
  - Home  
  - Detect Mood  
  - Search by Mood  
  - Explore  
  - About  

### 🌐 **YouTube Integration**
Clicking any track opens a YouTube search:
https://www.youtube.com/results?search_query=<track+name>   

### ❤️ **About Page**
Contains:
- About the project  
- About the developer  
- Experience, skills, achievements  
- GitHub, LinkedIn, Email icons  
- Source Code link  

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
- CSS Modules & Global Styles
- Framer Motion
- React Icons

### **AI / ML**
- Feature extraction: Librosa  
- Regression models: RandomForest  
- Language detection: Faster-Whisper  
- Custom mapping from valence + arousal → mood  

### **Other**
- Spotify Web API  
- Axios  
- YouTube Search Redirect  

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
Upload audio, returns:
```json
{
  "valence": 5.4,
  "arousal": 5.8,
  "mood": "happy energetic",
  "language": "ta",
  "language_confidence": 0.76
}
2. POST /recommend_v3/classify_and_search
Upload audio + optional params → returns full ranked track list.

3. POST /recommend_v3/search_by_mood
Body example:

json
Copy code
{
  "mood": "sad calm",
  "language": "ta",
  "keywords": ["lofi"],
  "artist_names": ["Arijit Singh"]
}
4. GET /search/genres
Returns available genre seeds.

🎨 Frontend UI Pages
Home
Logo, tagline, simple navigation.

Detect Mood
Upload → ML → mood visualization → music discovery button.

Search by Mood
Enter mood, language, keywords → ranked tracks.

Explore
Search Spotify directly.

About
Developer info, experience, skills, achievements, GitHub source code link.

🏗️ Local Development Setup
1. Clone the Repo
bash
Copy code
git clone https://github.com/RahulB-24/MoodCast
cd Moodcast
2. Backend Setup
Create virtual environment:
bash
Copy code
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Add .env:
ini
Copy code
SPOTIFY_CLIENT_ID=xxxx
SPOTIFY_CLIENT_SECRET=xxxx
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
SPOTIFY_USER_TOKEN_PATH=backend/utils/user_token.json
HF_HOME=~/.cache/huggingface
Run backend:
bash
Copy code
uvicorn backend.app:app --reload
3. Frontend Setup
bash
Copy code
cd frontend
npm install
npm run dev
Visit:

arduino
Copy code
http://localhost:5173
🐳 Docker (Will be added next)
A complete Docker section will appear here after we generate:

Backend Dockerfile

Frontend Dockerfile

Nginx reverse proxy config

docker-compose.yml

Production build instructions

☁️ AWS EC2 Deployment (Coming next)
This section will include:

EC2 instance setup

Docker installation

Pull + run containers

Environment variable injection

HTTPS using Caddy or Nginx + Certbot

Domain configuration

👤 Author
Rahul Balachandar
AI/ML Engineer & Full-Stack Developer

Email: rahulbalachandar24@gmail.com

GitHub: https://github.com/RahulB-24

LinkedIn: https://linkedin.com/in/

📄 License
This project is open-source under MIT License.

⭐ Contribute
Feel free to submit issues or PRs to improve MoodCast.

🎵 MoodCast
AI. Music. Mood. Discovery.