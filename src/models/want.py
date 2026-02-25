import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class WantCriteria(Base):
    __tablename__ = "want_criteria"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    code: Mapped[str] = mapped_column(String(10))  # W1, W2, ...
    name: Mapped[str] = mapped_column(String(200))
    weight: Mapped[int] = mapped_column(Integer)  # 1-10
    score_10: Mapped[str] = mapped_column(Text, default="")
    score_6: Mapped[str] = mapped_column(Text, default="")
    score_2: Mapped[str] = mapped_column(Text, default="")
    evidence_type: Mapped[str] = mapped_column(String(100), default="")


class WantScore(Base):
    __tablename__ = "want_scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    alternative_id: Mapped[str] = mapped_column(String(36), ForeignKey("alternatives.id"))
    criteria_id: Mapped[str] = mapped_column(String(36), ForeignKey("want_criteria.id"))
    score: Mapped[int] = mapped_column(Integer)  # 1-10
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weighted_score: Mapped[int] = mapped_column(Integer, default=0)  # weight × score
