from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Tender(Base):
    __tablename__ = "tenders"

    tender_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    organisation_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "organisations.organisation_id",
            ondelete="SET NULL"
        ),
     nullable=True
    )
    bid_number: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    tender_title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    item_category: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    tender_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    estimated_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True
    )

    quantity: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4),
        nullable=True
    )

    bid_start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    bid_end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    bid_opening_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    tender_status: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    procurement_mode: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    source_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    source_record_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )