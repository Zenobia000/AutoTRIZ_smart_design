import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, JSON, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class GateCheck(Base):
    __tablename__ = "gate_checks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    gate_number: Mapped[int] = mapped_column(Integer)  # 1, 2, 3
    checklist: Mapped[dict] = mapped_column(JSON, default=list)  # [{item, passed, note}]
    overall_pass: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
