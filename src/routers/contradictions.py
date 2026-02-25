import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.contradiction import Contradiction
from src.models.definition import TaskDefinition
from src.models.question import SocraticQuestion
from src.schemas.contradiction import ContradictionCreate, ContradictionResponse
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/contradictions", tags=["contradictions"])


@router.get("", response_model=list[ContradictionResponse])
def list_contradictions(project_id: str, db: Session = Depends(get_db)):
    return db.query(Contradiction).filter_by(project_id=project_id).order_by(Contradiction.code).all()


@router.post("", response_model=ContradictionResponse)
def create_contradiction(project_id: str, req: ContradictionCreate, db: Session = Depends(get_db)):
    c = Contradiction(project_id=project_id, **req.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.post("/identify", response_model=list[ContradictionResponse])
def identify_contradictions(project_id: str, db: Session = Depends(get_db)):
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        raise HTTPException(400, "Task definition not found")

    questions = db.query(SocraticQuestion).filter_by(project_id=project_id).all()
    qa_history = "\n".join(
        f"Q({q.category}): {q.question}\nA: {q.answer or '(未回答)'}" for q in questions
    )

    result = llm_service.generate(
        "contradiction_identify.md",
        {
            "mission": defn.mission,
            "hard_constraints": json.dumps(defn.hard_constraints, ensure_ascii=False),
            "qa_history": qa_history or "(無問答記錄)",
        },
    )

    # Clear old contradictions
    db.query(Contradiction).filter_by(project_id=project_id).delete()

    contradictions = []
    for item in result:
        c = Contradiction(
            project_id=project_id,
            code=item["code"],
            improve_param=item["improve_param"],
            worsen_param=item["worsen_param"],
            engineering_desc=item["engineering_desc"],
            physical_contradiction=item.get("physical_contradiction", ""),
            source=item.get("source", ""),
        )
        db.add(c)
        contradictions.append(c)

    db.commit()
    for c in contradictions:
        db.refresh(c)
    return contradictions


@router.delete("/{contradiction_id}")
def delete_contradiction(project_id: str, contradiction_id: str, db: Session = Depends(get_db)):
    c = db.query(Contradiction).filter_by(id=contradiction_id, project_id=project_id).first()
    if not c:
        raise HTTPException(404, "Contradiction not found")
    db.delete(c)
    db.commit()
    return {"ok": True}
