from datetime import datetime

from pydantic import BaseModel


class DataSourceCreate(BaseModel):
    source_name: str
    source_url: str | None = None
    source_type: str | None = None
    license: str | None = None
    dataset_version: str | None = None
    acquired_at: datetime | None = None
    notes: str | None = None


class DataSourceResponse(BaseModel):
    source_id: int
    source_name: str
    source_url: str | None
    source_type: str | None
    license: str | None
    dataset_version: str | None
    acquired_at: datetime | None
    notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True