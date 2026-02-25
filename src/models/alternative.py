import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Alternative(Base):
    __tablename__ = "alternatives"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    code: Mapped[str] = mapped_column(String(20))  # 方案 A, 方案 B, ...
    name: Mapped[str] = mapped_column(String(200))
    source: Mapped[str] = mapped_column(Text, default="")  # TRIZ#X + SCAMPER-Y
    mechanism: Mapped[dict] = mapped_column(JSON, default=dict)  # {physical_principle, structure, key_dimensions}
    assumptions: Mapped[dict] = mapped_column(JSON, default=list)  # [assumption_ids]
    risks: Mapped[dict] = mapped_column(JSON, default=dict)  # {failure_modes, process_risk, supply_risk}
    robust_scores: Mapped[dict] = mapped_column(JSON, default=dict)  # {margin, decoupling, recoverability, complexity, sensitivity}
    status: Mapped[str] = mapped_column(String(20), default="candidate")  # candidate/must_pass/must_fail/selected/backup/eliminated
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
