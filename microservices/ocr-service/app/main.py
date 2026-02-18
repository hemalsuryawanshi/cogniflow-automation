from fastapi import FastAPI, UploadFile, File
from app.service import extract_text_from_image
import uuid
import os

app = FastAPI(title="OCR Microservice")


@app.post("/ocr")
async def ocr_api(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    ext = file.filename.split(".")[-1]
    temp_file = f"temp_{uuid.uuid4()}.{ext}"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # Run OCR
    text = extract_text_from_image(temp_file)

    # Cleanup
    try:
        os.remove(temp_file)
    except:
        pass

    return {
        "raw_text": text,
        "engines": ["easyocr"]
    }
