from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.risk import Risk
from src.schemas.risk import RiskCreate, RiskUpdate, RiskResponse

RISK_MATRIX = {
    ("H", "H"): "H*", ("H", "M"): "H", ("H", "L"): "M",
    ("M", "H"): "H", ("M", "M"): "M", ("M", "L"): "L",
    ("L", "H"): "M", ("L", "M"): "L", ("L", "L"): "L",
}

router = APIRouter(prefix="/api/v1/projects/{project_id}/risks", tags=["risks"])


@router.get("", response_model=list[RiskResponse])
def list_risks(project_id: str, alternative_id: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Risk).filter_by(project_id=project_id)
    if alternative_id:
        q = q.filter_by(alternative_id=alternative_id)
    return q.all()


@router.post("", response_model=RiskResponse)
def create_risk(project_id: str, req: RiskCreate, db: Session = Depends(get_db)):
    level = RISK_MATRIX.get((req.probability, req.severity), "M")
    r = Risk(project_id=project_id, level=level, **req.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.put("/{risk_id}", response_model=RiskResponse)
def update_risk(project_id: str, risk_id: str, req: RiskUpdate, db: Session = Depends(get_db)):
    r = db.query(Risk).filter_by(id=risk_id, project_id=project_id).first()
    if not r:
        raise HTTPException(404, "Risk not found")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    # Recalculate level
    r.level = RISK_MATRIX.get((r.probability, r.severity), "M")
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{risk_id}")
def delete_risk(project_id: str, risk_id: str, db: Session = Depends(get_db)):
    r = db.query(Risk).filter_by(id=risk_id, project_id=project_id).first()
    if not r:
        raise HTTPException(404, "Risk not found")
    db.delete(r)
    db.commit()
    return {"ok": True}
