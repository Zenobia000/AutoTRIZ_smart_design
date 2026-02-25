from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.experiment import Experiment
from src.schemas.experiment import ExperimentCreate, ExperimentUpdate, ExperimentResponse

router = APIRouter(prefix="/api/v1/projects/{project_id}/experiments", tags=["experiments"])


@router.get("", response_model=list[ExperimentResponse])
def list_experiments(project_id: str, db: Session = Depends(get_db)):
    return db.query(Experiment).filter_by(project_id=project_id).all()


@router.post("", response_model=ExperimentResponse)
def create_experiment(project_id: str, req: ExperimentCreate, db: Session = Depends(get_db)):
    e = Experiment(project_id=project_id, **req.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@router.put("/{experiment_id}", response_model=ExperimentResponse)
def update_experiment(project_id: str, experiment_id: str, req: ExperimentUpdate, db: Session = Depends(get_db)):
    e = db.query(Experiment).filter_by(id=experiment_id, project_id=project_id).first()
    if not e:
        raise HTTPException(404, "Experiment not found")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(e, field, value)
    db.commit()
    db.refresh(e)
    return e


@router.delete("/{experiment_id}")
def delete_experiment(project_id: str, experiment_id: str, db: Session = Depends(get_db)):
    e = db.query(Experiment).filter_by(id=experiment_id, project_id=project_id).first()
    if not e:
        raise HTTPException(404, "Experiment not found")
    db.delete(e)
    db.commit()
    return {"ok": True}
