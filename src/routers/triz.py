import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.triz import TrizSolution
from src.models.separation_solution import SeparationSolution
from src.models.sufield_solution import SuFieldSolution
from src.models.contradiction import Contradiction
from src.models.definition import TaskDefinition
from src.schemas.triz import (
    TrizSolutionResponse, TrizGenerateRequest, UnifiedTrizResult,
    SeparationSolutionResponse, SuFieldSolutionResponse,
    ContradictionClassification,
)
from src.services.llm_service import llm_service
from src.services.triz_solve_service import triz_solve_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/triz", tags=["triz"])


@router.get("", response_model=list[TrizSolutionResponse])
def list_triz(project_id: str, db: Session = Depends(get_db)):
    return db.query(TrizSolution).filter_by(project_id=project_id).all()


@router.post("/solve", response_model=UnifiedTrizResult)
def solve_triz(project_id: str, req: TrizGenerateRequest, db: Session = Depends(get_db)):
    """Unified TRIZ solve: classify → 3-path route → grounded solutions."""
    contradiction = db.query(Contradiction).filter_by(
        id=req.contradiction_id, project_id=project_id
    ).first()
    if not contradiction:
        raise HTTPException(404, "Contradiction not found")

    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    constraints = json.dumps(defn.hard_constraints, ensure_ascii=False) if defn else ""

    result = triz_solve_service.solve(contradiction, constraints, db)

    return UnifiedTrizResult(
        contradiction_id=contradiction.id,
        classification=ContradictionClassification(**result["classification"]),
        param_mapping=result["param_mapping"],
        matrix_lookup=result["matrix_lookup"],
        technical_solutions=[TrizSolutionResponse.model_validate(s) for s in result["technical_solutions"]],
        separation_solutions=[SeparationSolutionResponse.model_validate(s) for s in result["separation_solutions"]],
        sufield_solutions=[SuFieldSolutionResponse.model_validate(s) for s in result["sufield_solutions"]],
    )


@router.get("/result/{contradiction_id}", response_model=UnifiedTrizResult)
def get_triz_result(project_id: str, contradiction_id: str, db: Session = Depends(get_db)):
    """Get unified result for a previously solved contradiction."""
    contradiction = db.query(Contradiction).filter_by(
        id=contradiction_id, project_id=project_id
    ).first()
    if not contradiction:
        raise HTTPException(404, "Contradiction not found")

    tc = db.query(TrizSolution).filter_by(
        project_id=project_id, contradiction_id=contradiction_id
    ).all()
    sep = db.query(SeparationSolution).filter_by(
        project_id=project_id, contradiction_id=contradiction_id
    ).all()
    sf = db.query(SuFieldSolution).filter_by(
        project_id=project_id, contradiction_id=contradiction_id
    ).all()

    classification = ContradictionClassification(
        types=contradiction.contradiction_types or [],
        sufield_state=contradiction.sufield_state or None,
    )

    return UnifiedTrizResult(
        contradiction_id=contradiction_id,
        classification=classification,
        param_mapping=None,  # Not persisted, only available at solve time
        matrix_lookup=None,
        technical_solutions=tc,
        separation_solutions=sep,
        sufield_solutions=sf,
    )


@router.post("/generate", response_model=list[TrizSolutionResponse], deprecated=True)
def generate_triz(project_id: str, req: TrizGenerateRequest, db: Session = Depends(get_db)):
    """Legacy endpoint — use /solve instead."""
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
