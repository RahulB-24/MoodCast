from faster_whisper import WhisperModel

# Load model once
model = WhisperModel("small", device="cpu", compute_type="int8")

def detect_language(audio_path: str):
    """
    Detects language using faster-whisper automatic language detection.
    """
    segments, info = model.transcribe(audio_path)

    # info.language = "en", "hi", "ta", etc.
    # info.language_probability = float
    return info.language, info.language_probability
