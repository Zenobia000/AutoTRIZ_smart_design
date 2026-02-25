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


# --- Unified TRIZ Solve schemas ---

class ParamMapping(BaseModel):
    triz_id: int
    triz_name: str
    confidence: str


class ContradictionClassification(BaseModel):
    types: list[str]
    sufield_state: str | None = None
    reasoning: str = ""


class SeparationSolutionResponse(BaseModel):
    id: str
    project_id: str
    contradiction_id: str
    separation_type: str
    separation_name: str
    strategy: str
    engineering_mappings: list
    cost_description: str
    experiment_desc: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SuFieldSolutionResponse(BaseModel):
    id: str
    project_id: str
    contradiction_id: str
    standard_code: str
    standard_name: str
    sufield_model: str
    engineering_mappings: list
    cost_description: str
    experiment_desc: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UnifiedTrizResult(BaseModel):
    contradiction_id: str
    classification: ContradictionClassification
    param_mapping: dict | None = None
    matrix_lookup: list[int] | None = None
    technical_solutions: list[TrizSolutionResponse] = []
    separation_solutions: list[SeparationSolutionResponse] = []
    sufield_solutions: list[SuFieldSolutionResponse] = []
