from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    customer_name = Column(String, nullable=True)
    document_date = Column(String, nullable=True)
    amount = Column(String, nullable=True)
    id_number = Column(String, nullable=True)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
