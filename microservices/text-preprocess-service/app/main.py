from fastapi import FastAPI
from pydantic import BaseModel
from app.service import preprocess_text


app = FastAPI(title="Text Preprocess Service")


class TextRequest(BaseModel):
    text: str


@app.post("/preprocess")
def preprocess(req: TextRequest):
    cleaned = preprocess_text(req.text)
    return {"text": cleaned}
