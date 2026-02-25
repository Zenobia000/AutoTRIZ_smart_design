from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# --- CausalLoop ---

class CausalLoopCreate(BaseModel):
    name: str = ""
    nodes: list = []
    edges: list = []
    description: str = ""


class CausalLoopUpdate(BaseModel):
    name: Optional[str] = None
    nodes: Optional[list] = None
    edges: Optional[list] = None
    description: Optional[str] = None


class CausalLoopResponse(BaseModel):
    id: str
    project_id: str
    name: str
    nodes: list
    edges: list
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Breakpoint ---

class BreakpointCreate(BaseModel):
    code: str
    causal_loop_id: str = ""
    location: str
    description: str = ""
    solution_direction: str = ""
    triz_principles: str = ""


class BreakpointUpdate(BaseModel):
    location: Optional[str] = None
    description: Optional[str] = None
    solution_direction: Optional[str] = None
    triz_principles: Optional[str] = None


class BreakpointResponse(BaseModel):
    id: str
    project_id: str
    causal_loop_id: str
    code: str
    location: str
    description: str
    solution_direction: str
    triz_principles: str
    created_at: datetime

    model_config = {"from_attributes": True}
