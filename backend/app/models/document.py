from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    tender_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "tenders.tender_id",
            ondelete="CASCADE"
        ),
     nullable=True
    )

    uploaded_by: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL"
            ),
        nullable=True
    )

    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    document_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )