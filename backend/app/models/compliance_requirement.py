from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ComplianceRequirement(Base):
    __tablename__ = "compliance_requirements"

    requirement_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenders.tender_id",
            ondelete="CASCADE"
        ),
     nullable=False
    )

    document_id: Mapped[int | None] = mapped_column(
    ForeignKey(
        "documents.document_id",
        ondelete="SET NULL"
    ),
    nullable=True
    )

    requirement_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    requirement_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    mandatory: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    source_page: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )