from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DecisionRecordResponse(BaseModel):
    id: str
    project_id: str
    statement: str
    must_results: dict
    want_results: dict
    ac_results: list
    primary_choice: Optional[str]
    primary_reason: str
    backup_choice: Optional[str]
    backup_reason: str
    action_items: list
    signed_by: Optional[str]
    signed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SignoffRequest(BaseModel):
    signed_by: str
