# Cogniflow Gateway Service

This is the API Gateway for Cogniflow Automation.

## Responsibilities

- Accept document upload
- Call OCR microservice
- Call Text Preprocess microservice
- Call Extraction microservice
- Call Confidence microservice
- Save results to database
- Provide document history APIs

## Endpoints

### POST /process
Upload document and process it.

### GET /documents
Get all processed documents.

### GET /documents/{doc_id}
Get single document.

### GET /health
Check service status.

## Run Locally

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
