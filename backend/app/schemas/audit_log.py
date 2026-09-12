from datetime import datetime
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    audit_id: int
    user_id: int | None = None
    action: str
    entity_type: str | None = None
    entity_id: str | None = None
    description: str | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }