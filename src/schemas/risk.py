from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RiskCreate(BaseModel):
    alternative_id: Optional[str] = None
    description: str
    risk_type: str
    probability: str  # L/M/H
    severity: str  # L/M/H
    owner: str = ""
    mitigation: str = ""
    residual_risk: str = ""
    monitor: str = ""


class RiskUpdate(BaseModel):
    description: Optional[str] = None
    risk_type: Optional[str] = None
    probability: Optional[str] = None
    severity: Optional[str] = None
    owner: Optional[str] = None
    mitigation: Optional[str] = None
    residual_risk: Optional[str] = None
    monitor: Optional[str] = None


class RiskResponse(BaseModel):
    id: str
    project_id: str
    alternative_id: Optional[str]
    description: str
    risk_type: str
    probability: str
    severity: str
    level: str
    owner: str
    mitigation: str
    residual_risk: str
    monitor: str
    created_at: datetime

    model_config = {"from_attributes": True}
