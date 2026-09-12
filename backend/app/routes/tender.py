from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.tender import Tender
from app.schemas.tender import TenderCreate, TenderResponse


router = APIRouter(
    prefix="/tenders",
    tags=["Tenders"]
)


@router.post(
    "/",
    response_model=TenderResponse
)
def create_tender(
    tender: TenderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_tender = Tender(
        organisation_id=tender.organisation_id,
        bid_number=tender.bid_number,
        tender_title=tender.tender_title,
        item_category=tender.item_category,
        tender_description=tender.tender_description,
        estimated_value=tender.estimated_value,
        quantity=tender.quantity,
        bid_start_date=tender.bid_start_date,
        bid_end_date=tender.bid_end_date,
        bid_opening_date=tender.bid_opening_date,
        tender_status=tender.tender_status,
        procurement_mode=tender.procurement_mode,
        source_url=tender.source_url,
        source_name=tender.source_name,
        source_record_date=tender.source_record_date
    )

    db.add(new_tender)
    db.commit()
    db.refresh(new_tender)

    return new_tender

@router.get(
    "/",
    response_model=list[TenderResponse]
)
def get_tenders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tenders = db.query(Tender).all()
    return tenders

@router.get(
    "/{tender_id}",
    response_model=TenderResponse
)
def get_tender(
    tender_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tender = db.query(Tender).filter(Tender.tender_id == tender_id).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    return tender