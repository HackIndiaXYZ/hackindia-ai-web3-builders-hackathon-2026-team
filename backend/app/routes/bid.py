from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.bid import Bid
from app.models.tender import Tender
from app.models.bidder import Bidder
from app.schemas.bid import BidCreate, BidResponse


router = APIRouter(prefix="/bids", tags=["Bids"])


@router.post("/", response_model=BidResponse)
def create_bid(
    bid: BidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check whether tender exists
    tender = db.query(Tender).filter(
        Tender.tender_id == bid.tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=404,
            detail="Tender not found"
        )

    # Check whether bidder exists
    bidder = db.query(Bidder).filter(
        Bidder.bidder_id == bid.bidder_id
    ).first()

    if not bidder:
        raise HTTPException(
            status_code=404,
            detail="Bidder not found"
        )

    new_bid = Bid(
        tender_id=bid.tender_id,
        bidder_id=bid.bidder_id,
        bid_amount=bid.bid_amount,
        bid_date=bid.bid_date,
        bid_status=bid.bid_status,
        is_winner=bid.is_winner,
        source_url=bid.source_url,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)

    return new_bid


@router.get("/", response_model=list[BidResponse])
def get_bids(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bids = db.query(Bid).all()
    return bids


@router.get("/{bid_id}", response_model=BidResponse)
def get_bid(
    bid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bid = db.query(Bid).filter(
        Bid.bid_id == bid_id
    ).first()

    if not bid:
        raise HTTPException(
            status_code=404,
            detail="Bid not found"
        )

    return bid