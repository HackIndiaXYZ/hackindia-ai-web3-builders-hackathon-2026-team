from datetime import datetime

from pydantic import BaseModel


class ComplianceRequirementCreate(BaseModel):
    tender_id: int
    document_id: int | None = None
    requirement_type: str | None = None
    requirement_text: str
    mandatory: bool = True
    source_page: str | None = None


class ComplianceRequirementResponse(BaseModel):
    requirement_id: int
    tender_id: int
    document_id: int | None
    requirement_type: str | None
    requirement_text: str
    mandatory: bool
    source_page: str | None
    created_at: datetime

    class Config:
        from_attributes = True