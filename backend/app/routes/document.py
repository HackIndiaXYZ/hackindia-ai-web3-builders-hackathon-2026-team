from datetime import datetime, timezone
import os

from fastapi import File, UploadFile
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.tender import Tender
from app.schemas.document import DocumentCreate, DocumentResponse


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether tender exists
    if document.tender_id is not None:
        tender = db.query(Tender).filter(
            Tender.tender_id == document.tender_id
        ).first()

        if not tender:
            raise HTTPException(
                status_code=404,
                detail="Tender not found"
            )

    new_document = Document(
        tender_id=document.tender_id,
        uploaded_by=current_user.id,
        filename=document.filename,
        file_path=document.file_path,
        document_type=document.document_type,
        mime_type=document.mime_type,
        source_url=document.source_url,
        uploaded_at=datetime.now(timezone.utc)
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document
@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    tender_id: int,
    document_type: str | None = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether tender exists
    tender = db.query(Tender).filter(
        Tender.tender_id == tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    # Create upload directory
    upload_dir = os.path.join(
        "uploads",
        str(current_user.id)
    )

    os.makedirs(upload_dir, exist_ok=True)

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is missing"
        )

    filename = file.filename

    # Create file path
    file_path = os.path.join(
        upload_dir,
        filename
    )

    # Save actual uploaded file
    with open(file_path, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)

    # Store file information in database
    new_document = Document(
        tender_id=tender_id,
        uploaded_by=current_user.id,
        filename=filename,
        file_path=file_path,
        document_type=document_type,
        mime_type=file.content_type,
        source_url=None,
        uploaded_at=datetime.now(timezone.utc)
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document

@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = db.query(Document).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document