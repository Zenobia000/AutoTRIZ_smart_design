from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UnknownFactorCreate(BaseModel):
    code: str
    name: str
    category: str = ""
    levels: list = []
    range_desc: str = ""
    impact_on: str = ""
    related_assumptions: str = ""


class UnknownFactorUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    levels: Optional[list] = None
    range_desc: Optional[str] = None
    impact_on: Optional[str] = None
    related_assumptions: Optional[str] = None


class UnknownFactorResponse(BaseModel):
    id: str
    project_id: str
    code: str
    name: str
    category: str
    levels: list
    range_desc: str
    impact_on: str
    related_assumptions: str
    created_at: datetime

    model_config = {"from_attributes": True}
