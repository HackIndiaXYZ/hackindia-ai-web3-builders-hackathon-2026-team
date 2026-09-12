from datetime import datetime

from pydantic import BaseModel


class OrganisationCreate(BaseModel):
    organisation_name: str
    ministry: str | None = None
    department: str | None = None
    organisation_code: str | None = None
    organisation_type: str | None = None


class OrganisationResponse(BaseModel):
    organisation_id: int
    organisation_name: str
    ministry: str | None
    department: str | None
    organisation_code: str | None
    organisation_type: str | None
    created_at: datetime

    class Config:
        from_attributes = True