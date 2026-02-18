from fastapi import FastAPI
from pydantic import BaseModel
from app.service import extract_entities

app = FastAPI(title="Extraction / NER Service")

class ExtractionRequest(BaseModel):
    text: str

@app.post("/extract")
def extract_api(req: ExtractionRequest):
    return {"entities": extract_entities(req.text)}
