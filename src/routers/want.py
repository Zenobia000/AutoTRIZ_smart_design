from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.want import WantCriteria, WantScore
from src.schemas.want import WantCriteriaCreate, WantCriteriaResponse, WantScoreRequest, WantScoreResponse

router = APIRouter(prefix="/api/v1/projects/{project_id}/want", tags=["want"])


# --- WANT Criteria ---

@router.get("/criteria", response_model=list[WantCriteriaResponse])
def list_criteria(project_id: str, db: Session = Depends(get_db)):
    return db.query(WantCriteria).filter_by(project_id=project_id).order_by(WantCriteria.code).all()


@router.post("/criteria", response_model=WantCriteriaResponse)
def create_criteria(project_id: str, req: WantCriteriaCreate, db: Session = Depends(get_db)):
    c = WantCriteria(project_id=project_id, **req.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/criteria/{criteria_id}")
def delete_criteria(project_id: str, criteria_id: str, db: Session = Depends(get_db)):
    c = db.query(WantCriteria).filter_by(id=criteria_id, project_id=project_id).first()
    if not c:
        raise HTTPException(404, "WANT criteria not found")
    db.delete(c)
    db.commit()
    return {"ok": True}


# --- WANT Scores ---

@router.get("/scores", response_model=list[WantScoreResponse])
def list_scores(project_id: str, alternative_id: str | None = None, db: Session = Depends(get_db)):
    q = db.query(WantScore).filter_by(project_id=project_id)
    if alternative_id:
        q = q.filter_by(alternative_id=alternative_id)
    return q.all()


@router.post("/scores", response_model=WantScoreResponse)
def create_or_update_score(project_id: str, req: WantScoreRequest, db: Session = Depends(get_db)):
    # Get weight from criteria
    criteria = db.query(WantCriteria).filter_by(id=req.criteria_id, project_id=project_id).first()
    if not criteria:
        raise HTTPException(404, "WANT criteria not found")

    weighted = criteria.weight * req.score

    # Upsert
    score = db.query(WantScore).filter_by(
        project_id=project_id, alternative_id=req.alternative_id, criteria_id=req.criteria_id
    ).first()

    if not score:
        score = WantScore(
            project_id=project_id,
            alternative_id=req.alternative_id,
            criteria_id=req.criteria_id,
        )
        db.add(score)

    score.score = req.score
    score.evidence = req.evidence
    score.weighted_score = weighted

    db.commit()
    db.refresh(score)
    return score


@router.get("/totals")
def get_totals(project_id: str, db: Session = Depends(get_db)):
    """Get weighted total scores per alternative."""
    scores = db.query(WantScore).filter_by(project_id=project_id).all()
    totals: dict[str, int] = {}
    for s in scores:
        totals[s.alternative_id] = totals.get(s.alternative_id, 0) + s.weighted_score
    return totals
