import os

# Railway automatically provides environment variables
# No need for dotenv in production

#OCR_URL = os.environ.get("OCR_URL")
#PREPROCESS_URL = os.environ.get("PREPROCESS_URL")
#EXTRACT_URL = os.environ.get("EXTRACT_URL")
#CONFIDENCE_URL = os.environ.get("CONFIDENCE_URL")
OCR_URL = "https://generous-passion-production-5ad5.up.railway.app/ocr"
PREPROCESS_URL = "https://remarkable-inspiration-production-017e.up.railway.app/preprocess"
EXTRACT_URL = "https://blissful-flow-production-ba39.up.railway.app/extract"
CONFIDENCE_URL = "https://resilient-playfulness-production-4f84.up.railway.app/confidence"


# Fallback database
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./cogniflow.db"
)

# Debug print (VERY IMPORTANT for checking Railway variables)
print("OCR_URL:", OCR_URL)
print("PREPROCESS_URL:", PREPROCESS_URL)
print("EXTRACT_URL:", EXTRACT_URL)
print("CONFIDENCE_URL:", CONFIDENCE_URL)
