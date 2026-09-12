from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ComplianceAnalysisCreate(BaseModel):
    tender_id: int
    bidder_id: int | None = None
    model_name: str | None = None
    model_version: str | None = None


class ComplianceAnalysisResponse(BaseModel):
    analysis_id: UUID
    tender_id: int
    bidder_id: int | None
    requested_by: int | None
    status: str
    overall_score: Decimal | None
    overall_status: str | None
    model_name: str | None
    model_version: str | None
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional


class ComplianceReportResult(BaseModel):
    result_id: int
    requirement_id: Optional[int] = None
    requirement_type: Optional[str] = None
    requirement_text: Optional[str] = None
    mandatory: Optional[bool] = None
    source_page: Optional[str] = None

    status: str
    score: Optional[float] = None
    explanation: Optional[str] = None
    evidence: Optional[str] = None
    ai_confidence: Optional[float] = None


class ComplianceReportResponse(BaseModel):
    analysis_id: str

    tender_id: int
    tender_title: Optional[str] = None
    bid_number: Optional[str] = None

    bidder_id: Optional[int] = None
    bidder_name: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None

    status: str
    overall_score: Optional[float] = None
    overall_status: Optional[str] = None

    model_name: Optional[str] = None
    model_version: Optional[str] = None

    results: list[ComplianceReportResult]