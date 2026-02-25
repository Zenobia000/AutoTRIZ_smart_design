from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AlternativeCreate(BaseModel):
    code: str
    name: str
    source: str = ""
    mechanism: dict = {}
    assumptions: list = []
    risks: dict = {}
    robust_scores: dict = {}


class AlternativeUpdate(BaseModel):
    name: Optional[str] = None
    source: Optional[str] = None
    mechanism: Optional[dict] = None
    assumptions: Optional[list] = None
    risks: Optional[dict] = None
    robust_scores: Optional[dict] = None
    status: Optional[str] = None


class AlternativeResponse(BaseModel):
    id: str
    project_id: str
    code: str
    name: str
    source: str
    mechanism: dict
    assumptions: list
    risks: dict
    robust_scores: dict
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
