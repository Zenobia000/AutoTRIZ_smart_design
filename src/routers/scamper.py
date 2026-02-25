import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.scamper import ScamperVariant
from src.models.definition import TaskDefinition
from src.models.contradiction import Contradiction
from src.models.causal_loop import Breakpoint
from src.models.triz import TrizSolution
from src.schemas.scamper import ScamperVariantResponse, ScamperGenerateRequest
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/scamper", tags=["scamper"])

SCAMPER_SOURCE_TAG = "SCAMPER 發現"


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
            new_contradictions=item.get("new_contradictions", []),
        )
        db.add(v)
        variants.append(v)

    db.commit()
    for v in variants:
        db.refresh(v)
    return variants


@router.post("/feedback-contradictions")
def feedback_contradictions(project_id: str, db: Session = Depends(get_db)):
    """Collect new contradictions discovered by SCAMPER and create Contradiction records."""
    variants = db.query(ScamperVariant).filter_by(project_id=project_id).all()
    existing = db.query(Contradiction).filter_by(project_id=project_id).all()
    existing_descs = {c.engineering_desc for c in existing}

    # Find max existing code number
    max_num = 0
    for c in existing:
        try:
            num = int(c.code.replace("C", ""))
            if num > max_num:
                max_num = num
        except (ValueError, IndexError):
            pass

    created = []
    seen_descs = set()
    for v in variants:
        for nc in (v.new_contradictions or []):
            desc = nc.get("engineering_desc", "")
            if not desc or desc in existing_descs or desc in seen_descs:
                continue
            seen_descs.add(desc)
            max_num += 1
            c = Contradiction(
                project_id=project_id,
                code=f"C{max_num}",
                improve_param=nc.get("improve", ""),
                worsen_param=nc.get("worsen", ""),
                engineering_desc=desc,
                source=SCAMPER_SOURCE_TAG,
            )
            db.add(c)
            created.append(c)

    db.commit()
    for c in created:
        db.refresh(c)

    return {"created_count": len(created), "contradictions": [
        {"id": c.id, "code": c.code, "engineering_desc": c.engineering_desc}
        for c in created
    ]}


@router.get("/subsystem-suggestions")
def suggest_subsystems(project_id: str, db: Session = Depends(get_db)):
    """Suggest subsystem names from breakpoints and TRIZ engineering mappings."""
    breakpoints = db.query(Breakpoint).filter_by(project_id=project_id).all()
    triz = db.query(TrizSolution).filter_by(project_id=project_id).all()

    suggestions = set()
    for bp in breakpoints:
        if bp.location:
            suggestions.add(bp.location)
    for ts in triz:
        for mapping in (ts.engineering_mappings or []):
            if isinstance(mapping, str) and len(mapping) < 30:
                suggestions.add(mapping)

    return sorted(suggestions)


@router.delete("/{scamper_id}")
def delete_scamper(project_id: str, scamper_id: str, db: Session = Depends(get_db)):
    v = db.query(ScamperVariant).filter_by(id=scamper_id, project_id=project_id).first()
    if not v:
        raise HTTPException(404, "SCAMPER variant not found")
    db.delete(v)
    db.commit()
    return {"ok": True}
