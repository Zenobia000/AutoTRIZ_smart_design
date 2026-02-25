import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.alternative import Alternative
from src.models.triz import TrizSolution
from src.models.scamper import ScamperVariant
from src.models.assumption import Assumption
from src.models.contradiction import Contradiction
from src.models.causal_loop import Breakpoint
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


@router.post("/anti-anchor", response_model=list[AlternativeResponse])
def anti_anchor_sprint(project_id: str, db: Session = Depends(get_db)):
    """Generate 3 non-conventional architecture concepts to break path dependency."""
    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    if not contradictions:
        raise HTTPException(400, "No contradictions found — complete Step 1.3 first")

    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    constraints = json.dumps(defn.hard_constraints, ensure_ascii=False) if defn else ""

    breakpoints = db.query(Breakpoint).filter_by(project_id=project_id).all()
    triz = db.query(TrizSolution).filter_by(project_id=project_id).all()

    contradictions_text = "\n".join(
        f"{c.code}: 改善「{c.improve_param}」vs 惡化「{c.worsen_param}」— {c.engineering_desc}"
        for c in contradictions
    )
    breakpoints_text = "\n".join(
        f"{bp.code}: {bp.location} — {bp.description}" for bp in breakpoints
    ) or "(無斷路點)"
    existing_solutions = "\n".join(
        f"#{s.principle_number} {s.principle_name}: {', '.join(s.engineering_mappings or [])}"
        for s in triz
    ) or "(無現有解法)"

    result = llm_service.generate(
        "anti_anchor_sprint.md",
        {
            "constraints": constraints,
            "contradictions": contradictions_text,
            "breakpoints": breakpoints_text,
            "existing_solutions": existing_solutions,
        },
    )

    alts = []
    for item in result:
        a = Alternative(
            project_id=project_id,
            code=item.get("code", f"AA-{len(alts)+1}"),
            name=item["name"],
            source=item.get("source", "Anti-Anchor Sprint"),
            mechanism=item.get("mechanism", {}),
            assumptions=item.get("assumptions", []),
            risks=item.get("risks", {}),
            robust_scores=item.get("robust_scores", {}),
            status="anti_anchor",
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
