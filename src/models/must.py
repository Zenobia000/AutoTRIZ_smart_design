import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class MustEvaluation(Base):
    __tablename__ = "must_evaluations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    alternative_id: Mapped[str] = mapped_column(String(36), ForeignKey("alternatives.id"))
    results: Mapped[dict] = mapped_column(JSON, default=dict)  # {M1: true/false, M2: true/false, ...}
    overall_pass: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, default="")
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
