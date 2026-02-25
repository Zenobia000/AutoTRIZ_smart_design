import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    assumption_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("assumptions.id"), nullable=True)
    goal: Mapped[str] = mapped_column(Text)
    question: Mapped[str] = mapped_column(Text)
    method: Mapped[str] = mapped_column(Text)
    success_criteria: Mapped[str] = mapped_column(Text, default="")
    failure_action: Mapped[str] = mapped_column(Text, default="")
    cost_cycle: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="planned")  # planned/in_progress/completed
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
