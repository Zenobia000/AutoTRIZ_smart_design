import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    alternative_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("alternatives.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    risk_type: Mapped[str] = mapped_column(String(50))  # technical/process/supply/integration/verification/production
    probability: Mapped[str] = mapped_column(String(5))  # L/M/H
    severity: Mapped[str] = mapped_column(String(5))  # L/M/H
    level: Mapped[str] = mapped_column(String(5))  # L/M/H/H*
    owner: Mapped[str] = mapped_column(String(100), default="")
    mitigation: Mapped[str] = mapped_column(Text, default="")
    residual_risk: Mapped[str] = mapped_column(Text, default="")
    monitor: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
