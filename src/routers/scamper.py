import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.scamper import ScamperVariant
from src.models.definition import TaskDefinition
from src.models.contradiction import Contradiction
from src.schemas.scamper import ScamperVariantResponse, ScamperGenerateRequest
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/scamper", tags=["scamper"])


@router.get("", response_model=list[ScamperVariantResponse])
def list_scamper(project_id: str, db: Session = Depends(get_db)):
    return db.query(ScamperVariant).filter_by(project_id=project_id).all()


@router.post("/generate", response_model=list[ScamperVariantResponse])
def generate_scamper(project_id: str, req: ScamperGenerateRequest, db: Session = Depends(get_db)):
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    constraints = json.dumps(defn.hard_constraints, ensure_ascii=False) if defn else ""

    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    contradictions_text = "\n".join(
        f"{c.code}: {c.engineering_desc}" for c in contradictions
    ) or "(無)"

    result = llm_service.generate(
        "scamper_variant.md",
        {
            "subsystem": req.subsystem,
            "constraints": constraints or req.constraints,
            "contradictions": contradictions_text,
        },
    )

    variants = []
    for item in result:
        v = ScamperVariant(
            project_id=project_id,
            subsystem=req.subsystem,
            action=item["action"],
            target=item["target"],
            mechanism=item["mechanism"],
            failure_mode=item.get("failure_mode", ""),
            supply_risk=item.get("supply_risk", ""),
            assumptions=item.get("assumptions", ""),
            verification=item.get("verification", ""),
        )
        db.add(v)
        variants.append(v)

    db.commit()
    for v in variants:
        db.refresh(v)
    return variants


@router.delete("/{scamper_id}")
def delete_scamper(project_id: str, scamper_id: str, db: Session = Depends(get_db)):
    v = db.query(ScamperVariant).filter_by(id=scamper_id, project_id=project_id).first()
    if not v:
        raise HTTPException(404, "SCAMPER variant not found")
    db.delete(v)
    db.commit()
    return {"ok": True}
