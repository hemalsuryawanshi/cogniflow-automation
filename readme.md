

Steps to Run:

1. Create virtual environment
   python -m venv venv

2. Activate venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Run project
   uvicorn app.main:app --reload
# Cogniflow Automation – AI Microservices Backend

This project contains AI-based microservices for:

- OCR (Text extraction from Image / PDF / DOCX)
- Text Preprocessing
- Entity Extraction
- Confidence Scoring
- API Gateway

A

#  HOW TO RUN 

Each service must be run in its own terminal.

---

## 1️ OCR Service

```bash
cd microservices/ocr-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Runs on:
```
http://localhost:8001/docs
```

---

## 2️ Text Preprocess Service

```bash
cd microservices/text-preprocess-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

Runs on:
```
http://localhost:8002/docs
```

---

## 3️ Extraction Service

```bash
cd microservices/extraction-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload --port 8006
```

Runs on:
```
http://localhost:8006/docs
```

---

## 4️ Confidence Service

```bash
cd microservices/confidence-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8007
```

Runs on:
```
http://localhost:8007/docs
```

---

## 5️ Gateway Service

```bash
cd gateway
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Runs on:
```
http://localhost:8000/docs
```

---

#  API Endpoints (Gateway)

Base URL:
```
http://localhost:8000
```

### OCR
POST `/ocr`
- Upload file (PDF / Image / DOCX)

### Preprocess
POST `/preprocess`
- Body:
```
{
  "text": "sample text"
}
```

### Extract
POST `/extract`
- Body:
```
{
  "text": "sample text"
}
```

### Confidence
POST `/confidence`
- Body:
```
{
  "extracted_data": {...}
}
```

---

# ⚠ Important Notes

- OCR requires EasyOCR and Torch (heavy libraries).
- Extraction requires spaCy model `en_core_web_sm`.
- All services must be running for gateway to work properly.

---


