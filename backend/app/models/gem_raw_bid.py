from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GemRawBid(Base):
    __tablename__ = "gem_raw_bids"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    bid_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    bid_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    bid_end_datetime: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    bid_opening_datetime: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    bid_offer_validity_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    ministry: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    department: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    organisation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    office: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    item_category: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    mse_relaxation: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    startup_relaxation: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    seller_documents_required: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    imported_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )