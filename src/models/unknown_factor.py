import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UnknownFactor(Base):
    """未知集合 (U) — 已知會變動但不確定如何變動的因子"""
    __tablename__ = "unknown_factors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    code: Mapped[str] = mapped_column(String(10))  # U-001, U-002
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50), default="")  # 環境/使用者行為/製程/材料/供應/介面
    levels: Mapped[dict] = mapped_column(JSON, default=list)  # ["低","中","高"]
    range_desc: Mapped[str] = mapped_column(String(200), default="")  # e.g. "-20°C ~ +55°C"
    impact_on: Mapped[str] = mapped_column(Text, default="")  # 影響哪些指標
    related_assumptions: Mapped[str] = mapped_column(Text, default="")  # e.g. "A-001, A-003"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
