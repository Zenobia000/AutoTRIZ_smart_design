from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: str
    project_id: str
    category: str
    question: str
    answer: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AnswerRequest(BaseModel):
    answer: str
