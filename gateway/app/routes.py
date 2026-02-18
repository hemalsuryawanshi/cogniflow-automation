from typing import List
from fastapi import APIRouter, UploadFile, File
from app.services import (
    process_file,
    get_all_documents,
    get_document,
    update_document,
    delete_document
)
from app.schemas import DocumentResponse, DocumentUpdate

router = APIRouter()


# ---------------- CREATE ----------------
@router.post("/process")
def process_document(file: UploadFile = File(...)):
    return process_file(file)


# ---------------- READ ALL ----------------
@router.get("/documents", response_model=List[DocumentResponse])
def documents():
    return get_all_documents()


# ---------------- READ ONE ----------------
@router.get("/documents/{doc_id}", response_model=DocumentResponse)
def document(doc_id: int):
    return get_document(doc_id)


# ---------------- UPDATE ----------------
@router.put("/documents/{doc_id}", response_model=DocumentResponse)
def update(doc_id: int, update_data: DocumentUpdate):
    return update_document(doc_id, update_data)


# ---------------- DELETE ----------------
@router.delete("/documents/{doc_id}")
def delete(doc_id: int):
    return delete_document(doc_id)


# ---------------- HEALTH ----------------
@router.get("/health")
def health():
    return {"status": "Gateway running"}
