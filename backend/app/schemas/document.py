from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    tender_id: int | None = None
    filename: str
    file_path: str
    document_type: str | None = None
    mime_type: str | None = None
    source_url: str | None = None


class DocumentResponse(BaseModel):
    document_id: int
    tender_id: int | None
    uploaded_by: int | None
    filename: str
    file_path: str
    document_type: str | None
    mime_type: str | None
    source_url: str | None
    uploaded_at: datetime

    class Config:
        from_attributes = True