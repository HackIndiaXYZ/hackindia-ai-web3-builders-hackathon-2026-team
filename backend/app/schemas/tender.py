from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TenderCreate(BaseModel):
    organisation_id: int | None = None
    bid_number: str
    tender_title: str | None = None
    item_category: str | None = None
    tender_description: str | None = None
    estimated_value: Decimal | None = None
    quantity: Decimal | None = None
    bid_start_date: datetime | None = None
    bid_end_date: datetime | None = None
    bid_opening_date: datetime | None = None
    tender_status: str | None = None
    procurement_mode: str | None = None
    source_url: str | None = None
    source_name: str | None = None
    source_record_date: datetime | None = None


class TenderResponse(BaseModel):
    tender_id: int
    organisation_id: int | None
    bid_number: str
    tender_title: str | None
    item_category: str | None
    tender_description: str | None
    estimated_value: Decimal | None
    quantity: Decimal | None
    bid_start_date: datetime | None
    bid_end_date: datetime | None
    bid_opening_date: datetime | None
    tender_status: str | None
    procurement_mode: str | None
    source_url: str | None
    source_name: str | None
    source_record_date: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True