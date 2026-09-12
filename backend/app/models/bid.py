from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Bid(Base):
    __tablename__ = "bids"

    bid_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenders.tender_id",
            ondelete="CASCADE"
        ),
      nullable=False
     )

    bidder_id: Mapped[int] = mapped_column(
        ForeignKey(
            "bidders.bidder_id",
            ondelete="CASCADE"
        ),
     nullable=False
    )

    bid_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True
    )

    bid_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    bid_status: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    is_winner: Mapped[bool | None] = mapped_column(
        Boolean,
        default=False,
        nullable=True
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )