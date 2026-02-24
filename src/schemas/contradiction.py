from datetime import datetime

from pydantic import BaseModel


class ContradictionCreate(BaseModel):
    code: str
    improve_param: str
    worsen_param: str
    engineering_desc: str
    physical_contradiction: str = ""
    source: str = ""


class ContradictionResponse(BaseModel):
    id: str
    project_id: str
    code: str
    improve_param: str
    worsen_param: str
    engineering_desc: str
    physical_contradiction: str
    source: str
    created_at: datetime

    model_config = {"from_attributes": True}
