from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from uuid import UUID


class ComplianceResultCreate(BaseModel):
    analysis_id: UUID
    requirement_id: int | None = None
    status: str
    score: Decimal | None = None
    explanation: str | None = None
    evidence: str | None = None
    ai_confidence: Decimal | None = None


class ComplianceResultResponse(BaseModel):
    result_id: int
    analysis_id: UUID
    requirement_id: int | None
    status: str
    score: Decimal | None
    explanation: str | None
    evidence: str | None
    ai_confidence: Decimal | None
    created_at: datetime

    class Config:
        from_attributes = True