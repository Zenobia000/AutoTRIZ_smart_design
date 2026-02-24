from datetime import datetime

from pydantic import BaseModel


class TrizSolutionResponse(BaseModel):
    id: str
    project_id: str
    contradiction_id: str
    principle_number: int
    principle_name: str
    abstract_strategy: str
    engineering_mappings: list
    cost_description: str
    robust_estimate: dict
    experiment_desc: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TrizGenerateRequest(BaseModel):
    contradiction_id: str
