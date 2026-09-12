import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ComplianceAnalysis(Base):
    __tablename__ = "compliance_analyses"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.tender_id", ondelete="CASCADE"),
        nullable=False
    )

    bidder_id: Mapped[int | None] = mapped_column(
        ForeignKey("bidders.bidder_id", ondelete="SET NULL"),
        nullable=True
    )

    requested_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
    )

    overall_score: Mapped[Decimal | None] = mapped_column(
        Numeric(6, 2),
        nullable=True
    )

    overall_status: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    model_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    model_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )