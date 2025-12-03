from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.utils.inference import run_inference
from backend.utils.language_detection import detect_language

router = APIRouter()

@router.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...)):
    # save temporary file
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Detect language
    lang, lang_conf = detect_language(temp_path)

    # 2. Run ML model
    result = run_inference(temp_path)

    # remove temp file
    os.remove(temp_path)

    # add language into result
    result["language"] = lang
    result["language_confidence"] = lang_conf

    return result
