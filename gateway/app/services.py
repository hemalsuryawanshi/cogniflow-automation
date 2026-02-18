import requests
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.db import SessionLocal
from app.models import Document
from app.config import OCR_URL, PREPROCESS_URL, EXTRACT_URL, CONFIDENCE_URL


REQUEST_TIMEOUT = 180  # seconds


# ---------------- CREATE ----------------
def process_file(file: UploadFile):

    db = SessionLocal()

    try:
        file.file.seek(0)

        files = {
            "file": (file.filename, file.file, file.content_type)
        }

        # OCR
        ocr_res = requests.post(OCR_URL, files=files, timeout=REQUEST_TIMEOUT)
        if ocr_res.status_code != 200:
            raise HTTPException(status_code=502, detail="OCR service failed")

        raw_text = ocr_res.json().get("raw_text")
        if not raw_text:
            raise HTTPException(status_code=500, detail="OCR returned empty text")

        # PREPROCESS
        prep_res = requests.post(
            PREPROCESS_URL,
            json={"text": raw_text},
            timeout=REQUEST_TIMEOUT
        )
        if prep_res.status_code != 200:
            raise HTTPException(status_code=502, detail="Preprocess service failed")

        clean_text = prep_res.json().get("text")

        # EXTRACT
        extract_res = requests.post(
            EXTRACT_URL,
            json={"text": clean_text},
            timeout=REQUEST_TIMEOUT
        )
        if extract_res.status_code != 200:
            raise HTTPException(status_code=502, detail="Extraction service failed")

        entities = extract_res.json().get("entities", {})

        # CONFIDENCE
        conf_res = requests.post(
            CONFIDENCE_URL,
            json={"entities": entities},
            timeout=REQUEST_TIMEOUT
        )
        if conf_res.status_code != 200:
            raise HTTPException(status_code=502, detail="Confidence service failed")

        confidence = conf_res.json().get("confidence")

        # SAVE
        new_doc = Document(
            file_name=file.filename,
            customer_name=entities.get("customer_name"),
            document_date=entities.get("document_date"),
            amount=entities.get("amount"),
            id_number=entities.get("id_number"),
            confidence=confidence,
            created_at=datetime.utcnow()
        )

        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        return {
            "entities": entities,
            "confidence": confidence
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


# ---------------- READ ALL ----------------
def get_all_documents():
    db = SessionLocal()
    try:
        return db.query(Document).all()
    finally:
        db.close()


# ---------------- READ ONE ----------------
def get_document(doc_id: int):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == doc_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    finally:
        db.close()


# ---------------- UPDATE ----------------
def update_document(doc_id: int, update_data):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(document, key, value)

        db.commit()
        db.refresh(document)

        return document

    finally:
        db.close()


# ---------------- DELETE ----------------
def delete_document(doc_id: int):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        db.delete(document)
        db.commit()

        return {"message": "Document deleted successfully"}

    finally:
        db.close()
