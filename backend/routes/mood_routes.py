from fastapi import APIRouter, UploadFile, File
import shutil
import os
import tempfile
import librosa
import soundfile as sf

from backend.utils.inference import run_inference
from backend.utils.language_detection import detect_language

router = APIRouter()

MAX_SECONDS = 10

@router.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...)):
    trimmed_path = None

    # Save upload to /tmp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir="/tmp") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        # Fast duration check (no full decode)
        total_duration = librosa.get_duration(path=temp_path)

        # Choose middle window
        if total_duration <= MAX_SECONDS:
            offset = 0.0
            duration = total_duration
        else:
            offset = max(0.0, (total_duration / 2) - (MAX_SECONDS / 2))
            duration = MAX_SECONDS

        # Load ONLY selected window
        y, sr = librosa.load(
            temp_path,
            sr=22050,
            mono=True,
            offset=offset,
            duration=duration
        )

        # Write trimmed audio
        trimmed_path = temp_path + "_trimmed.wav"
        sf.write(trimmed_path, y, sr)

        # Language (stubbed)
        lang, lang_conf = detect_language(trimmed_path)

        # ML inference
        result = run_inference(trimmed_path)

        result["language"] = lang
        result["language_confidence"] = lang_conf
        result["used_duration_seconds"] = round(duration, 2)
        result["offset_seconds"] = round(offset, 2)

        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if trimmed_path and os.path.exists(trimmed_path):
            os.remove(trimmed_path)
