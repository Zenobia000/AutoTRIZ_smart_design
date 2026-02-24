import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ScamperVariant(Base):
    __tablename__ = "scamper_variants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    subsystem: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(1))  # S/C/A/M/P/E/R
    target: Mapped[str] = mapped_column(Text)
    mechanism: Mapped[str] = mapped_column(Text)
    failure_mode: Mapped[str] = mapped_column(Text, default="")
    supply_risk: Mapped[str] = mapped_column(Text, default="")
    assumptions: Mapped[str] = mapped_column(Text, default="")
    verification: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
