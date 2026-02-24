import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Contradiction(Base):
    __tablename__ = "contradictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    code: Mapped[str] = mapped_column(String(10))  # C1, C2, ...
    improve_param: Mapped[str] = mapped_column(Text)
    worsen_param: Mapped[str] = mapped_column(Text)
    engineering_desc: Mapped[str] = mapped_column(Text)
    physical_contradiction: Mapped[str] = mapped_column(Text, default="")
    source: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
