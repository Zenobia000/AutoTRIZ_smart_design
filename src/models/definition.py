import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TaskDefinition(Base):
    __tablename__ = "task_definitions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    mission: Mapped[str] = mapped_column(Text, default="")
    hard_constraints: Mapped[dict] = mapped_column(JSON, default=list)  # [{name, value, source}]
    soft_objectives: Mapped[dict] = mapped_column(JSON, default=list)  # [{name, direction}]
    non_goals: Mapped[dict] = mapped_column(JSON, default=list)  # [string]
    critical_metrics: Mapped[dict] = mapped_column(JSON, default=list)  # [{name, target, method}]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
