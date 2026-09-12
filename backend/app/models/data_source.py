from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    source_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    source_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    source_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    license: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    dataset_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    acquired_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )