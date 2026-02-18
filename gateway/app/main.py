from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.db import init_db

app = FastAPI(
    title="Cogniflow Gateway",
    version="1.0.0",
    description="Microservice Gateway for OCR, Extraction and Confidence Scoring"
)

# ---------------- CORS Middleware ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Startup Event ----------------
@app.on_event("startup")
def startup_event():
    init_db()

# ---------------- Include Routes ----------------
app.include_router(router)
