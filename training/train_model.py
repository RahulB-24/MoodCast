import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from tqdm import tqdm  # progress bar

FEATURE_DIR = "../DEAM/features/features"

ANNOT1 = "../DEAM/DEAM_Annotations/annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
ANNOT2 = "../DEAM/DEAM_Annotations/annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_2000_2058.csv"


# ------------------------------
# Load annotations
# ------------------------------
print("\nLoading annotation files...")
df1 = pd.read_csv(ANNOT1)
df2 = pd.read_csv(ANNOT2)

df1.columns = [c.strip() for c in df1.columns]
df2.columns = [c.strip() for c in df2.columns]

annotations = pd.concat([df1, df2], ignore_index=True)
annotations["song_id"] = annotations["song_id"].astype(str)

print("Annotations loaded:", len(annotations))


# ------------------------------
# Convert one CSV → single feature vector
# ------------------------------
def load_feature_vector(csv_path):
    df = pd.read_csv(csv_path, header=None)

    # remove header row (contains feature names)
    df = df.iloc[1:]

    parts = df[0].str.split(";", expand=True)

    # remove 'frameTime' column
    parts = parts.drop(columns=[0])

    # convert everything remaining to float
    parts = parts.astype(float)

    # compute mean + std for each feature across all frames
    mean_vals = parts.mean(axis=0).values
    std_vals = parts.std(axis=0).values

    vector = np.concatenate([mean_vals, std_vals])
    return vector


# ------------------------------
# Build dataset with progress bar
# ------------------------------
print("\nBuilding dataset from features...")
X = []
Y_val = []
Y_ar = []
song_ids = []

feature_files = sorted(os.listdir(FEATURE_DIR))

for fname in tqdm(feature_files, desc="Processing feature files"):
    song_id = os.path.splitext(fname)[0]

    ann = annotations[annotations["song_id"] == song_id]
    if ann.empty:
        continue

    feat_path = os.path.join(FEATURE_DIR, fname)

    try:
        vector = load_feature_vector(feat_path)
    except Exception as e:
        print(f"\nError processing {fname}: {e}")
        continue

    X.append(vector)
    Y_val.append(float(ann["valence_mean"].iloc[0]))
    Y_ar.append(float(ann["arousal_mean"].iloc[0]))
    song_ids.append(song_id)

X = np.array(X)
Y_val = np.array(Y_val)
Y_ar = np.array(Y_ar)

print("\nFinal dataset shape:", X.shape)


# ------------------------------
# Train valence model
# ------------------------------
print("\nTraining valence regression model...")
Xt, Xv, yt, yv = train_test_split(X, Y_val, test_size=0.2, random_state=42)

model_val = RandomForestRegressor(
    n_estimators=350, 
    random_state=42,
    n_jobs=-1
)

model_val.fit(Xt, yt)
pred_val = model_val.predict(Xv)
valence_mae = mean_absolute_error(yv, pred_val)

print("Valence MAE:", valence_mae)


# ------------------------------
# Train arousal model
# ------------------------------
print("\nTraining arousal regression model...")
Xt, Xv, yt, yv = train_test_split(X, Y_ar, test_size=0.2, random_state=42)

model_ar = RandomForestRegressor(
    n_estimators=350, 
    random_state=42,
    n_jobs=-1
)

model_ar.fit(Xt, yt)
pred_ar = model_ar.predict(Xv)
arousal_mae = mean_absolute_error(yv, pred_ar)

print("Arousal MAE:", arousal_mae)


# ------------------------------
# Save trained models
# ------------------------------
print("\nSaving trained models...")
joblib.dump(model_val, "../models/valence_model.pkl")
joblib.dump(model_ar, "../models/arousal_model.pkl")

print("\nTraining complete. Models saved in /models folder.")
print("Valence model -> valence_model.pkl")
print("Arousal model -> arousal_model.pkl\n")
