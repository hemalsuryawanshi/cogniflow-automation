from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------- RESPONSE MODEL ----------------
class DocumentResponse(BaseModel):
    id: int
    file_name: str
    customer_name: Optional[str] = None
    document_date: Optional[str] = None
    amount: Optional[str] = None
    id_number: Optional[str] = None
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- UPDATE MODEL ----------------
class DocumentUpdate(BaseModel):
    customer_name: Optional[str] = None
    document_date: Optional[str] = None
    amount: Optional[str] = None
    id_number: Optional[str] = None
