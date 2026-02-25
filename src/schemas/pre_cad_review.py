from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PreCadReviewCreate(BaseModel):
    alternative_id: str
    space_score: int = 0
    space_note: str = ""
    cost_score: int = 0
    cost_note: str = ""
    safety_score: int = 0
    safety_note: str = ""
    decoupling_score: int = 0
    decoupling_note: str = ""
    supply_score: int = 0
    supply_note: str = ""
    reviewer: str = ""


class PreCadReviewUpdate(BaseModel):
    space_score: Optional[int] = None
    space_note: Optional[str] = None
    cost_score: Optional[int] = None
    cost_note: Optional[str] = None
    safety_score: Optional[int] = None
    safety_note: Optional[str] = None
    decoupling_score: Optional[int] = None
    decoupling_note: Optional[str] = None
    supply_score: Optional[int] = None
    supply_note: Optional[str] = None
    reviewer: Optional[str] = None


class PreCadReviewResponse(BaseModel):
    id: str
    project_id: str
    alternative_id: str
    space_score: int
    space_note: str
    cost_score: int
    cost_note: str
    safety_score: int
    safety_note: str
    decoupling_score: int
    decoupling_note: str
    supply_score: int
    supply_note: str
    overall_pass: bool
    reviewer: str
    ai_analysis: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
