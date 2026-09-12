from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.compliance_analysis import ComplianceAnalysis
from app.models.compliance_requirement import ComplianceRequirement
from app.models.compliance_result import ComplianceResult
from app.schemas.compliance_result import (
    ComplianceResultCreate,
    ComplianceResultResponse
)


router = APIRouter(
    prefix="/compliance-results",
    tags=["Compliance Results"]
)


@router.post(
    "/",
    response_model=ComplianceResultResponse
)
def create_result(
    result: ComplianceResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check analysis
    analysis = db.query(ComplianceAnalysis).filter(
        ComplianceAnalysis.analysis_id == result.analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Compliance analysis not found"
        )

    # Check requirement if provided
    if result.requirement_id is not None:
        requirement = db.query(ComplianceRequirement).filter(
            ComplianceRequirement.requirement_id == result.requirement_id
        ).first()

        if not requirement:
            raise HTTPException(
                status_code=404,
                detail="Compliance requirement not found"
            )

    new_result = ComplianceResult(
        analysis_id=result.analysis_id,
        requirement_id=result.requirement_id,
        status=result.status,
        score=result.score,
        explanation=result.explanation,
        evidence=result.evidence,
        ai_confidence=result.ai_confidence,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


@router.get(
    "/",
    response_model=list[ComplianceResultResponse]
)
def get_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(ComplianceResult).all()
    return results


@router.get(
    "/{result_id}",
    response_model=ComplianceResultResponse
)
def get_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = db.query(ComplianceResult).filter(
        ComplianceResult.result_id == result_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Compliance result not found"
        )

    return result