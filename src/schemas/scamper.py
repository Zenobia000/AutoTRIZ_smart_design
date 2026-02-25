from datetime import datetime

from pydantic import BaseModel


class ScamperVariantResponse(BaseModel):
    id: str
    project_id: str
    subsystem: str
    action: str
    target: str
    mechanism: str
    failure_mode: str
    supply_risk: str
    assumptions: str
    verification: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ScamperGenerateRequest(BaseModel):
    subsystem: str
    constraints: str = ""
