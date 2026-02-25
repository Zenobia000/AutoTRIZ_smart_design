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


STANDARD_CRITERIA = [
    {"code": "W1", "name": "性能餘裕", "weight": 10, "score_10": "超越目標 >20%", "score_6": "達到目標", "score_2": "低於目標 >10%", "evidence_type": "仿真/實測"},
    {"code": "W2", "name": "製造可行性", "weight": 8, "score_10": "成熟製程，良率 >95%", "score_6": "需微調製程", "score_2": "需全新製程開發", "evidence_type": "DFM 報告"},
    {"code": "W3", "name": "成本競爭力", "weight": 7, "score_10": "低於目標成本 >10%", "score_6": "達到目標成本", "score_2": "超過目標 >15%", "evidence_type": "BOM 估算"},
    {"code": "W4", "name": "開發時程", "weight": 6, "score_10": "可提前 >2 週", "score_6": "準時", "score_2": "延遲 >2 週", "evidence_type": "排程評估"},
    {"code": "W5", "name": "解耦程度", "weight": 8, "score_10": "完全獨立，無耦合", "score_6": "弱耦合，可管理", "score_2": "強耦合，牽一髮動全身", "evidence_type": "架構分析"},
    {"code": "W6", "name": "驗證難度", "weight": 5, "score_10": "桌面分析即可確認", "score_6": "需原型驗證", "score_2": "需全尺寸/長期試驗", "evidence_type": "實驗計畫"},
]


@router.post("/criteria/seed", response_model=list[WantCriteriaResponse])
def seed_criteria(project_id: str, db: Session = Depends(get_db)):
    """Create standard W1-W6 criteria. Idempotent guard: 409 if criteria already exist."""
    existing = db.query(WantCriteria).filter_by(project_id=project_id).count()
    if existing > 0:
        raise HTTPException(409, f"Project already has {existing} criteria")

    created = []
    for c in STANDARD_CRITERIA:
        wc = WantCriteria(project_id=project_id, **c)
        db.add(wc)
        created.append(wc)
    db.commit()
    for wc in created:
        db.refresh(wc)
    return created


@router.get("/totals")
def get_totals(project_id: str, db: Session = Depends(get_db)):
    """Get weighted total scores per alternative."""
    scores = db.query(WantScore).filter_by(project_id=project_id).all()
    totals: dict[str, int] = {}
    for s in scores:
        totals[s.alternative_id] = totals.get(s.alternative_id, 0) + s.weighted_score
    return totals
