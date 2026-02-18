import os
import uuid
import re
from PIL import Image
import pdfplumber
import docx

# -------- SAFE EASYOCR LOAD --------
try:
    import easyocr
    reader = easyocr.Reader(["en"], gpu=False)
except Exception as e:
    reader = None
    print("EasyOCR failed to load:", e)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",").replace(" .", ".")
    return text.strip()


def extract_text_from_image(file_path: str) -> str:
    """
    OCR microservice entry function.
    Accepts file path and returns extracted raw text.
    """

    if not os.path.exists(file_path):
        return "FILE_NOT_FOUND"

    filename = file_path.lower()
    temp_path = f"temp_{uuid.uuid4()}_{os.path.basename(filename)}"

    with open(file_path, "rb") as src, open(temp_path, "wb") as dst:
        dst.write(src.read())

    text = ""

    try:
        # ================= PDF =================
        if filename.endswith(".pdf"):
            with pdfplumber.open(temp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "

            # OCR fallback (scanned PDF)
            if not text.strip() and reader:
                with pdfplumber.open(temp_path) as pdf:
                    for page in pdf.pages:
                        img = page.to_image(resolution=200).original
                        result = reader.readtext(img)
                        text += " ".join([r[1] for r in result]) + " "

        # ================= IMAGE =================
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            if not reader:
                return "OCR_ENGINE_NOT_AVAILABLE"
            result = reader.readtext(temp_path)
            text = " ".join([r[1] for r in result])

        # ================= DOCX =================
        elif filename.endswith(".docx"):
            document = docx.Document(temp_path)
            text = " ".join([p.text for p in document.paragraphs])

        else:
            return "UNSUPPORTED_FILE_TYPE"

        return clean_text(text) if text else "NO_TEXT_FOUND"

    except Exception as e:
        return f"OCR_FAILED: {str(e)}"

    finally:
        try:
            os.remove(temp_path)
        except:
            pass
