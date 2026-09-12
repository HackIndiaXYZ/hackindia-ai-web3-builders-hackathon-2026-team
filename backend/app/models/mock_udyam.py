from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MockUdyam(Base):
    __tablename__ = "mock_udyam"

    udyam_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    bidder_id: Mapped[int] = mapped_column(
        ForeignKey("bidders.bidder_id", ondelete="CASCADE"),
        nullable=False
    )

    udyam_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    enterprise_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    enterprise_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    registration_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    registration_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    valid_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )