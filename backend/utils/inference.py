from training.extract_features import extract_librosa_features  
from backend.utils.language_detection import detect_language
import joblib
import numpy as np

model_val = joblib.load("models/valence_model.pkl")
model_ar = joblib.load("models/arousal_model.pkl")
scaler = joblib.load("models/scaler.pkl")

def map_mood(v, a):
    if v > 5.4 and a > 5.35:
        return "happy energetic"
    if v > 5.4 and a < 5.1:
        return "relaxed positive"
    if v < 4.7 and a > 5.35:
        return "tense or angry"
    if v < 4.7 and a < 5.1:
        return "sad calm"

    if v > 5.15 and a > 5.15:
        return "neutral-happy energetic"
    if v > 5.15 and a < 5.15:
        return "neutral-happy"
    if v < 5.0 and a > 5.15:
        return "neutral-tense"
    if v < 5.0 and a < 5.15:
        return "neutral-sad"

    return "neutral"


def run_inference(audio_path: str):
    # features
    feats = extract_librosa_features(audio_path)
    feats = feats.reshape(1, -1)
    feats = scaler.transform(feats)

    val = float(model_val.predict(feats)[0])
    aro = float(model_ar.predict(feats)[0])
    mood = map_mood(val, aro)

    # detect language
    lang, lang_conf = detect_language(audio_path)

    return {
        "valence": val,
        "arousal": aro,
        "mood": mood,
        "language": lang,                     # important
        "language_confidence": lang_conf      # important
    }
