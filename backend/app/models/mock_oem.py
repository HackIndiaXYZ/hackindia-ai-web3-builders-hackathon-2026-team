from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MockOEM(Base):
    __tablename__ = "mock_oem"

    oem_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    bidder_id: Mapped[int] = mapped_column(
        ForeignKey("bidders.bidder_id", ondelete="CASCADE"),
        nullable=False
    )

    authorization_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    oem_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    authorization_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
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