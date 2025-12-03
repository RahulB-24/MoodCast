import joblib
import numpy as np
from extract_features import extract_librosa_features

model_val = joblib.load("../models/valence_model.pkl")
model_ar = joblib.load("../models/arousal_model.pkl")
scaler = joblib.load("../models/scaler.pkl")
def map_mood(v, a):
    # Hard boundaries for strong emotions
    if v > 5.4 and a > 5.4:
        return "happy energetic"
    if v > 5.4 and a < 5.0:
        return "relaxed positive"
    if v < 4.7 and a > 5.4:
        return "tense or angry"
    if v < 4.7 and a < 5.0:
        return "sad calm"

    # Soft boundaries: neutral leaning moods
    if v > 5.15 and a > 5.15:
        return "neutral-happy energetic"
    if v > 5.15 and a < 5.15:
        return "neutral-happy"
    if v < 5.0 and a > 5.15:
        return "neutral-tense"
    if v < 5.0 and a < 5.15:
        return "neutral-sad"

    # Otherwise
    return "neutral"




def predict_audio(path):
    feats = extract_librosa_features(path)
    feats = feats.reshape(1, -1)
    feats = scaler.transform(feats)

    v = model_val.predict(feats)[0]
    a = model_ar.predict(feats)[0]

    mood = map_mood(v, a)
    return {
        "valence": float(v),
        "arousal": float(a),
        "mood": mood
    }

if __name__ == "__main__":
    import sys
    print(predict_audio(sys.argv[1]))
