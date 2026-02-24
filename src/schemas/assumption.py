from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssumptionCreate(BaseModel):
    code: str
    content: str
    assumption_type: str = ""
    source: str = ""
    worst_consequence: str = ""
    risk_level: str = "Medium"
    verification_method: str = ""
    acceptance_criteria: str = ""
    owner: str = ""
    due_date: str = ""


class AssumptionUpdate(BaseModel):
    content: Optional[str] = None
    assumption_type: Optional[str] = None
    source: Optional[str] = None
    worst_consequence: Optional[str] = None
    risk_level: Optional[str] = None
    verification_method: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None


class AssumptionResponse(BaseModel):
    id: str
    project_id: str
    code: str
    content: str
    assumption_type: str
    source: str
    worst_consequence: str
    risk_level: str
    verification_method: str
    acceptance_criteria: str
    owner: str
    due_date: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
