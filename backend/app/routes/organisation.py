from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.organisation import Organisation
from app.models.user import User
from app.schemas.organisation import (
    OrganisationCreate,
    OrganisationResponse
)


router = APIRouter(
    prefix="/organisations",
    tags=["Organisations"]
)


@router.post("/", response_model=OrganisationResponse)
def create_organisation(
    organisation: OrganisationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_organisation = (
        db.query(Organisation)
        .filter(
            Organisation.organisation_code
            == organisation.organisation_code
        )
        .first()
    )

    if (
        organisation.organisation_code
        and existing_organisation
    ):
        raise HTTPException(
            status_code=400,
            detail="Organisation code already exists"
        )

    new_organisation = Organisation(
        organisation_name=organisation.organisation_name,
        ministry=organisation.ministry,
        department=organisation.department,
        organisation_code=organisation.organisation_code,
        organisation_type=organisation.organisation_type,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_organisation)
    db.commit()
    db.refresh(new_organisation)

    return new_organisation


@router.get(
    "/",
    response_model=list[OrganisationResponse]
)
def get_organisations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Organisation).all()


@router.get(
    "/{organisation_id}",
    response_model=OrganisationResponse
)
def get_organisation(
    organisation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organisation = (
        db.query(Organisation)
        .filter(
            Organisation.organisation_id == organisation_id
        )
        .first()
    )

    if not organisation:
        raise HTTPException(
            status_code=404,
            detail="Organisation not found"
        )

    return organisation