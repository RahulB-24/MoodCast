import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
import joblib
from tqdm import tqdm
from extract_features import extract_librosa_features

AUDIO_DIR = "../DEAM/DEAM_audio/MEMD_audio/"
ANNOT1 = "../DEAM/DEAM_Annotations/annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
ANNOT2 = "../DEAM/DEAM_Annotations/annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_2000_2058.csv"

print("\nLoading annotations...")
df1 = pd.read_csv(ANNOT1)
df2 = pd.read_csv(ANNOT2)

df = pd.concat([df1, df2], ignore_index=True)
df.columns = [c.strip() for c in df.columns]
df["song_id"] = df["song_id"].astype(str)
print("Annotation count:", len(df))

X = []
Y_val = []
Y_ar = []
ids = []

print("\nExtracting librosa features from audio files...")
for fname in tqdm(os.listdir(AUDIO_DIR)):
    if not fname.lower().endswith((".mp3", ".wav", ".m4a", ".mp4")):
        continue

    song_id = os.path.splitext(fname)[0]

    row = df[df["song_id"] == song_id]
    if row.empty:
        continue

    path = os.path.join(AUDIO_DIR, fname)

    try:
        feat = extract_librosa_features(path)
    except:
        print("Error reading:", fname)
        continue

    X.append(feat)
    Y_val.append(float(row["valence_mean"].iloc[0]))
    Y_ar.append(float(row["arousal_mean"].iloc[0]))
    ids.append(song_id)

X = np.array(X)
Y_val = np.array(Y_val)
Y_ar = np.array(Y_ar)

print("\nFinal dataset shape:", X.shape)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "../models/scaler.pkl")

print("\nTraining valence model...")
Xt, Xv, yt, yv = train_test_split(X_scaled, Y_val, test_size=0.2, random_state=42)
model_val = RandomForestRegressor(n_estimators=400, n_jobs=-1, random_state=42)
model_val.fit(Xt, yt)
print("Valence MAE:", mean_absolute_error(yv, model_val.predict(Xv)))

print("\nTraining arousal model...")
Xt, Xv, yt, yv = train_test_split(X_scaled, Y_ar, test_size=0.2, random_state=42)
model_ar = RandomForestRegressor(n_estimators=400, n_jobs=-1, random_state=42)
model_ar.fit(Xt, yt)
print("Arousal MAE:", mean_absolute_error(yv, model_ar.predict(Xv)))

joblib.dump(model_val, "../models/valence_model.pkl")
joblib.dump(model_ar, "../models/arousal_model.pkl")

print("\nModels saved in /models folder.")
