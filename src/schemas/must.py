from datetime import datetime

from pydantic import BaseModel


class MustEvaluateRequest(BaseModel):
    alternative_id: str
    results: dict  # {M1: true/false, M2: true/false, ...}
    notes: str = ""


class MustEvaluationResponse(BaseModel):
    id: str
    project_id: str
    alternative_id: str
    results: dict
    overall_pass: bool
    notes: str
    evaluated_at: datetime

    model_config = {"from_attributes": True}
