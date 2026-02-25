from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExperimentCreate(BaseModel):
    assumption_id: Optional[str] = None
    goal: str
    question: str
    method: str
    success_criteria: str = ""
    failure_action: str = ""
    cost_cycle: str = ""


class ExperimentUpdate(BaseModel):
    status: Optional[str] = None
    result: Optional[str] = None


class ExperimentResponse(BaseModel):
    id: str
    project_id: str
    assumption_id: Optional[str]
    goal: str
    question: str
    method: str
    success_criteria: str
    failure_action: str
    cost_cycle: str
    status: str
    result: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
