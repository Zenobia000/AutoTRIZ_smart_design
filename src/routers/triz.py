import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.triz import TrizSolution
from src.models.contradiction import Contradiction
from src.models.definition import TaskDefinition
from src.schemas.triz import TrizSolutionResponse, TrizGenerateRequest
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/triz", tags=["triz"])


@router.get("", response_model=list[TrizSolutionResponse])
def list_triz(project_id: str, db: Session = Depends(get_db)):
    return db.query(TrizSolution).filter_by(project_id=project_id).all()


@router.post("/generate", response_model=list[TrizSolutionResponse])
def generate_triz(project_id: str, req: TrizGenerateRequest, db: Session = Depends(get_db)):
    contradiction = db.query(Contradiction).filter_by(id=req.contradiction_id, project_id=project_id).first()
    if not contradiction:
        raise HTTPException(404, "Contradiction not found")

    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    constraints = json.dumps(defn.hard_constraints, ensure_ascii=False) if defn else ""

    contradiction_text = (
        f"{contradiction.code}: 若要提高「{contradiction.improve_param}」，"
        f"則「{contradiction.worsen_param}」會惡化。{contradiction.engineering_desc}"
    )

    result = llm_service.generate(
        "triz_solution.md",
        {"contradiction": contradiction_text, "constraints": constraints},
    )

    solutions = []
    for item in result:
        s = TrizSolution(
            project_id=project_id,
            contradiction_id=contradiction.id,
            principle_number=item["principle_number"],
            principle_name=item["principle_name"],
            abstract_strategy=item["abstract_strategy"],
            engineering_mappings=item.get("engineering_mappings", []),
            cost_description=item.get("cost_description", ""),
            robust_estimate=item.get("robust_estimate", {}),
            experiment_desc=item.get("experiment_desc", ""),
        )
        db.add(s)
        solutions.append(s)

    db.commit()
    for s in solutions:
        db.refresh(s)
    return solutions


@router.delete("/{triz_id}")
def delete_triz(project_id: str, triz_id: str, db: Session = Depends(get_db)):
    s = db.query(TrizSolution).filter_by(id=triz_id, project_id=project_id).first()
    if not s:
        raise HTTPException(404, "TRIZ solution not found")
    db.delete(s)
    db.commit()
    return {"ok": True}
