import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.decision import DecisionRecord
from src.models.definition import TaskDefinition
from src.models.alternative import Alternative
from src.models.must import MustEvaluation
from src.models.want import WantScore
from src.models.risk import Risk
from src.schemas.decision import DecisionRecordResponse, SignoffRequest
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/decisions", tags=["decisions"])


@router.get("", response_model=DecisionRecordResponse | None)
def get_decision(project_id: str, db: Session = Depends(get_db)):
    return db.query(DecisionRecord).filter_by(project_id=project_id).first()


@router.post("/generate", response_model=DecisionRecordResponse)
def generate_decision(project_id: str, db: Session = Depends(get_db)):
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        raise HTTPException(400, "Task definition not found")

    alts = db.query(Alternative).filter_by(project_id=project_id).all()
    must_evals = db.query(MustEvaluation).filter_by(project_id=project_id).all()
    scores = db.query(WantScore).filter_by(project_id=project_id).all()
    risks = db.query(Risk).filter_by(project_id=project_id).all()

    # Build context
    must_results_text = json.dumps({
        "passed": [e.alternative_id for e in must_evals if e.overall_pass],
        "eliminated": [{"alt": e.alternative_id, "reason": e.notes} for e in must_evals if not e.overall_pass],
    }, ensure_ascii=False)

    totals: dict[str, int] = {}
    for s in scores:
        totals[s.alternative_id] = totals.get(s.alternative_id, 0) + s.weighted_score
    want_results_text = json.dumps(totals, ensure_ascii=False)

    risk_results_text = json.dumps([
        {"alt": r.alternative_id, "risk": r.description, "level": r.level, "mitigation": r.mitigation}
        for r in risks
    ], ensure_ascii=False)

    alts_text = json.dumps([
        {"code": a.code, "name": a.name, "status": a.status} for a in alts
    ], ensure_ascii=False)

    result = llm_service.generate(
        "decision_record.md",
        {
            "mission": defn.mission,
            "must_results": must_results_text,
            "want_results": want_results_text,
            "risk_results": risk_results_text,
            "alternatives": alts_text,
        },
    )

    dr = db.query(DecisionRecord).filter_by(project_id=project_id).first()
    if not dr:
        dr = DecisionRecord(project_id=project_id)
        db.add(dr)

    dr.statement = result.get("statement", "")
    dr.must_results = result.get("must_results", {})
    dr.want_results = result.get("want_results", {})
    dr.ac_results = result.get("ac_results", [])
    dr.primary_choice = result.get("primary_choice")
    dr.primary_reason = result.get("primary_reason", "")
    dr.backup_choice = result.get("backup_choice")
    dr.backup_reason = result.get("backup_reason", "")
    dr.action_items = result.get("action_items", [])

    db.commit()
    db.refresh(dr)
    return dr


@router.put("/signoff", response_model=DecisionRecordResponse)
def signoff_decision(project_id: str, req: SignoffRequest, db: Session = Depends(get_db)):
    dr = db.query(DecisionRecord).filter_by(project_id=project_id).first()
    if not dr:
        raise HTTPException(404, "Decision record not found")
    dr.signed_by = req.signed_by
    dr.signed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(dr)
    return dr
