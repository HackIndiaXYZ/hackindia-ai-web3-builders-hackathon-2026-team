from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Bidder(Base):
    __tablename__ = "bidders"

    bidder_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    gstin: Mapped[str | None] = mapped_column(
        String(30),
        unique=True,
        nullable=True
    )

    pan: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    contact_person: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    source_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )