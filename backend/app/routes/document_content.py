from datetime import datetime, timezone
import os

from pypdf import PdfReader
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.document_content import DocumentContent
from app.schemas.document_content import DocumentContentResponse


router = APIRouter(
    prefix="/document-contents",
    tags=["Document Contents"]
)


@router.post(
    "/{document_id}",
    response_model=DocumentContentResponse
)
def create_document_content(
    document_id: int,
    extracted_text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether document exists
    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # One content record per document
    existing_content = db.query(DocumentContent).filter(
        DocumentContent.document_id == document_id
    ).first()

    if existing_content:
        existing_content.extracted_text = extracted_text
        existing_content.extraction_status = "completed"
        existing_content.extracted_at = datetime.now(timezone.utc)
        existing_content.extraction_error = None

        db.commit()
        db.refresh(existing_content)

        return existing_content

    new_content = DocumentContent(
        document_id=document_id,
        extracted_text=extracted_text,
        extraction_status="completed",
        extracted_at=datetime.now(timezone.utc),
        extraction_error=None
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return new_content

@router.post(
    "/{document_id}/extract",
    response_model=DocumentContentResponse
)
def extract_document_text(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether document exists
    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Check whether physical file exists
    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=404,
            detail="Physical document file not found"
        )

    try:
        # Read PDF
        reader = PdfReader(document.file_path)

        extracted_pages = []

        # Extract text from every page
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            extracted_pages.append(
                f"\n--- Page {page_number} ---\n{text}"
            )

        extracted_text = "\n".join(extracted_pages)

        # Check if text was extracted
        if not extracted_text.strip():
            raise HTTPException(
                status_code=422,
                detail="No text could be extracted from the document"
            )

        # Check for existing content
        existing_content = db.query(DocumentContent).filter(
            DocumentContent.document_id == document_id
        ).first()

        if existing_content:
            existing_content.extracted_text = extracted_text
            existing_content.extraction_status = "completed"
            existing_content.extracted_at = datetime.now(timezone.utc)
            existing_content.extraction_error = None

            db.commit()
            db.refresh(existing_content)

            return existing_content

        # Create new content record
        new_content = DocumentContent(
            document_id=document_id,
            extracted_text=extracted_text,
            extraction_status="completed",
            extracted_at=datetime.now(timezone.utc),
            extraction_error=None
        )

        db.add(new_content)
        db.commit()
        db.refresh(new_content)

        return new_content

    except HTTPException:
        raise

    except Exception as e:
        # Save extraction failure in database
        existing_content = db.query(DocumentContent).filter(
            DocumentContent.document_id == document_id
        ).first()

        if existing_content:
            existing_content.extraction_status = "failed"
            existing_content.extraction_error = str(e)
            existing_content.extracted_at = datetime.now(timezone.utc)
        else:
            failed_content = DocumentContent(
                document_id=document_id,
                extracted_text=None,
                extraction_status="failed",
                extracted_at=datetime.now(timezone.utc),
                extraction_error=str(e)
            )

            db.add(failed_content)

        db.commit()

        raise HTTPException(
            status_code=500,
            detail="Document text extraction failed"
        )
    
@router.get(
    "/{document_id}",
    response_model=DocumentContentResponse
)
def get_document_content(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = db.query(DocumentContent).filter(
        DocumentContent.document_id == document_id
    ).first()

    if not content:
        raise HTTPException(
            status_code=404,
            detail="Document content not found"
        )

    return content