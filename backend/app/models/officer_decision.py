from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class OfficerDecision(Base):
    __tablename__ = "officer_decisions"

    decision_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    analysis_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    officer_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    decision: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    decided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )