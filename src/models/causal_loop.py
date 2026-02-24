import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

from src.database import Base


class CausalLoop(Base):
    """因果迴路圖 — 節點與邊的結構化表達"""
    __tablename__ = "causal_loops"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(200), default="")  # e.g. "熱-機-振 耦合迴路"
    nodes: Mapped[dict] = mapped_column(JSON, default=list)  # [{id, label}]
    edges: Mapped[dict] = mapped_column(JSON, default=list)  # [{from, to, polarity: "+"/"-", label}]
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Breakpoint(Base):
    """斷路點 — 因果迴路中可介入切斷耦合的位置"""
    __tablename__ = "breakpoints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    causal_loop_id: Mapped[str] = mapped_column(String(36), ForeignKey("causal_loops.id"), default="")
    code: Mapped[str] = mapped_column(String(10))  # BP-001, BP-002
    location: Mapped[str] = mapped_column(String(200))  # e.g. "馬達-減速機界面"
    description: Mapped[str] = mapped_column(Text, default="")  # 斷路點說明
    solution_direction: Mapped[str] = mapped_column(Text, default="")  # 可能解法方向
    triz_principles: Mapped[str] = mapped_column(Text, default="")  # TRIZ 原理提示, e.g. "#1分割, #2分離"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
