from fastapi import APIRouter, UploadFile, File
import shutil
import os
import tempfile

from backend.utils.inference import run_inference
from backend.utils.language_detection import detect_language

router = APIRouter()

@router.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...)):
    print(">>> predict_audio called")

    # Always use /tmp on Render
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir="/tmp") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    # Detect language (stubbed)
    lang, lang_conf = detect_language(temp_path)

    # ML inference
    result = run_inference(temp_path)

    # Cleanup
    os.remove(temp_path)

    result["language"] = lang
    result["language_confidence"] = lang_conf

    return result
