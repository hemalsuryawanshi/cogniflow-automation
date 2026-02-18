
import re

def preprocess_text(text: str):
    if not text:
        return ""

    # lowercase only
    text = text.lower()

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    # DO NOT remove punctuation needed for extraction
    return text.strip()
