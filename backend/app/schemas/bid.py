from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BidCreate(BaseModel):
    tender_id: int
    bidder_id: int
    bid_amount: Decimal | None = None
    bid_date: datetime | None = None
    bid_status: str | None = None
    is_winner: bool | None = False
    source_url: str | None = None


class BidResponse(BaseModel):
    bid_id: int
    tender_id: int
    bidder_id: int
    bid_amount: Decimal | None
    bid_date: datetime | None
    bid_status: str | None
    is_winner: bool | None
    source_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True