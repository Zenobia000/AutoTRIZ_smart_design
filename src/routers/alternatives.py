import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.alternative import Alternative
from src.models.triz import TrizSolution
from src.models.scamper import ScamperVariant
from src.models.assumption import Assumption
from src.models.definition import TaskDefinition
from src.schemas.alternative import AlternativeCreate, AlternativeUpdate, AlternativeResponse
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/alternatives", tags=["alternatives"])


@router.get("", response_model=list[AlternativeResponse])
def list_alternatives(project_id: str, db: Session = Depends(get_db)):
    return db.query(Alternative).filter_by(project_id=project_id).order_by(Alternative.code).all()


@router.post("", response_model=AlternativeResponse)
def create_alternative(project_id: str, req: AlternativeCreate, db: Session = Depends(get_db)):
    a = Alternative(project_id=project_id, **req.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.put("/{alt_id}", response_model=AlternativeResponse)
def update_alternative(project_id: str, alt_id: str, req: AlternativeUpdate, db: Session = Depends(get_db)):
    a = db.query(Alternative).filter_by(id=alt_id, project_id=project_id).first()
    if not a:
        raise HTTPException(404, "Alternative not found")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(a, field, value)
    db.commit()
    db.refresh(a)
    return a


@router.post("/generate", response_model=list[AlternativeResponse])
def generate_alternatives(project_id: str, db: Session = Depends(get_db)):
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    constraints = json.dumps(defn.hard_constraints, ensure_ascii=False) if defn else ""

    triz = db.query(TrizSolution).filter_by(project_id=project_id).all()
    scamper = db.query(ScamperVariant).filter_by(project_id=project_id).all()
    assumptions = db.query(Assumption).filter_by(project_id=project_id).all()

    triz_text = json.dumps([
        {"principle": f"#{s.principle_number} {s.principle_name}", "strategy": s.abstract_strategy,
         "mappings": s.engineering_mappings}
        for s in triz
    ], ensure_ascii=False)

    scamper_text = json.dumps([
        {"action": v.action, "target": v.target, "mechanism": v.mechanism}
        for v in scamper
    ], ensure_ascii=False)

    assumptions_text = json.dumps([
        {"code": a.code, "content": a.content} for a in assumptions
    ], ensure_ascii=False)

    result = llm_service.generate(
        "alternative_generate.md",
        {
            "triz_solutions": triz_text,
            "scamper_variants": scamper_text,
            "constraints": constraints,
            "assumptions": assumptions_text,
        },
    )

    alts = []
    for item in result:
        a = Alternative(
            project_id=project_id,
            code=item["code"],
            name=item["name"],
            source=item.get("source", ""),
            mechanism=item.get("mechanism", {}),
            assumptions=item.get("assumptions", []),
            risks=item.get("risks", {}),
            robust_scores=item.get("robust_scores", {}),
        )
        db.add(a)
        alts.append(a)

    db.commit()
    for a in alts:
        db.refresh(a)
    return alts


@router.delete("/{alt_id}")
def delete_alternative(project_id: str, alt_id: str, db: Session = Depends(get_db)):
    a = db.query(Alternative).filter_by(id=alt_id, project_id=project_id).first()
    if not a:
        raise HTTPException(404, "Alternative not found")
    db.delete(a)
    db.commit()
    return {"ok": True}
