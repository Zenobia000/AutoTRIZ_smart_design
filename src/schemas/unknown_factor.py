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
    assumption_refs: list[dict] = []  # [{"assumption_id": "uuid", "code": "A-001"}]


class UnknownFactorUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    levels: Optional[list] = None
    range_desc: Optional[str] = None
    impact_on: Optional[str] = None
    assumption_refs: Optional[list[dict]] = None


class UnknownFactorResponse(BaseModel):
    id: str
    project_id: str
    code: str
    name: str
    category: str
    levels: list
    range_desc: str
    impact_on: str
    assumption_refs: list[dict] = []
    created_at: datetime

    model_config = {"from_attributes": True}
