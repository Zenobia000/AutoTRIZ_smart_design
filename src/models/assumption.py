import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Assumption(Base):
    __tablename__ = "assumptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    code: Mapped[str] = mapped_column(String(10))  # A-001, A-002, ...
    content: Mapped[str] = mapped_column(Text)
    assumption_type: Mapped[str] = mapped_column(String(50), default="")  # 介面/包絡, 系統邊界/架構, 可靠度/壽命, NVH/體驗, 環境可靠度, 低溫性能, 製程/DFM, 成本
    source: Mapped[str] = mapped_column(String(100), default="")  # 規格需求, 案例/競品, 工程常識, 初算/推估, 供應商資料
    worst_consequence: Mapped[str] = mapped_column(Text, default="")
    risk_level: Mapped[str] = mapped_column(String(20), default="Medium")  # High, Medium-High, Medium, Low
    verification_method: Mapped[str] = mapped_column(Text, default="")
    acceptance_criteria: Mapped[str] = mapped_column(Text, default="")
    owner: Mapped[str] = mapped_column(String(100), default="")
    due_date: Mapped[str] = mapped_column(String(50), default="")  # e.g. "Gate 1.2 前", "Phase Gate 1 前"
    status: Mapped[str] = mapped_column(String(20), default="Open")  # Open/Planned/Verifying/Verified/Disproved
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
