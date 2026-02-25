import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class SeparationSolution(Base):
    __tablename__ = "separation_solutions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    contradiction_id: Mapped[str] = mapped_column(String(36), ForeignKey("contradictions.id"))
    separation_type: Mapped[str] = mapped_column(String(20))    # time, space, condition, whole_part
    separation_name: Mapped[str] = mapped_column(String(50))     # 時間分離, 空間分離, ...
    strategy: Mapped[str] = mapped_column(Text)
    engineering_mappings: Mapped[dict] = mapped_column(JSON, default=list)
    cost_description: Mapped[str] = mapped_column(Text, default="")
    experiment_desc: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
