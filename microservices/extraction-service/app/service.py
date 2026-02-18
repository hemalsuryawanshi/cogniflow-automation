import re
import spacy

nlp = spacy.load("en_core_web_sm")

BAD_PERSON_WORDS = [
    "store", "phone", "invoice", "gst", "total",
    "amount", "date", "payment", "manager", "scan",
    "electronics", "tax"
]


def extract_entities(text: str):

    if not text:
        return {
            "customer_name": None,
            "document_date": None,
            "amount": None,
            "id_number": None
        }

    original_text = text
    text_lower = text.lower()

    entities = {
        "customer_name": None,
        "document_date": None,
        "amount": None,
        "id_number": None
    }

    # ---------------- CUSTOMER NAME ----------------

    name_match = re.search(
        r"customer\s*name\s*[:\-]?\s*([a-z]{2,}\s+[a-z]{2,})",
        text_lower
    )

    if name_match:
        candidate = name_match.group(1).strip()

        STOP_WORDS = [
            "item", "description", "address",
            "phone", "city", "invoice", "total"
        ]

        words = candidate.split()
        cleaned = []

        for w in words:
            if w in STOP_WORDS:
                break
            cleaned.append(w)

        entities["customer_name"] = " ".join(cleaned)

    else:
        name_match_alt = re.search(
            r"cust\w*\s*name\s*[:\-]?\s*([a-z]{2,}\s+[a-z]{2,})",
            text_lower
        )

        if name_match_alt:
            entities["customer_name"] = name_match_alt.group(1).strip()

        else:
            doc = nlp(original_text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    candidate = ent.text.lower().strip()
                    if not any(bad in candidate for bad in BAD_PERSON_WORDS):
                        entities["customer_name"] = candidate
                        break

    # ---------------- DATE (Improved for OCR) ----------------
    date_patterns = [
        r"\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}",            # 18/02/2026 or 18-02-2026
        r"\d{4}[\/\-]\d{2}[\/\-]\d{2}",                # 2026-02-18
        r"\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4}",        # 18 Feb 2026 / 18-Feb-2026
        r"\d{1,2}[A-Za-z]{3}\d{4}"                     # 18Feb2026
    ]

    for pattern in date_patterns:
        match = re.search(pattern, original_text, re.I)
        if match:
            entities["document_date"] = match.group().lower()
            break

    # ---------------- INVOICE NUMBER ----------------
    id_patterns = [
        r"invoice\s*(number|no)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        r"\binv[-\s:]?([A-Za-z0-9\-]+)"
    ]

    for pattern in id_patterns:
        match = re.search(pattern, original_text, re.I)
        if match:
            extracted = (
                match.group(2) if len(match.groups()) > 1 else match.group(1)
            ).strip().lower()

            if extracted not in ["invoice", "oice"]:
                entities["id_number"] = extracted
            break

    # ---------------- AMOUNT ----------------
    amount_matches = re.findall(
        r"(grand\s*total|total)[^\d]{0,15}(₹?\s?[\d,]+)",
        original_text,
        re.I
    )

    if amount_matches:
        entities["amount"] = amount_matches[-1][1].replace(",", "").strip()

    return entities

