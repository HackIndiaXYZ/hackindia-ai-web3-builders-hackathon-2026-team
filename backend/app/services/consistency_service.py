def normalize_name(name: str | None) -> str:
    if not name:
        return ""

    return (
        name.upper()
        .replace(".", "")
        .replace(",", "")
        .replace("-", " ")
        .replace("  ", " ")
        .strip()
    )


def check_identity_consistency(
    bidder_name: str | None,
    gst_name: str | None = None,
    pan_name: str | None = None,
    udyam_name: str | None = None,
) -> dict:

    names = {
        "bidder": bidder_name,
        "GST": gst_name,
        "PAN": pan_name,
        "Udyam": udyam_name,
    }

    normalized = {
        source: normalize_name(name)
        for source, name in names.items()
        if name
    }

    if not normalized:
        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "message": "No identity information available for comparison.",
            "matched_sources": [],
            "mismatched_sources": []
        }

    unique_names = set(normalized.values())

    if len(unique_names) == 1:
        return {
            "status": "MATCH",
            "confidence": 0.98,
            "message": "Bidder identity is consistent across the available records.",
            "matched_sources": list(normalized.keys()),
            "mismatched_sources": []
        }

    reference_name = normalized.get("bidder")

    mismatched_sources = []

    if reference_name:
        for source, name in normalized.items():
            if source != "bidder" and name != reference_name:
                mismatched_sources.append(source)

    return {
        "status": "MISMATCH",
        "confidence": 0.95,
        "message": "Bidder identity differs across one or more verification records.",
        "matched_sources": [
            source
            for source, name in normalized.items()
            if source not in mismatched_sources
        ],
        "mismatched_sources": mismatched_sources
    }