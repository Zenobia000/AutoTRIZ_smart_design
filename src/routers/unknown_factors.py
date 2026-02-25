from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.unknown_factor import UnknownFactor
from src.schemas.unknown_factor import (
    UnknownFactorCreate, UnknownFactorUpdate, UnknownFactorResponse,
)

router = APIRouter(prefix="/api/v1/projects/{project_id}/unknown-factors", tags=["unknown-factors"])


@router.get("", response_model=list[UnknownFactorResponse])
def list_unknown_factors(project_id: str, db: Session = Depends(get_db)):
    return db.query(UnknownFactor).filter_by(project_id=project_id).order_by(UnknownFactor.code).all()


@router.post("", response_model=UnknownFactorResponse)
def create_unknown_factor(project_id: str, req: UnknownFactorCreate, db: Session = Depends(get_db)):
    uf = UnknownFactor(project_id=project_id, **req.model_dump())
    db.add(uf)
    db.commit()
    db.refresh(uf)
    return uf


@router.put("/{factor_id}", response_model=UnknownFactorResponse)
def update_unknown_factor(project_id: str, factor_id: str, req: UnknownFactorUpdate, db: Session = Depends(get_db)):
    uf = db.query(UnknownFactor).filter_by(id=factor_id, project_id=project_id).first()
    if not uf:
        raise HTTPException(404, "Unknown factor not found")
    for k, v in req.model_dump(exclude_none=True).items():
        setattr(uf, k, v)
    db.commit()
    db.refresh(uf)
    return uf


@router.delete("/{factor_id}")
def delete_unknown_factor(project_id: str, factor_id: str, db: Session = Depends(get_db)):
    uf = db.query(UnknownFactor).filter_by(id=factor_id, project_id=project_id).first()
    if not uf:
        raise HTTPException(404, "Unknown factor not found")
    db.delete(uf)
    db.commit()
    return {"ok": True}
