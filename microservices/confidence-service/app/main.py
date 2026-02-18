from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.service import calculate_confidence

app = FastAPI(title="Confidence Scoring Service")

class Entities(BaseModel):
    customer_name: Optional[str] = None
    document_date: Optional[str] = None
    amount: Optional[str] = None
    id_number: Optional[str] = None

class ConfidenceRequest(BaseModel):
    entities: Entities

@app.post("/confidence")
def confidence_api(req: ConfidenceRequest):
    score = calculate_confidence(req.entities.dict())
    return {"confidence": score}
