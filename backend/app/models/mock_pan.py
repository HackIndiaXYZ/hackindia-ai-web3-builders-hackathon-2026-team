from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MockPAN(Base):
    __tablename__ = "mock_pan"

    pan_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    bidder_id: Mapped[int] = mapped_column(
        ForeignKey("bidders.bidder_id", ondelete="CASCADE"),
        nullable=False
    )

    pan: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    legal_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    pan_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    income_tax_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    last_return_filed: Mapped[datetime | None] = mapped_column(
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