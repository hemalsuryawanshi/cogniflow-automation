import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

OCR_URL = os.getenv("OCR_URL")
PREPROCESS_URL = os.getenv("PREPROCESS_URL")
EXTRACT_URL = os.getenv("EXTRACT_URL")
CONFIDENCE_URL = os.getenv("CONFIDENCE_URL")

# Default to SQLite if DATABASE_URL not set
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cogniflow.db"
)
