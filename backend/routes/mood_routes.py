from fastapi import APIRouter, UploadFile, File
import shutil
import os
import tempfile
import librosa

from backend.utils.inference import run_inference
from backend.utils.language_detection import detect_language

router = APIRouter()

MAX_SECONDS = 10

@router.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...)):
    # Save upload to /tmp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir="/tmp") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        # Load ONLY first 10 seconds
        y, sr = librosa.load(
            temp_path,
            sr=22050,
            mono=True,
            duration=MAX_SECONDS
        )

        # Save trimmed audio to temp file
        trimmed_path = temp_path + "_trimmed.wav"
        librosa.output.write_wav(trimmed_path, y, sr)

        # Language (stubbed)
        lang, lang_conf = detect_language(trimmed_path)

        # Inference on trimmed audio
        result = run_inference(trimmed_path)

        result["language"] = lang
        result["language_confidence"] = lang_conf
        result["used_duration_seconds"] = MAX_SECONDS

        return result

    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(trimmed_path):
            os.remove(trimmed_path)
