from datetime import datetime

from pydantic import BaseModel


class GateCheckResponse(BaseModel):
    id: str
    project_id: str
    gate_id: str
    checklist: list
    overall_pass: bool
    checked_at: datetime

    model_config = {"from_attributes": True}
