from typing import Optional

from pydantic import BaseModel


class WantCriteriaCreate(BaseModel):
    code: str
    name: str
    weight: int
    score_10: str = ""
    score_6: str = ""
    score_2: str = ""
    evidence_type: str = ""


class WantCriteriaResponse(BaseModel):
    id: str
    project_id: str
    code: str
    name: str
    weight: int
    score_10: str
    score_6: str
    score_2: str
    evidence_type: str

    model_config = {"from_attributes": True}


class WantScoreRequest(BaseModel):
    alternative_id: str
    criteria_id: str
    score: int
    evidence: Optional[str] = None


class WantScoreResponse(BaseModel):
    id: str
    project_id: str
    alternative_id: str
    criteria_id: str
    score: int
    evidence: Optional[str]
    weighted_score: int

    model_config = {"from_attributes": True}
