from datetime import datetime

from pydantic import BaseModel


class OfficerDecisionCreate(BaseModel):
    analysis_id: str
    decision: str
    remarks: str | None = None


class OfficerDecisionResponse(BaseModel):
    decision_id: int
    analysis_id: str
    officer_id: int
    decision: str
    remarks: str | None = None
    decided_at: datetime

    model_config = {
        "from_attributes": True
    }