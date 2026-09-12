from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.tender import Tender
from app.models.document import Document
from app.models.document_content import DocumentContent
from app.models.compliance_requirement import ComplianceRequirement

from app.schemas.compliance_requirement import (
    ComplianceRequirementCreate,
    ComplianceRequirementResponse
)

from app.services.extractor import extract_requirements_from_pages


router = APIRouter(
    prefix="/compliance-requirements",
    tags=["Compliance Requirements"]
)


# ============================================================
# CREATE A SINGLE COMPLIANCE REQUIREMENT MANUALLY
# ============================================================

@router.post(
    "/",
    response_model=ComplianceRequirementResponse
)
def create_requirement(
    requirement: ComplianceRequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether tender exists
    tender = db.query(Tender).filter(
        Tender.tender_id == requirement.tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    # Check document if provided
    if requirement.document_id is not None:

        document = db.query(Document).filter(
            Document.document_id == requirement.document_id
        ).first()

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

    # Create requirement
    new_requirement = ComplianceRequirement(
        tender_id=requirement.tender_id,
        document_id=requirement.document_id,
        requirement_type=requirement.requirement_type,
        requirement_text=requirement.requirement_text,
        mandatory=requirement.mandatory,
        source_page=requirement.source_page,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)

    return new_requirement


# ============================================================
# AUTOMATIC REQUIREMENT EXTRACTION FROM PDF
# ============================================================

@router.post(
    "/extract/{document_id}",
    response_model=list[ComplianceRequirementResponse]
)
def extract_compliance_requirements(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # --------------------------------------------------------
    # 1. Check whether document exists
    # --------------------------------------------------------

    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # --------------------------------------------------------
    # 2. Check whether document belongs to a tender
    # --------------------------------------------------------

    if document.tender_id is None:
        raise HTTPException(
            status_code=400,
            detail="Document is not associated with a tender"
        )

    # --------------------------------------------------------
    # 3. Check physical PDF file
    # --------------------------------------------------------

    if not document.file_path:
        raise HTTPException(
            status_code=404,
            detail="Document file path not found"
        )

    # --------------------------------------------------------
    # 4. Read PDF
    # --------------------------------------------------------

    try:

        reader = PdfReader(document.file_path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            page_text = page.extract_text() or ""

            pages.append({
                "page": page_number,
                "text": page_text
            })

        # ----------------------------------------------------
        # 5. Check whether text was extracted
        # ----------------------------------------------------

        complete_text = "\n".join(
            page["text"]
            for page in pages
        )

        if not complete_text.strip():

            raise HTTPException(
                status_code=422,
                detail="No text could be extracted from the document"
            )

        # ----------------------------------------------------
        # 6. Extract compliance requirements
        # ----------------------------------------------------

        extracted_requirements = extract_requirements_from_pages(
            pages
        )

        if not extracted_requirements:

            raise HTTPException(
                status_code=422,
                detail="No compliance requirements detected"
            )

        # ----------------------------------------------------
        # 7. Remove previously extracted requirements
        # ----------------------------------------------------
        # This prevents duplicate requirements when the
        # extraction endpoint is called again.

        existing_requirements = db.query(
            ComplianceRequirement
        ).filter(
            ComplianceRequirement.document_id == document_id
        ).all()

        for existing_requirement in existing_requirements:
            db.delete(existing_requirement)

        db.flush()

        # ----------------------------------------------------
        # 8. Create new requirement records
        # ----------------------------------------------------

        created_requirements = []

        for requirement in extracted_requirements:

            new_requirement = ComplianceRequirement(

                tender_id=document.tender_id,

                document_id=document_id,

                requirement_type=requirement[
                    "requirement_type"
                ],

                requirement_text=requirement[
                    "requirement_text"
                ],

                mandatory=requirement[
                    "mandatory"
                ],

                source_page=requirement[
                    "source_page"
                ],

                created_at=datetime.now(timezone.utc)
            )

            db.add(new_requirement)

            created_requirements.append(
                new_requirement
            )

        # ----------------------------------------------------
        # 9. Save everything
        # ----------------------------------------------------

        db.commit()

        # ----------------------------------------------------
        # 10. Refresh database objects
        # ----------------------------------------------------

        for requirement in created_requirements:
            db.refresh(requirement)

        return created_requirements

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Requirement extraction failed: {str(e)}"
        )


# ============================================================
# GET ALL COMPLIANCE REQUIREMENTS
# ============================================================

@router.get(
    "/",
    response_model=list[ComplianceRequirementResponse]
)
def get_requirements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requirements = db.query(
        ComplianceRequirement
    ).all()

    return requirements


# ============================================================
# GET ONE COMPLIANCE REQUIREMENT
# ============================================================

@router.get(
    "/{requirement_id}",
    response_model=ComplianceRequirementResponse
)
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requirement = db.query(
        ComplianceRequirement
    ).filter(
        ComplianceRequirement.requirement_id == requirement_id
    ).first()

    if not requirement:

        raise HTTPException(
            status_code=404,
            detail="Compliance requirement not found"
        )

    return requirement