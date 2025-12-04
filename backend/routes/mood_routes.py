from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.utils.inference import run_inference
from backend.utils.language_detection import detect_language

router = APIRouter()

@router.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect language
    lang, lang_conf = detect_language(temp_path)

    # ML inference
    result = run_inference(temp_path)

    # Cleanup
    os.remove(temp_path)

    # Attach language info
    result["language"] = lang
    result["language_confidence"] = lang_conf

    return result
