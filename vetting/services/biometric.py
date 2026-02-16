def validate_face(scan_data):
    """
    Expected payload:
    {
        "confidence": 0.87
    }
    """

    confidence = scan_data.get("confidence", 0)

    # Telecom-grade threshold
    if confidence >= 0.85:
        return True

    return False



def validate_id(scan_data):
    """
    Expected payload:
    {
        "ocr_match_score": 0.92,
        "id_number_match": True
    }
    """

    score = scan_data.get("ocr_match_score", 0)
    id_match = scan_data.get("id_number_match", False)

    if score >= 0.85 and id_match:
        return True

    return False

