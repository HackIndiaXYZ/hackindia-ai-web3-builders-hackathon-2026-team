from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.bidder import Bidder
from app.schemas.bidder import BidderCreate, BidderResponse
from datetime import datetime, timezone


router = APIRouter(
    prefix="/bidders",
    tags=["Bidders"]
)


@router.post(
    "/",
    response_model=BidderResponse
)
def create_bidder(
    bidder: BidderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_bidder = Bidder(
        company_name=bidder.company_name,
        email=bidder.email,
        gstin=bidder.gstin,
        pan=bidder.pan,
        address=bidder.address,
        contact_person=bidder.contact_person,
        source_name=bidder.source_name,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_bidder)
    db.commit()
    db.refresh(new_bidder)

    return new_bidder


@router.get(
    "/",
    response_model=list[BidderResponse]
)
def get_bidders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bidders = db.query(Bidder).all()
    return bidders


@router.get(
    "/{bidder_id}",
    response_model=BidderResponse
)
def get_bidder(
    bidder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bidder = (
        db.query(Bidder)
        .filter(Bidder.bidder_id == bidder_id)
        .first()
    )

    if not bidder:
        raise HTTPException(
            status_code=404,
            detail="Bidder not found"
        )

    return bidder