import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class SuFieldSolution(Base):
    __tablename__ = "sufield_solutions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    contradiction_id: Mapped[str] = mapped_column(String(36), ForeignKey("contradictions.id"))
    standard_code: Mapped[str] = mapped_column(String(10))      # "1.2.1"
    standard_name: Mapped[str] = mapped_column(String(100))
    sufield_model: Mapped[str] = mapped_column(Text)             # "S1=碟盤, S2=卡鉗, F=液壓"
    engineering_mappings: Mapped[dict] = mapped_column(JSON, default=list)
    cost_description: Mapped[str] = mapped_column(Text, default="")
    experiment_desc: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
