from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models.audit_log import AuditLog
from app.models.officer_decision import OfficerDecision
from app.routes.auth import router as auth_router
from app.models.mock_gst import MockGST
from app.models.mock_udyam import MockUdyam
from app.core.auth import get_current_user
from app.models.user import User
from app.routes.tender import router as tender_router
from app.routes.bidder import router as bidder_router
from app.routes.bid import router as bid_router
from app.routes.document import router as document_router
from app.routes.document_content import router as document_content_router
from app.routes.compliance_requirement import (
    router as compliance_requirement_router
)
from app.routes.compliance_analysis import (
    router as compliance_analysis_router
)
from app.routes.compliance_result import (
    router as compliance_result_router
)
from app.routes.organisation import router as organisation_router
from app.routes.data_source import router as data_source_router
from app.routes.mock_verification import router as mock_verification_router
from app.routes.consistency import router as consistency_router
from app.routes.audit_log import router as audit_log_router
from app.routes.officer_decision import router as officer_decision_router
from app.models.mock_pan import MockPAN
from app.models.mock_epfo import MockEPFO
from app.models.mock_esic import MockESIC
from app.models.mock_startup import MockStartup
from app.models.mock_nsic import MockNSIC
from app.models.mock_oem import MockOEM
from app.models.mock_blacklist import MockBlacklist


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BidSure AI",
    description="AI-Powered Bid Compliance Verification Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication routes
app.include_router(auth_router)
app.include_router(tender_router)
app.include_router(bidder_router)
app.include_router(bid_router)
app.include_router(document_router)
app.include_router(document_content_router)
app.include_router(compliance_requirement_router)
app.include_router(compliance_analysis_router)
app.include_router(compliance_result_router)
app.include_router(organisation_router)
app.include_router(data_source_router)
app.include_router(mock_verification_router)
app.include_router(consistency_router)
app.include_router(audit_log_router)
app.include_router(officer_decision_router)

@app.get("/")
def root():
    return {
        "message": "BidSure AI Backend is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/protected")
def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.id,
        "email": current_user.email
    }

