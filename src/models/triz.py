import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TrizSolution(Base):
    __tablename__ = "triz_solutions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    contradiction_id: Mapped[str] = mapped_column(String(36), ForeignKey("contradictions.id"))
    principle_number: Mapped[int] = mapped_column(Integer)
    principle_name: Mapped[str] = mapped_column(String(100))
    abstract_strategy: Mapped[str] = mapped_column(Text)
    engineering_mappings: Mapped[dict] = mapped_column(JSON, default=list)  # [string]
    cost_description: Mapped[str] = mapped_column(Text, default="")
    robust_estimate: Mapped[dict] = mapped_column(JSON, default=dict)  # {margin, decoupling, recoverability}
    experiment_desc: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
