from datetime import datetime, timezone
from app.models.tender import Tender
from app.models.bidder import Bidder
from app.models.compliance_result import ComplianceResult
from app.schemas.compliance_analysis import ComplianceReportResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.tender import Tender
from app.models.bidder import Bidder
from app.models.compliance_analysis import ComplianceAnalysis
from app.models.compliance_requirement import ComplianceRequirement
from app.models.compliance_result import ComplianceResult

from app.schemas.compliance_analysis import (
    ComplianceAnalysisCreate,
    ComplianceAnalysisResponse
)

from app.services.verification_service import verify_requirement
from app.services.compliance_engine import (
    evaluate_requirement,
    calculate_overall_score,
    determine_overall_status,
    determine_risk
)


router = APIRouter(
    prefix="/compliance-analyses",
    tags=["Compliance Analysis"]
)


# ============================================================
# CREATE ANALYSIS
# ============================================================

@router.post(
    "/",
    response_model=ComplianceAnalysisResponse
)
def create_analysis(
    analysis: ComplianceAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # --------------------------------------------------------
    # Check tender
    # --------------------------------------------------------

    tender = db.query(Tender).filter(
        Tender.tender_id == analysis.tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    # --------------------------------------------------------
    # Check bidder
    # --------------------------------------------------------

    if analysis.bidder_id is not None:

        bidder = db.query(Bidder).filter(
            Bidder.bidder_id == analysis.bidder_id
        ).first()

        if not bidder:
            raise HTTPException(
                status_code=404,
                detail="Bidder not found"
            )

    # --------------------------------------------------------
    # Create pending analysis
    # --------------------------------------------------------

    new_analysis = ComplianceAnalysis(
        tender_id=analysis.tender_id,
        bidder_id=analysis.bidder_id,
        requested_by=current_user.id,
        status="pending",
        overall_score=None,
        overall_status=None,
        model_name=analysis.model_name,
        model_version=analysis.model_version,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis


# ============================================================
# RUN COMPLETE COMPLIANCE ANALYSIS
# ============================================================

@router.post(
    "/run",
    response_model=ComplianceAnalysisResponse
)
def run_compliance_analysis(
    analysis: ComplianceAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # 1. Check tender
    # --------------------------------------------------------

    tender = db.query(Tender).filter(
        Tender.tender_id == analysis.tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    # --------------------------------------------------------
    # 2. Check bidder
    # --------------------------------------------------------

    if analysis.bidder_id is None:
        raise HTTPException(
            status_code=400,
            detail="bidder_id is required to run compliance analysis"
        )

    bidder = db.query(Bidder).filter(
        Bidder.bidder_id == analysis.bidder_id
    ).first()

    if not bidder:
        raise HTTPException(
            status_code=404,
            detail="Bidder not found"
        )

    # --------------------------------------------------------
    # 3. Get compliance requirements for this tender
    # --------------------------------------------------------

    requirements = db.query(
        ComplianceRequirement
    ).filter(
        ComplianceRequirement.tender_id == analysis.tender_id
    ).all()

    if not requirements:
        raise HTTPException(
            status_code=404,
            detail="No compliance requirements found for this tender"
        )

    # --------------------------------------------------------
    # 4. Create analysis record
    # --------------------------------------------------------

    new_analysis = ComplianceAnalysis(
        tender_id=analysis.tender_id,
        bidder_id=analysis.bidder_id,
        requested_by=current_user.id,
        status="running",
        overall_score=None,
        overall_status=None,
        model_name=(
            analysis.model_name
            or "BidSure Compliance Engine"
        ),
        model_version=(
            analysis.model_version
            or "1.0"
        ),
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # --------------------------------------------------------
    # 5. Demo identifiers
    #
    # These will later come from verified bidder documents
    # or authorized government integrations.
    # --------------------------------------------------------

    extra_identifiers = {
        "udyam": "UDYAM-MH-18-0012345",
        "epfo": "EPFO-ABC-001",
        "esic": "ESIC-ABC-001"
    }

    evaluated_results = []

    # --------------------------------------------------------
    # 6. Process every requirement
    # --------------------------------------------------------

    for requirement in requirements:

        verification_result = verify_requirement(
            requirement.requirement_type,
            bidder,
            extra_identifiers
        )

        evaluated = evaluate_requirement(
            requirement_type=requirement.requirement_type,
            verification_result=verification_result,
            mandatory=requirement.mandatory
        )

        # Add DB requirement information
        evaluated["requirement_type"] = (
            requirement.requirement_type
        )

        evaluated["mandatory"] = (
            requirement.mandatory
        )

        evaluated_results.append(evaluated)

        # ----------------------------------------------------
        # Save compliance result
        # ----------------------------------------------------

        new_result = ComplianceResult(
            analysis_id=new_analysis.analysis_id,
            requirement_id=requirement.requirement_id,
            status=evaluated["status"],
            score=evaluated["score"],
            explanation=evaluated["explanation"],
            evidence=evaluated["evidence"],
            ai_confidence=evaluated["ai_confidence"],
            created_at=datetime.now(timezone.utc)
        )

        db.add(new_result)

    # --------------------------------------------------------
    # 7. Calculate overall score
    # --------------------------------------------------------

    overall_score = calculate_overall_score(
        evaluated_results
    )

    # --------------------------------------------------------
    # 8. Determine overall status
    # --------------------------------------------------------

    overall_status = determine_overall_status(
        evaluated_results
    )

    # --------------------------------------------------------
    # 9. Determine risk
    # --------------------------------------------------------

    risk = determine_risk(
        overall_score
    )

    # --------------------------------------------------------
    # 10. Store final analysis
    # --------------------------------------------------------

    new_analysis.status = "completed"

    new_analysis.overall_score = overall_score

    new_analysis.overall_status = (
        f"{overall_status} - {risk} RISK"
    )

    new_analysis.completed_at = (
        datetime.now(timezone.utc)
    )

    db.commit()
    db.refresh(new_analysis)

    return new_analysis


# ============================================================
# GET ALL ANALYSES
# ============================================================

@router.get(
    "/",
    response_model=list[ComplianceAnalysisResponse]
)
def get_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    analyses = db.query(
        ComplianceAnalysis
    ).all()

    return analyses


# ============================================================
# GET ONE ANALYSIS
# ============================================================

@router.get(
    "/{analysis_id}",
    response_model=ComplianceAnalysisResponse
)
def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    analysis = db.query(
        ComplianceAnalysis
    ).filter(
        ComplianceAnalysis.analysis_id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Compliance analysis not found"
        )

    return analysis
@router.get(
    "/{analysis_id}/report",
    response_model=ComplianceReportResponse
)
def get_compliance_report(
    analysis_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get analysis
    analysis = db.query(ComplianceAnalysis).filter(
        ComplianceAnalysis.analysis_id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Compliance analysis not found"
        )

    # Get tender
    tender = db.query(Tender).filter(
        Tender.tender_id == analysis.tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    # Get bidder
    bidder = None

    if analysis.bidder_id is not None:
        bidder = db.query(Bidder).filter(
            Bidder.bidder_id == analysis.bidder_id
        ).first()

    # Get all compliance results
    results = db.query(ComplianceResult).filter(
        ComplianceResult.analysis_id == analysis_id
    ).all()

    report_results = []

    for result in results:

        requirement = None

        if result.requirement_id is not None:
            requirement = db.query(ComplianceRequirement).filter(
                ComplianceRequirement.requirement_id ==
                result.requirement_id
            ).first()

        report_results.append({
            "result_id": result.result_id,
            "requirement_id": result.requirement_id,

            "requirement_type": (
                requirement.requirement_type
                if requirement else None
            ),

            "requirement_text": (
                requirement.requirement_text
                if requirement else None
            ),

            "mandatory": (
                requirement.mandatory
                if requirement else None
            ),

            "source_page": (
                requirement.source_page
                if requirement else None
            ),

            "status": result.status,
            "score": result.score,
            "explanation": result.explanation,
            "evidence": result.evidence,
            "ai_confidence": result.ai_confidence
        })

    return {
        "analysis_id": str(analysis.analysis_id),

        "tender_id": tender.tender_id,
        "tender_title": tender.tender_title,
        "bid_number": tender.bid_number,

        "bidder_id": bidder.bidder_id if bidder else None,
        "bidder_name": bidder.company_name if bidder else None,
        "gstin": bidder.gstin if bidder else None,
        "pan": bidder.pan if bidder else None,

        "status": analysis.status,
        "overall_score": analysis.overall_score,
        "overall_status": analysis.overall_status,

        "model_name": analysis.model_name,
        "model_version": analysis.model_version,

        "results": report_results
    }