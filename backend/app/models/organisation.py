from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    organisation_id: Mapped[int] = mapped_column(primary_key=True)

    organisation_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ministry: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    department: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    organisation_code: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    organisation_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )