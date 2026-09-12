from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.compliance_analysis import ComplianceAnalysis
from app.models.officer_decision import OfficerDecision

from app.schemas.officer_decision import (
    OfficerDecisionCreate,
    OfficerDecisionResponse
)


router = APIRouter(
    prefix="/officer-decisions",
    tags=["Officer Decisions"]
)


ALLOWED_DECISIONS = {
    "QUALIFY",
    "DISQUALIFY",
    "REQUEST_CLARIFICATION"
}


@router.post(
    "/",
    response_model=OfficerDecisionResponse
)
def create_officer_decision(
    decision_data: OfficerDecisionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if decision_data.decision not in ALLOWED_DECISIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid decision. Use QUALIFY, "
                "DISQUALIFY or REQUEST_CLARIFICATION."
            )
        )

    analysis = db.query(ComplianceAnalysis).filter(
        ComplianceAnalysis.analysis_id == decision_data.analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Compliance analysis not found"
        )

    decision = OfficerDecision(
        analysis_id=str(analysis.analysis_id),
        officer_id=current_user.id,
        decision=decision_data.decision,
        remarks=decision_data.remarks
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


@router.get(
    "/{analysis_id}",
    response_model=list[OfficerDecisionResponse]
)
def get_analysis_decisions(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(OfficerDecision)
        .filter(
            OfficerDecision.analysis_id == analysis_id
        )
        .order_by(
            OfficerDecision.decided_at.desc()
        )
        .all()
    )