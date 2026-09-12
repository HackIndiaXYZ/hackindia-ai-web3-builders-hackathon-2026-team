from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.mock_gst import MockGST
from app.models.mock_udyam import MockUdyam
from app.models.mock_pan import MockPAN
from app.models.mock_epfo import MockEPFO
from app.models.mock_esic import MockESIC
from app.models.mock_startup import MockStartup
from app.models.mock_nsic import MockNSIC
from app.models.mock_oem import MockOEM
from app.models.mock_blacklist import MockBlacklist


def not_verified(source: str, company_name: str | None, message: str) -> dict:
    return {
        "source": source,
        "status": "NOT_VERIFIED",
        "entity_name": company_name,
        "registration_status": "NOT_FOUND",
        "verified_at": None,
        "confidence": 0.0,
        "evidence": message,
    }


def verify_requirement(
    requirement_type: str,
    bidder,
    db: Session,
    extra_identifiers: dict | None = None,
) -> dict | None:

    extra_identifiers = extra_identifiers or {}
    company_name = bidder.company_name

    # -----------------------------------------
    # GST
    # -----------------------------------------

    if requirement_type == "GST":

        if not bidder.gstin:
            return not_verified(
                "GSTN",
                company_name,
                "Bidder GSTIN was not provided.",
            )

        record = (
            db.query(MockGST)
            .filter(MockGST.gstin == bidder.gstin)
            .first()
        )

        if not record:
            return not_verified(
                "GSTN",
                company_name,
                "GSTIN was not found in the ground-truth database.",
            )

        return {
            "source": "GSTN",
            "status": "VERIFIED"
            if record.registration_status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.legal_name,
            "registration_status": record.registration_status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.98,
            "evidence": (
                f"GST ground-truth record found for {record.legal_name}. "
                f"Registration status = {record.registration_status}."
            ),
        }

    # -----------------------------------------
    # PAN / Income Tax
    # -----------------------------------------

    if requirement_type == "PAN_INCOME_TAX":

        if not bidder.pan:
            return not_verified(
                "Income Tax / PAN",
                company_name,
                "Bidder PAN was not provided.",
            )

        record = (
            db.query(MockPAN)
            .filter(MockPAN.pan == bidder.pan)
            .first()
        )

        if not record:
            return not_verified(
                "Income Tax / PAN",
                company_name,
                "PAN was not found in the ground-truth database.",
            )

        return {
            "source": "Income Tax / PAN",
            "status": "VERIFIED"
            if record.status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.legal_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.97,
            "evidence": (
                f"PAN ground-truth record found for {record.legal_name}. "
                f"Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # Udyam / MSME
    # -----------------------------------------

    if requirement_type == "MSME_UDYAM":

        udyam_number = extra_identifiers.get("udyam")

        if not udyam_number:
            return not_verified(
                "Udyam Registration",
                company_name,
                "Udyam registration number was not provided.",
            )

        record = (
            db.query(MockUdyam)
            .filter(MockUdyam.udyam_number == udyam_number)
            .first()
        )

        if not record:
            return not_verified(
                "Udyam Registration",
                company_name,
                "Udyam number was not found in the ground-truth database.",
            )

        return {
            "source": "Udyam Registration",
            "status": "VERIFIED"
            if record.status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.enterprise_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.97,
            "evidence": (
                f"Udyam ground-truth record found for "
                f"{record.enterprise_name}. Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # EPFO
    # -----------------------------------------

    if requirement_type == "EPFO":

        epfo_number = extra_identifiers.get("epfo")

        if not epfo_number:
            return not_verified(
                "EPFO",
                company_name,
                "EPFO registration number was not provided.",
            )

        record = (
            db.query(MockEPFO)
            .filter(MockEPFO.epfo_number == epfo_number)
            .first()
        )

        if not record:
            return not_verified(
                "EPFO",
                company_name,
                "EPFO number was not found in the ground-truth database.",
            )

        return {
            "source": "EPFO",
            "status": "VERIFIED"
            if record.status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.company_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.96,
            "evidence": (
                f"EPFO ground-truth record found for "
                f"{record.company_name}. Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # ESIC
    # -----------------------------------------

    if requirement_type == "ESIC":

        esic_number = extra_identifiers.get("esic")

        if not esic_number:
            return not_verified(
                "ESIC",
                company_name,
                "ESIC registration number was not provided.",
            )

        record = (
            db.query(MockESIC)
            .filter(MockESIC.esic_number == esic_number)
            .first()
        )

        if not record:
            return not_verified(
                "ESIC",
                company_name,
                "ESIC number was not found in the ground-truth database.",
            )

        return {
            "source": "ESIC",
            "status": "VERIFIED"
            if record.status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.company_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.96,
            "evidence": (
                f"ESIC ground-truth record found for "
                f"{record.company_name}. Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # Startup India
    # -----------------------------------------

    if requirement_type == "STARTUP":

        startup_number = extra_identifiers.get("startup")

        if not startup_number:
            return not_verified(
                "Startup India",
                company_name,
                "Startup recognition number was not provided.",
            )

        record = (
            db.query(MockStartup)
            .filter(MockStartup.recognition_number == startup_number)
            .first()
        )

        if not record:
            return not_verified(
                "Startup India",
                company_name,
                "Startup recognition number was not found in the ground-truth database.",
            )

        return {
            "source": "Startup India",
            "status": "VERIFIED"
            if record.status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.company_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.95,
            "evidence": (
                f"Startup India ground-truth record found for "
                f"{record.company_name}. Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # NSIC
    # -----------------------------------------

    if requirement_type == "NSIC":

        nsic_number = extra_identifiers.get("nsic")

        if not nsic_number:
            return not_verified(
                "NSIC",
                company_name,
                "NSIC certificate number was not provided.",
            )

        record = (
            db.query(MockNSIC)
            .filter(MockNSIC.certificate_number == nsic_number)
            .first()
        )

        if not record:
            return not_verified(
                "NSIC",
                company_name,
                "NSIC certificate was not found in the ground-truth database.",
            )

        return {
            "source": "NSIC",
            "status": "VERIFIED"
            if record.status == "ACTIVE"
            else "NOT_VERIFIED",
            "entity_name": record.company_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.95,
            "evidence": (
                f"NSIC ground-truth record found for "
                f"{record.company_name}. Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # OEM Authorization
    # -----------------------------------------

    if requirement_type == "OEM":

        authorization_number = extra_identifiers.get("oem")

        if not authorization_number:
            return not_verified(
                "OEM Authorization Database",
                company_name,
                "OEM authorization number was not provided.",
            )

        record = (
            db.query(MockOEM)
            .filter(
                MockOEM.authorization_number == authorization_number
            )
            .first()
        )

        if not record:
            return not_verified(
                "OEM Authorization Database",
                company_name,
                "OEM authorization was not found in the ground-truth database.",
            )

        return {
            "source": "OEM Authorization Database",
            "status": "VERIFIED"
            if record.authorization_status == "AUTHORIZED"
            else "NOT_VERIFIED",
            "entity_name": record.oem_name,
            "registration_status": record.authorization_status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.98,
            "evidence": (
                f"OEM authorization record found. "
                f"Authorization status = {record.authorization_status}."
            ),
        }

    # -----------------------------------------
    # Blacklist / Debarment
    # -----------------------------------------

    if requirement_type == "BLACKLIST":

        if not company_name:
            return not_verified(
                "Blacklisting Database",
                None,
                "Bidder company name was not provided.",
            )

        record = (
            db.query(MockBlacklist)
            .filter(
                MockBlacklist.company_name == company_name
            )
            .first()
        )

        if not record:
            return not_verified(
                "Blacklisting Database",
                company_name,
                "Company was not found in the ground-truth database.",
            )

        return {
            "source": "Blacklisting Database",
            "status": (
                "VERIFIED"
                if record.status == "NOT_BLACKLISTED"
                else "NOT_VERIFIED"
            ),
            "entity_name": record.company_name,
            "registration_status": record.status,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.98,
            "evidence": (
                f"Blacklisting ground-truth record found. "
                f"Status = {record.status}."
            ),
        }

    # -----------------------------------------
    # Document / rule-based requirements
    # -----------------------------------------

    if requirement_type in [
        "MAKE_IN_INDIA",
        "ATC_DOCUMENT",
        "LAND_BORDER_ELIGIBILITY",
    ]:
        return None

    # -----------------------------------------
    # Unknown requirement
    # -----------------------------------------

    return None