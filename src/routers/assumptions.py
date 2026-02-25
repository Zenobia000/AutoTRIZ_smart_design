import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.alternative import Alternative
from src.models.assumption import Assumption
from src.models.causal_loop import Breakpoint, CausalLoop
from src.models.contradiction import Contradiction
from src.models.definition import TaskDefinition
from src.models.question import SocraticQuestion
from src.models.triz import TrizSolution
from src.schemas.assumption import (
    AssumptionCreate,
    AssumptionExtractResponse,
    AssumptionResponse,
    AssumptionUpdate,
    DisproveRequest,
    DisproveResponse,
    ImpactItem,
)
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/assumptions", tags=["assumptions"])

AI_SOURCE_TAG = "AI 萃取"


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


@router.post("/extract", response_model=AssumptionExtractResponse)
def extract_assumptions(project_id: str, db: Session = Depends(get_db)):
    """Batch-extract assumptions from all upstream artifacts using LLM."""
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        raise HTTPException(400, "Task definition not found — complete Step 1 first")

    questions = db.query(SocraticQuestion).filter_by(project_id=project_id).all()
    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    breakpoints = db.query(Breakpoint).filter_by(project_id=project_id).all()
    causal_loops = db.query(CausalLoop).filter_by(project_id=project_id).all()

    # Format upstream artifacts for prompt injection
    qa_history = "\n".join(
        f"Q({q.category}): {q.question}\nA: {q.answer or '(未回答)'}" for q in questions
    ) or "(無問答記錄)"

    contra_text = "\n".join(
        f"- {c.code}: 改善「{c.improve_param}」vs 惡化「{c.worsen_param}」— {c.engineering_desc}"
        + (f"\n  物理矛盾: {c.physical_contradiction}" if c.physical_contradiction else "")
        for c in contradictions
    ) or "(無矛盾)"

    bp_text = "\n".join(
        f"- {b.code}: {b.location} — {b.description}"
        + (f"\n  解法方向: {b.solution_direction}" if b.solution_direction else "")
        for b in breakpoints
    ) or "(無斷路點)"

    loop_text = "\n".join(
        f"- {loop.name}: {loop.description}" for loop in causal_loops
    ) or "(無因果迴路)"

    result = llm_service.generate(
        "assumption_extract.md",
        {
            "mission": defn.mission,
            "hard_constraints": json.dumps(defn.hard_constraints, ensure_ascii=False),
            "qa_history": qa_history,
            "contradictions": contra_text,
            "breakpoints": bp_text,
            "causal_loops": loop_text,
        },
    )

    # Delete old AI-extracted assumptions only; keep manual ones
    db.query(Assumption).filter_by(project_id=project_id, source=AI_SOURCE_TAG).delete()

    # Auto-number: find max existing code number
    existing = db.query(Assumption).filter_by(project_id=project_id).all()
    max_num = 0
    for a in existing:
        try:
            num = int(a.code.split("-")[1])
            if num > max_num:
                max_num = num
        except (IndexError, ValueError):
            pass

    assumptions = []
    for i, item in enumerate(result, start=1):
        a = Assumption(
            project_id=project_id,
            code=f"A-{max_num + i:03d}",
            content=item["content"],
            assumption_type=item.get("assumption_type", ""),
            source=AI_SOURCE_TAG,
            worst_consequence=item.get("worst_consequence", ""),
            risk_level=item.get("risk_level", "Medium"),
            verification_method=item.get("verification_method", ""),
            acceptance_criteria=item.get("acceptance_criteria", ""),
            source_refs=item.get("source_refs", []),
        )
        db.add(a)
        assumptions.append(a)

    db.commit()
    for a in assumptions:
        db.refresh(a)

    return AssumptionExtractResponse(extracted_count=len(assumptions), assumptions=assumptions)


@router.post("/{assumption_id}/disprove", response_model=DisproveResponse)
def disprove_assumption(
    project_id: str, assumption_id: str, req: DisproveRequest, db: Session = Depends(get_db)
):
    """Mark an assumption as disproved and perform impact analysis."""
    a = db.query(Assumption).filter_by(id=assumption_id, project_id=project_id).first()
    if not a:
        raise HTTPException(404, "Assumption not found")
    if a.status == "Disproved":
        raise HTTPException(400, "Assumption already disproved")

    a.status = "Disproved"
    a.disproved_reason = req.reason
    a.disproved_at = datetime.now(timezone.utc)

    # Impact analysis: trace from source_refs to affected artifacts
    impact: list[ImpactItem] = []
    actions: list[str] = []

    # 1. Find affected contradictions via source_refs
    affected_contradiction_ids = set()
    for ref in (a.source_refs or []):
        if ref.get("type") == "contradiction" and ref.get("id"):
            affected_contradiction_ids.add(ref["id"])
        elif ref.get("type") == "contradiction" and ref.get("code"):
            c = db.query(Contradiction).filter_by(
                project_id=project_id, code=ref["code"]
            ).first()
            if c:
                affected_contradiction_ids.add(c.id)

    for cid in affected_contradiction_ids:
        c = db.query(Contradiction).filter_by(id=cid).first()
        if c:
            impact.append(ImpactItem(
                type="contradiction", code=c.code, id=c.id,
                description=c.engineering_desc[:100],
            ))
            actions.append(f"重新評估矛盾 {c.code} 的 TRIZ 解法")

        # 2. Find TRIZ solutions linked to this contradiction
        triz_solutions = db.query(TrizSolution).filter_by(contradiction_id=cid).all()
        for ts in triz_solutions:
            impact.append(ImpactItem(
                type="triz_solution", code=ts.principle_name or "", id=ts.id,
                description=f"TRIZ 原理 #{ts.principle_number}: {ts.principle_name}",
            ))

    # 3. Find alternatives that reference this assumption
    alternatives = db.query(Alternative).filter_by(project_id=project_id).all()
    for alt in alternatives:
        alt_assumptions = alt.assumptions or []
        if a.id in alt_assumptions or a.code in alt_assumptions:
            impact.append(ImpactItem(
                type="alternative", code=alt.code, id=alt.id,
                description=f"方案「{alt.name}」依賴此假設",
            ))
            actions.append(f"重新評估方案 {alt.code}「{alt.name}」的前提")

    if not actions:
        actions.append("此假設無直接關聯的下游工件，建議記錄為 Lessons Learned")

    db.commit()
    db.refresh(a)

    return DisproveResponse(
        assumption=a,
        impact_analysis=impact,
        recommended_actions=actions,
    )


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
