from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HardConstraint(BaseModel):
    name: str
    value: str
    source: str = ""


class SoftObjective(BaseModel):
    name: str
    direction: str


class CriticalMetric(BaseModel):
    name: str
    target: str
    method: str


class TaskDefinitionCreate(BaseModel):
    mission: str
    hard_constraints: list[HardConstraint] = []
    soft_objectives: list[SoftObjective] = []
    non_goals: list[str] = []
    critical_metrics: list[CriticalMetric] = []


class TaskDefinitionResponse(BaseModel):
    id: str
    project_id: str
    mission: str
    hard_constraints: list
    soft_objectives: list
    non_goals: list
    critical_metrics: list
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class GenerateRequest(BaseModel):
    requirement_text: str
    constraints: str = ""
