import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.pre_cad_review import PreCadReview
from src.models.alternative import Alternative
from src.models.definition import TaskDefinition
from src.schemas.pre_cad_review import PreCadReviewCreate, PreCadReviewUpdate, PreCadReviewResponse
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/pre-cad-reviews", tags=["pre-cad-reviews"])

DIMENSIONS = ["space", "cost", "safety", "decoupling", "supply"]


def _calc_overall_pass(review) -> bool:
    scores = [getattr(review, f"{d}_score") for d in DIMENSIONS]
    return all(s >= 3 for s in scores) and all(s > 0 for s in scores)


@router.get("", response_model=list[PreCadReviewResponse])
def list_reviews(project_id: str, db: Session = Depends(get_db)):
    return db.query(PreCadReview).filter_by(project_id=project_id).all()


@router.post("", response_model=PreCadReviewResponse)
def create_review(project_id: str, req: PreCadReviewCreate, db: Session = Depends(get_db)):
    r = PreCadReview(project_id=project_id, **req.model_dump())
    r.overall_pass = _calc_overall_pass(r)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.put("/{review_id}", response_model=PreCadReviewResponse)
def update_review(project_id: str, review_id: str, req: PreCadReviewUpdate, db: Session = Depends(get_db)):
    r = db.query(PreCadReview).filter_by(id=review_id, project_id=project_id).first()
    if not r:
        raise HTTPException(404, "Pre-CAD review not found")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    r.overall_pass = _calc_overall_pass(r)
    db.commit()
    db.refresh(r)
    return r


@router.post("/{review_id}/ai-analyze", response_model=PreCadReviewResponse)
def ai_analyze(project_id: str, review_id: str, db: Session = Depends(get_db)):
    r = db.query(PreCadReview).filter_by(id=review_id, project_id=project_id).first()
    if not r:
        raise HTTPException(404, "Pre-CAD review not found")

    alt = db.query(Alternative).filter_by(id=r.alternative_id).first()
    if not alt:
        raise HTTPException(404, "Alternative not found")

    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()

    result = llm_service.generate(
        "pre_cad_review.md",
        {
            "alternative_code": alt.code,
            "alternative_name": alt.name,
            "mechanism": json.dumps(alt.mechanism or {}, ensure_ascii=False),
            "robust_scores": json.dumps(alt.robust_scores or {}, ensure_ascii=False),
            "mission": defn.mission if defn else "",
            "hard_constraints": json.dumps(defn.hard_constraints if defn else [], ensure_ascii=False),
            "risks": json.dumps(alt.risks or {}, ensure_ascii=False),
            "assumptions": json.dumps(alt.assumptions or [], ensure_ascii=False),
        },
    )

    if isinstance(result, dict):
        for dim in DIMENSIONS:
            if dim in result:
                setattr(r, f"{dim}_score", result[dim].get("score", 0))
                setattr(r, f"{dim}_note", result[dim].get("note", ""))
        r.ai_analysis = result.get("summary", "")
        r.overall_pass = _calc_overall_pass(r)

    db.commit()
    db.refresh(r)
    return r


@router.delete("/{review_id}")
def delete_review(project_id: str, review_id: str, db: Session = Depends(get_db)):
    r = db.query(PreCadReview).filter_by(id=review_id, project_id=project_id).first()
    if not r:
        raise HTTPException(404, "Pre-CAD review not found")
    db.delete(r)
    db.commit()
    return {"ok": True}
