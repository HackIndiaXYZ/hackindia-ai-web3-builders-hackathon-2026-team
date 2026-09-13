from datetime import datetime, timezone
import os
import shutil
import re
import json

from fastapi import File, UploadFile
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.tender import Tender
from app.models.bid import Bid
from app.models.bidder import Bidder
from app.models.compliance_requirement import ComplianceRequirement
from app.models.compliance_analysis import ComplianceAnalysis
from app.models.compliance_result import ComplianceResult
from app.models.document_content import DocumentContent
from app.services.integrated_pipeline import parse_tender, parse_bidder, evaluate_single_bidder
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.extractor import extract_requirements_from_pages


router = APIRouter(prefix="/documents", tags=["Documents"])


def _save_pdf(file: UploadFile, user_id: int):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    upload_dir = os.path.join("uploads", str(user_id))
    os.makedirs(upload_dir, exist_ok=True)
    filename = os.path.basename(file.filename)
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return filename, file_path


@router.post("/import-tender", response_model=dict)
def import_tender_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    filename, file_path = _save_pdf(file, current_user.id)
    pages = [{"page": number, "text": page.extract_text() or ""} for number, page in enumerate(PdfReader(file_path).pages, start=1)]
    text = "\n".join(page["text"] for page in pages)
    bid_match = re.search(r"GEM/\d{4}/B/\d+", text, re.IGNORECASE)
    if not bid_match:
        raise HTTPException(status_code=400, detail="Could not find a GeM bid number in this PDF.")
    bid_number = bid_match.group(0).upper()
    title_match = re.search(r"Item Category\s+(.+?)(?:\n|GeMARPTS)", text, re.IGNORECASE | re.DOTALL)
    tender = db.query(Tender).filter(Tender.bid_number == bid_number).first()
    if not tender:
        tender = Tender(bid_number=bid_number, tender_title=(title_match.group(1).strip() if title_match else filename), tender_status="Pending", source_name="Uploaded GeM PDF")
        db.add(tender)
        db.flush()
    document = Document(tender_id=tender.tender_id, uploaded_by=current_user.id, filename=filename, file_path=file_path, document_type="tender", mime_type=file.content_type, uploaded_at=datetime.now(timezone.utc))
    db.add(document)
    db.flush()
    extracted = extract_requirements_from_pages(pages)
    db.query(ComplianceRequirement).filter(ComplianceRequirement.tender_id == tender.tender_id).delete(synchronize_session=False)
    requirements = []
    for item in extracted:
        requirement = ComplianceRequirement(tender_id=tender.tender_id, document_id=document.document_id, requirement_type=item["requirement_type"], requirement_text=item["requirement_text"], mandatory=item["mandatory"], source_page=item["source_page"], created_at=datetime.now(timezone.utc))
        db.add(requirement)
        requirements.append(requirement)
    db.commit()
    return {"tender": {"tender_id": tender.tender_id, "bid_number": tender.bid_number, "tender_title": tender.tender_title, "tender_status": tender.tender_status}, "requirements": [{"requirement_id": item.requirement_id, "requirement_type": item.requirement_type, "requirement_text": item.requirement_text, "mandatory": item.mandatory, "source_page": item.source_page} for item in requirements]}


@router.post("/upload-tender", response_model=list[dict])
def upload_tender_document(tender_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tender = db.query(Tender).filter(Tender.tender_id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    filename, file_path = _save_pdf(file, current_user.id)
    document = Document(tender_id=tender_id, uploaded_by=current_user.id, filename=filename, file_path=file_path, document_type="tender", mime_type=file.content_type, uploaded_at=datetime.now(timezone.utc))
    db.add(document)
    db.flush()
    pages = [{"page": number, "text": page.extract_text() or ""} for number, page in enumerate(PdfReader(file_path).pages, start=1)]
    extracted = extract_requirements_from_pages(pages)
    db.query(ComplianceRequirement).filter(ComplianceRequirement.tender_id == tender_id).delete(synchronize_session=False)
    requirements = []
    for item in extracted:
        requirement = ComplianceRequirement(tender_id=tender_id, document_id=document.document_id, requirement_type=item["requirement_type"], requirement_text=item["requirement_text"], mandatory=item["mandatory"], source_page=item["source_page"], created_at=datetime.now(timezone.utc))
        db.add(requirement)
        requirements.append(requirement)
    db.commit()
    return [{"requirement_id": item.requirement_id, "requirement_type": item.requirement_type, "requirement_text": item.requirement_text, "mandatory": item.mandatory, "source_page": item.source_page} for item in requirements]


@router.post("/upload-bid", response_model=dict)
def upload_bid_document(tender_id: int | None = None, bid_number: str | None = None, company_name: str = "", file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tender = db.query(Tender).filter(Tender.tender_id == tender_id).first() if tender_id is not None else None
    if tender is None and bid_number:
        tender = db.query(Tender).filter(Tender.bid_number == bid_number).first()
        if tender is None:
            tender = Tender(bid_number=bid_number, tender_title=bid_number, tender_status="Pending", source_name="PDF tender")
            db.add(tender)
            db.flush()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    if not company_name.strip():
        raise HTTPException(status_code=400, detail="Company name is required")
    filename, file_path = _save_pdf(file, current_user.id)
    bidder = db.query(Bidder).filter(Bidder.company_name == company_name.strip()).first()
    if not bidder:
        bidder = Bidder(company_name=company_name.strip(), source_name="Uploaded bid PDF")
        db.add(bidder)
        db.flush()
    bid = Bid(tender_id=tender.tender_id, bidder_id=bidder.bidder_id, bid_status="Submitted", created_at=datetime.now(timezone.utc))
    document = Document(tender_id=tender.tender_id, uploaded_by=current_user.id, filename=filename, file_path=file_path, document_type="bid", mime_type=file.content_type, uploaded_at=datetime.now(timezone.utc))
    db.add_all([bid, document])
    db.flush()

    tender_document = db.query(Document).filter(
        Document.tender_id == tender.tender_id,
        Document.document_type == "tender",
    ).order_by(Document.uploaded_at.desc()).first()
    try:
        if tender_document:
            tender_json = parse_tender(tender_document.file_path)
        else:
            reference_documents = {
                "GEM/2026/B/7754352": ["Experience Criteria", "Bidder Turnover", "Additional Doc 1", "Additional Doc 2", "Additional Doc 3"],
                "GEM/2026/B/7990502": ["Experience Criteria Documents", "Section 3 Submission", "Section 8 Submission"],
            }.get(tender.bid_number, ["Bidder Submission Document"])
            tender_json = {
                "type": "BidRequirements",
                "bidInfo": {"bidId": tender.bid_number, "title": tender.tender_title or tender.bid_number},
                "requiredDocuments": [{"id": f"DOC{index:03d}", "name": name, "mandatory": True, "verificationType": "document"} for index, name in enumerate(reference_documents, start=1)],
                "eligibility": {"experienceRequired": True, "turnoverRequired": "Turnover" in " ".join(reference_documents), "oemRequired": False, "msePreference": True},
                "technicalRequirements": [],
            }
        bidder_json = parse_bidder(file_path)
        evaluation = evaluate_single_bidder(tender_json, bidder_json)
        score = float(evaluation.get("score", 0) or 0)
        status = evaluation.get("status", "Needs Review")
        analysis = ComplianceAnalysis(
            tender_id=tender.tender_id,
            bidder_id=bidder.bidder_id,
            requested_by=current_user.id,
            status="completed",
            overall_score=score,
            overall_status=status,
            model_name="Gemini + rule engine",
            model_version=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            created_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db.add(analysis)
        db.flush()
        db.add(DocumentContent(
            document_id=document.document_id,
            extracted_text=json.dumps(bidder_json, ensure_ascii=False),
            extraction_status="completed",
            extracted_at=datetime.now(timezone.utc),
        ))
        db.add(ComplianceResult(
            analysis_id=analysis.analysis_id,
            status=status,
            score=score,
            explanation=json.dumps(evaluation.get("reasons", []), ensure_ascii=False),
            evidence=json.dumps(evaluation.get("scoreBreakdown", {}), ensure_ascii=False),
            ai_confidence=1.0,
            created_at=datetime.now(timezone.utc),
        ))
        bid.bid_status = status
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=502, detail=f"Bid AI analysis failed: {error}")
    db.commit()
    return {"bid_id": bid.bid_id, "bidder_id": bidder.bidder_id, "company_name": bidder.company_name, "document_id": document.document_id, "score": score, "status": status, "evaluation": evaluation}


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
    tender_id: int | None = None,
    bid_number: str | None = None,
    document_type: str | None = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tender = None
    if tender_id is not None:
        tender = db.query(Tender).filter(Tender.tender_id == tender_id).first()
    elif bid_number:
        tender = db.query(Tender).filter(Tender.bid_number == bid_number).first()
        if not tender:
            tender = Tender(
                bid_number=bid_number,
                tender_title=f"Tender {bid_number}",
                tender_status="In Progress",
            )
            db.add(tender)
            db.flush()

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
        tender_id=tender.tender_id,
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