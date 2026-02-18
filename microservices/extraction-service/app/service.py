import re
import spacy

nlp = spacy.load("en_core_web_sm")


def detect_document_type(text: str) -> str:
    text_lower = text.lower()

    if "income tax department" in text_lower or re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
        return "pan"

    elif "aadhaar" in text_lower or "uidai" in text_lower or re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text):
        return "aadhaar"

    elif "passport" in text_lower or re.search(r"\b[A-Z][0-9]{7}\b", text):
        return "passport"

    elif "driving licence" in text_lower or "driving license" in text_lower:
        return "driving_license"

    elif "invoice" in text_lower or "bill" in text_lower:
        return "invoice"

    return "unknown"


def extract_entities(text: str):

    if not text:
        return {}

    doc_type = detect_document_type(text)
    text_lower = text.lower()

    entities = {
        "document_type": doc_type,
        "customer_name": None,
        "father_name": None,
        "document_date": None,
        "dob": None,
        "amount": None,
        "id_number": None,
        "aadhaar_number": None,
        "pan_number": None,
        "passport_number": None,
        "dl_number": None
    }

    # ---------------- NAME (Common using spaCy) ----------------
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["customer_name"] = ent.text.strip()
            break

    # ---------------- DATE / DOB ----------------
    date_patterns = [
        r"\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}",
        r"\d{4}[\/\-]\d{2}[\/\-]\d{2}",
        r"\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4}"
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            entities["document_date"] = match.group()
            entities["dob"] = match.group()
            break

    # ---------------- PAN ----------------
    pan_match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
    if pan_match:
        entities["pan_number"] = pan_match.group()
        entities["id_number"] = pan_match.group()

    # ---------------- AADHAAR ----------------
    aadhaar_match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
    if aadhaar_match:
        entities["aadhaar_number"] = aadhaar_match.group()
        entities["id_number"] = aadhaar_match.group()

    # ---------------- PASSPORT ----------------
    passport_match = re.search(r"\b[A-Z][0-9]{7}\b", text)
    if passport_match:
        entities["passport_number"] = passport_match.group()
        entities["id_number"] = passport_match.group()

    # ---------------- DRIVING LICENSE ----------------
    dl_match = re.search(r"\b[A-Z]{2}\d{2}\s?\d{11}\b", text)
    if dl_match:
        entities["dl_number"] = dl_match.group()
        entities["id_number"] = dl_match.group()

    # ---------------- INVOICE NUMBER ----------------
    invoice_match = re.search(
        r"invoice\s*(number|no)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        text,
        re.I
    )
    if invoice_match:
        entities["id_number"] = invoice_match.group(2)

    # ---------------- AMOUNT ----------------
    amount_match = re.findall(
        r"(grand\s*total|total)[^\d]{0,15}(₹?\s?[\d,]+)",
        text,
        re.I
    )

    if amount_match:
        entities["amount"] = amount_match[-1][1].replace(",", "").strip()

    # ---------------- FATHER NAME (PAN Specific) ----------------
    father_match = re.search(
        r"father'?s?\s*name\s*[:\-]?\s*([A-Za-z\s]+)",
        text,
        re.I
    )
    if father_match:
        entities["father_name"] = father_match.group(1).strip()

    return entities
