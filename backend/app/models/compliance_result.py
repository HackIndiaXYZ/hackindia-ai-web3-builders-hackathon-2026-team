from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import DateTime, ForeignKey, Numeric, String,Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    result_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("compliance_analyses.analysis_id", ondelete="CASCADE"),
        nullable=False
    )

    requirement_id: Mapped[int | None] = mapped_column(
        ForeignKey("compliance_requirements.requirement_id", ondelete="SET NULL"),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    score: Mapped[Decimal | None] = mapped_column(
        Numeric(6, 2),
        nullable=True
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    evidence: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    ai_confidence: Mapped[Decimal | None] = mapped_column(
        Numeric(6, 2),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )