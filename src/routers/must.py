from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.must import MustEvaluation
from src.models.alternative import Alternative
from src.schemas.must import MustEvaluateRequest, MustEvaluationResponse

router = APIRouter(prefix="/api/v1/projects/{project_id}/must", tags=["must"])


@router.get("", response_model=list[MustEvaluationResponse])
def list_must_evaluations(project_id: str, db: Session = Depends(get_db)):
    return db.query(MustEvaluation).filter_by(project_id=project_id).all()


@router.post("/evaluate", response_model=MustEvaluationResponse)
def evaluate_must(project_id: str, req: MustEvaluateRequest, db: Session = Depends(get_db)):
    alt = db.query(Alternative).filter_by(id=req.alternative_id, project_id=project_id).first()
    if not alt:
        raise HTTPException(404, "Alternative not found")

    overall_pass = all(req.results.values())

    # Update or create evaluation
    ev = db.query(MustEvaluation).filter_by(
        project_id=project_id, alternative_id=req.alternative_id
    ).first()
    if not ev:
        ev = MustEvaluation(project_id=project_id, alternative_id=req.alternative_id)
        db.add(ev)

    ev.results = req.results
    ev.overall_pass = overall_pass
    ev.notes = req.notes

    # Update alternative status
    alt.status = "must_pass" if overall_pass else "must_fail"

    db.commit()
    db.refresh(ev)
    return ev
