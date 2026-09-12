from datetime import datetime
from pydantic import BaseModel, EmailStr


class BidderCreate(BaseModel):
    company_name: str
    email: EmailStr | None = None
    gstin: str | None = None
    pan: str | None = None
    address: str | None = None
    contact_person: str | None = None
    source_name: str | None = None


class BidderResponse(BaseModel):
    bidder_id: int
    company_name: str
    email: EmailStr | None
    gstin: str | None
    pan: str | None
    address: str | None
    contact_person: str | None
    source_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True