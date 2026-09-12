from fastapi import APIRouter

from app.services.mock_verification_service import (
    verify_gst,
    verify_udyam,
    verify_pan,
    verify_epfo,
    verify_esic,
    verify_blacklist
)


router = APIRouter(
    prefix="/api/mock",
    tags=["Mock Verification APIs"]
)


@router.get("/gst/{gstin}")
def mock_gst_verification(gstin: str):
    return verify_gst(gstin)


@router.get("/udyam/{number}")
def mock_udyam_verification(number: str):
    return verify_udyam(number)


@router.get("/pan/{pan}")
def mock_pan_verification(pan: str):
    return verify_pan(pan)


@router.get("/epfo/{number}")
def mock_epfo_verification(number: str):
    return verify_epfo(number)


@router.get("/esic/{number}")
def mock_esic_verification(number: str):
    return verify_esic(number)


@router.get("/blacklist/{company}")
def mock_blacklist_verification(company: str):
    return verify_blacklist(company)