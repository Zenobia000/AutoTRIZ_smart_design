import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class DecisionRecord(Base):
    __tablename__ = "decision_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    statement: Mapped[str] = mapped_column(Text, default="")
    must_results: Mapped[dict] = mapped_column(JSON, default=dict)  # {passed: [], eliminated: [{alt, reason}]}
    want_results: Mapped[dict] = mapped_column(JSON, default=dict)  # {alt_id: total_score, ...}
    ac_results: Mapped[dict] = mapped_column(JSON, default=list)  # [{alt, risk, level, mitigation}]
    primary_choice: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    primary_reason: Mapped[str] = mapped_column(Text, default="")
    backup_choice: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    backup_reason: Mapped[str] = mapped_column(Text, default="")
    action_items: Mapped[dict] = mapped_column(JSON, default=list)  # [{task, owner, due}]
    signed_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
