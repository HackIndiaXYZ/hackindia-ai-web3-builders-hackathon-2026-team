# backend/app/services/compliance_engine.py


REQUIREMENT_WEIGHTS = {
    "GST": 15,
    "PAN_INCOME_TAX": 10,
    "MSME_UDYAM": 10,
    "STARTUP": 5,
    "OEM": 15,
    "MAKE_IN_INDIA": 10,
    "EPFO": 10,
    "ESIC": 10,
    "BLACKLIST": 10,
    "ATC_DOCUMENT": 5,
    "LAND_BORDER_ELIGIBILITY": 5,
}


def evaluate_requirement(
    requirement_type: str,
    verification_result: dict | None = None,
    mandatory: bool = True
) -> dict:

    weight = REQUIREMENT_WEIGHTS.get(
        requirement_type,
        5
    )

    # Government/API verification
    if verification_result:

        registration_status = verification_result.get(
            "registration_status"
        )

        # Successfully verified
        if registration_status in [
            "ACTIVE",
            "CLEAR"
        ]:
            return {
                "status": "PASS",
                "score": weight,
                "explanation": (
                    f"{requirement_type} verification "
                    "was successful."
                ),
                "evidence": verification_result.get(
                    "evidence"
                ),
                "ai_confidence": (
                    verification_result.get(
                        "confidence",
                        0.0
                    ) * 100
                )
            }

        # Could not verify
        if registration_status in [
            "NOT_FOUND",
            "UNKNOWN"
        ]:
            return {
                "status": (
                    "FAIL"
                    if mandatory
                    else "WARN"
                ),
                "score": 0,
                "explanation": (
                    f"{requirement_type} "
                    "could not be verified."
                ),
                "evidence": verification_result.get(
                    "evidence"
                ),
                "ai_confidence": (
                    verification_result.get(
                        "confidence",
                        0.0
                    ) * 100
                )
            }

    # Document-based verification
    return {
        "status": "WARN",
        "score": 0,
        "explanation": (
            f"{requirement_type} requires "
            "document-based verification "
            "or additional evidence."
        ),
        "evidence": None,
        "ai_confidence": 70.0
    }


def calculate_overall_score(
    results: list[dict]
) -> float:

    if not results:
        return 0.0

    total_score = 0
    total_weight = 0

    for result in results:

        requirement_type = result.get(
            "requirement_type"
        )

        weight = REQUIREMENT_WEIGHTS.get(
            requirement_type,
            5
        )

        total_score += result.get(
            "score",
            0
        )

        total_weight += weight

    if total_weight == 0:
        return 0.0

    score = (
        total_score /
        total_weight
    ) * 100

    return round(score, 2)


def determine_overall_status(
    results: list[dict]
) -> str:

    # Mandatory failure
    for result in results:

        if (
            result.get("status") == "FAIL"
            and result.get(
                "mandatory",
                True
            )
        ):
            return "NON_COMPLIANT"

    # Manual review required
    for result in results:

        if result.get("status") == "WARN":
            return "MANUAL_REVIEW"

    # Everything passed
    return "COMPLIANT"


def determine_risk(
    score: float
) -> str:

    if score >= 90:
        return "LOW"

    if score >= 75:
        return "MEDIUM"

    if score >= 50:
        return "HIGH"

    return "CRITICAL"