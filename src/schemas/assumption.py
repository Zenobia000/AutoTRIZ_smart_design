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
    source_refs: list[dict] = []


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
    disproved_reason: Optional[str] = None


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
    source_refs: list[dict] = []
    disproved_reason: str = ""
    disproved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssumptionExtractResponse(BaseModel):
    extracted_count: int
    assumptions: list[AssumptionResponse]


class DisproveRequest(BaseModel):
    reason: str


class ImpactItem(BaseModel):
    type: str        # "contradiction" | "triz_solution" | "alternative"
    code: str
    id: str
    description: str


class DisproveResponse(BaseModel):
    assumption: AssumptionResponse
    impact_analysis: list[ImpactItem]
    recommended_actions: list[str]
