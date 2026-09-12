from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.data_source import DataSource
from app.models.user import User
from app.schemas.data_source import (
    DataSourceCreate,
    DataSourceResponse
)


router = APIRouter(
    prefix="/data-sources",
    tags=["Data Sources"]
)


@router.post("/", response_model=DataSourceResponse)
def create_data_source(
    source: DataSourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_source = DataSource(
        source_name=source.source_name,
        source_url=source.source_url,
        source_type=source.source_type,
        license=source.license,
        dataset_version=source.dataset_version,
        acquired_at=source.acquired_at,
        notes=source.notes,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_source)
    db.commit()
    db.refresh(new_source)

    return new_source


@router.get(
    "/",
    response_model=list[DataSourceResponse]
)
def get_data_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(DataSource).all()


@router.get(
    "/{source_id}",
    response_model=DataSourceResponse
)
def get_data_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    source = (
        db.query(DataSource)
        .filter(DataSource.source_id == source_id)
        .first()
    )

    if not source:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Data source not found"
        )

    return source