from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.assumption import Assumption
from src.schemas.assumption import AssumptionCreate, AssumptionUpdate, AssumptionResponse

router = APIRouter(prefix="/api/v1/projects/{project_id}/assumptions", tags=["assumptions"])


@router.get("", response_model=list[AssumptionResponse])
def list_assumptions(project_id: str, db: Session = Depends(get_db)):
    return db.query(Assumption).filter_by(project_id=project_id).order_by(Assumption.code).all()


@router.post("", response_model=AssumptionResponse)
def create_assumption(project_id: str, req: AssumptionCreate, db: Session = Depends(get_db)):
    a = Assumption(project_id=project_id, **req.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.put("/{assumption_id}", response_model=AssumptionResponse)
def update_assumption(project_id: str, assumption_id: str, req: AssumptionUpdate, db: Session = Depends(get_db)):
    a = db.query(Assumption).filter_by(id=assumption_id, project_id=project_id).first()
    if not a:
        raise HTTPException(404, "Assumption not found")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(a, field, value)
    db.commit()
    db.refresh(a)
    return a


@router.delete("/{assumption_id}")
def delete_assumption(project_id: str, assumption_id: str, db: Session = Depends(get_db)):
    a = db.query(Assumption).filter_by(id=assumption_id, project_id=project_id).first()
    if not a:
        raise HTTPException(404, "Assumption not found")
    db.delete(a)
    db.commit()
    return {"ok": True}
