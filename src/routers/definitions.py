import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.definition import TaskDefinition
from src.models.project import Project
from src.schemas.definition import TaskDefinitionCreate, TaskDefinitionResponse, GenerateRequest
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/definitions", tags=["definitions"])


@router.get("", response_model=TaskDefinitionResponse | None)
def get_definition(project_id: str, db: Session = Depends(get_db)):
    return db.query(TaskDefinition).filter_by(project_id=project_id).first()


@router.put("", response_model=TaskDefinitionResponse)
def update_definition(project_id: str, req: TaskDefinitionCreate, db: Session = Depends(get_db)):
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        defn = TaskDefinition(project_id=project_id)
        db.add(defn)

    defn.mission = req.mission
    defn.hard_constraints = [c.model_dump() for c in req.hard_constraints]
    defn.soft_objectives = [o.model_dump() for o in req.soft_objectives]
    defn.non_goals = req.non_goals
    defn.critical_metrics = [m.model_dump() for m in req.critical_metrics]

    db.commit()
    db.refresh(defn)
    return defn


@router.post("/generate", response_model=TaskDefinitionResponse)
def generate_definition(project_id: str, req: GenerateRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    result = llm_service.generate(
        "task_definition.md",
        {"requirement_text": req.requirement_text, "constraints": req.constraints},
    )

    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        defn = TaskDefinition(project_id=project_id)
        db.add(defn)

    defn.mission = result.get("mission", "")
    defn.hard_constraints = result.get("hard_constraints", [])
    defn.soft_objectives = result.get("soft_objectives", [])
    defn.non_goals = result.get("non_goals", [])
    defn.critical_metrics = result.get("critical_metrics", [])

    # Update project status to PHASE_I
    if project.status == "DRAFT":
        project.status = "PHASE_I"

    db.commit()
    db.refresh(defn)
    return defn
