from datetime import datetime

from pydantic import BaseModel


class DocumentContentResponse(BaseModel):
    content_id: int
    document_id: int
    extracted_text: str | None
    extraction_status: str
    extracted_at: datetime | None
    extraction_error: str | None

    class Config:
        from_attributes = True