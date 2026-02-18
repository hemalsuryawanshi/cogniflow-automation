def calculate_confidence(entities: dict) -> float:
    score = 0.0

    if entities.get("customer_name"):
        score += 0.25
    if entities.get("document_date"):
        score += 0.25
    if entities.get("amount"):
        score += 0.25
    if entities.get("id_number"):
        score += 0.25

    return round(score, 2)
