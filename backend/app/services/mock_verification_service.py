from datetime import datetime, timezone


def verify_gst(gstin: str):
    if gstin == "27ABCDE1234F1Z5":
        return {
            "source": "GSTN",
            "status": "VERIFIED",
            "entity_name": "ABC Engineering Pvt Ltd",
            "registration_status": "ACTIVE",
            "verified_at": datetime.now(timezone.utc),
            "confidence": 0.98,
            "evidence": "GST registration is active."
        }

    return {
        "source": "GSTN",
        "status": "NOT_VERIFIED",
        "entity_name": None,
        "registration_status": "NOT_FOUND",
        "verified_at": datetime.now(timezone.utc),
        "confidence": 0.50,
        "evidence": "GSTIN was not found in the mock verification database."
    }


def verify_udyam(number: str):
    if number == "UDYAM-MH-18-0012345":
        return {
            "source": "Udyam Registration",
            "status": "VERIFIED",
            "entity_name": "ABC Engineering Pvt Ltd",
            "registration_status": "ACTIVE",
            "verified_at": datetime.now(timezone.utc),
            "confidence": 0.97,
            "evidence": "Udyam registration is active."
        }

    return {
        "source": "Udyam Registration",
        "status": "NOT_VERIFIED",
        "entity_name": None,
        "registration_status": "NOT_FOUND",
        "verified_at": datetime.now(timezone.utc),
        "confidence": 0.50,
        "evidence": "Udyam number was not found in the mock verification database."
    }


def verify_pan(pan: str):
    if pan == "ABCDE1234F":
        return {
            "source": "Income Tax / PAN",
            "status": "VERIFIED",
            "entity_name": "ABC Engineering Pvt Ltd",
            "registration_status": "ACTIVE",
            "verified_at": datetime.now(timezone.utc),
            "confidence": 0.98,
            "evidence": "PAN is valid and active."
        }

    return {
        "source": "Income Tax / PAN",
        "status": "NOT_VERIFIED",
        "entity_name": None,
        "registration_status": "NOT_FOUND",
        "verified_at": datetime.now(timezone.utc),
        "confidence": 0.50,
        "evidence": "PAN was not found in the mock verification database."
    }


def verify_epfo(number: str):
    if number == "EPFO-ABC-001":
        return {
            "source": "EPFO",
            "status": "VERIFIED",
            "entity_name": "ABC Engineering Pvt Ltd",
            "registration_status": "ACTIVE",
            "verified_at": datetime.now(timezone.utc),
            "confidence": 0.95,
            "evidence": "EPFO registration is active."
        }

    return {
        "source": "EPFO",
        "status": "NOT_VERIFIED",
        "entity_name": None,
        "registration_status": "NOT_FOUND",
        "verified_at": datetime.now(timezone.utc),
        "confidence": 0.50,
        "evidence": "EPFO registration was not found in the mock verification database."
    }


def verify_esic(number: str):
    if number == "ESIC-ABC-001":
        return {
            "source": "ESIC",
            "status": "VERIFIED",
            "entity_name": "ABC Engineering Pvt Ltd",
            "registration_status": "ACTIVE",
            "verified_at": datetime.now(timezone.utc),
            "confidence": 0.95,
            "evidence": "ESIC registration is active."
        }

    return {
        "source": "ESIC",
        "status": "NOT_VERIFIED",
        "entity_name": None,
        "registration_status": "NOT_FOUND",
        "verified_at": datetime.now(timezone.utc),
        "confidence": 0.50,
        "evidence": "ESIC registration was not found in the mock verification database."
    }


def verify_blacklist(company: str):
    if company.lower() == "abc engineering pvt ltd":
        return {
            "source": "Blacklisting Database",
            "status": "VERIFIED",
            "entity_name": "ABC Engineering Pvt Ltd",
            "registration_status": "CLEAR",
            "verified_at": datetime.now(timezone.utc),
            "confidence": 0.96,
            "evidence": "No active blacklisting or debarment record found."
        }

    return {
        "source": "Blacklisting Database",
        "status": "NOT_VERIFIED",
        "entity_name": company,
        "registration_status": "UNKNOWN",
        "verified_at": datetime.now(timezone.utc),
        "confidence": 0.50,
        "evidence": "Company was not found in the mock blacklisting database."
    }