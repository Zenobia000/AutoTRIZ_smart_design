import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class PreCadReview(Base):
    __tablename__ = "pre_cad_reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    alternative_id: Mapped[str] = mapped_column(String(36), ForeignKey("alternatives.id"))
    space_score: Mapped[int] = mapped_column(Integer, default=0)
    space_note: Mapped[str] = mapped_column(Text, default="")
    cost_score: Mapped[int] = mapped_column(Integer, default=0)
    cost_note: Mapped[str] = mapped_column(Text, default="")
    safety_score: Mapped[int] = mapped_column(Integer, default=0)
    safety_note: Mapped[str] = mapped_column(Text, default="")
    decoupling_score: Mapped[int] = mapped_column(Integer, default=0)
    decoupling_note: Mapped[str] = mapped_column(Text, default="")
    supply_score: Mapped[int] = mapped_column(Integer, default=0)
    supply_note: Mapped[str] = mapped_column(Text, default="")
    overall_pass: Mapped[bool] = mapped_column(Boolean, default=False)
    reviewer: Mapped[str] = mapped_column(String(100), default="")
    ai_analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
