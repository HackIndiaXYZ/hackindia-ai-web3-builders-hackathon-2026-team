from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DocumentContent(Base):
    __tablename__ = "document_contents"

    content_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.document_id",
            ondelete="CASCADE"
        ),
     unique=True,
     nullable=False
    )

    extracted_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    extraction_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
    )

    extracted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    extraction_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )