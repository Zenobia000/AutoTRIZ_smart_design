import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.causal_loop import CausalLoop, Breakpoint
from src.models.definition import TaskDefinition
from src.models.question import SocraticQuestion
from src.models.contradiction import Contradiction
from src.schemas.causal_loop import (
    CausalLoopCreate, CausalLoopUpdate, CausalLoopResponse,
    BreakpointCreate, BreakpointUpdate, BreakpointResponse,
)
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}", tags=["causal-loops"])


# ── AI Generate ──

@router.post("/causal-loops/generate")
def generate_causal_loops(project_id: str, db: Session = Depends(get_db)):
    """AI 根據任務定義、索克拉底問答、矛盾句，自動建立因果迴路圖與斷路點。"""
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        raise HTTPException(400, "Task definition not found")

    questions = db.query(SocraticQuestion).filter_by(project_id=project_id).all()
    qa_history = "\n".join(
        f"Q({q.category}): {q.question}\nA: {q.answer or '(未回答)'}" for q in questions
    )

    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    contradictions_text = "\n".join(
        f"{c.code}: 改善 {c.improve_param} → 惡化 {c.worsen_param} | {c.engineering_desc}"
        for c in contradictions
    ) or "(尚無矛盾)"

    result = llm_service.generate(
        "causal_loop_generate.md",
        {
            "mission": defn.mission,
            "hard_constraints": json.dumps(defn.hard_constraints, ensure_ascii=False),
            "critical_metrics": json.dumps(defn.critical_metrics, ensure_ascii=False),
            "qa_history": qa_history or "(無問答記錄)",
            "contradictions": contradictions_text,
        },
    )

    # Clear old data
    db.query(Breakpoint).filter_by(project_id=project_id).delete()
    db.query(CausalLoop).filter_by(project_id=project_id).delete()

    # Save causal loops
    created_loops = []
    for item in result.get("causal_loops", []):
        cl = CausalLoop(
            project_id=project_id,
            name=item.get("name", ""),
            description=item.get("description", ""),
            nodes=item.get("nodes", []),
            edges=item.get("edges", []),
        )
        db.add(cl)
        db.flush()
        created_loops.append(cl)

    # Save breakpoints
    created_bps = []
    first_loop_id = created_loops[0].id if created_loops else ""
    for item in result.get("breakpoints", []):
        bp = Breakpoint(
            project_id=project_id,
            causal_loop_id=first_loop_id,
            code=item.get("code", ""),
            location=item.get("location", ""),
            description=item.get("description", ""),
            solution_direction=item.get("solution_direction", ""),
            triz_principles=item.get("triz_principles", ""),
        )
        db.add(bp)
        created_bps.append(bp)

    db.commit()
    for cl in created_loops:
        db.refresh(cl)
    for bp in created_bps:
        db.refresh(bp)

    return {
        "causal_loops": [CausalLoopResponse.model_validate(cl).model_dump() for cl in created_loops],
        "breakpoints": [BreakpointResponse.model_validate(bp).model_dump() for bp in created_bps],
    }


# ── CausalLoop CRUD ──

@router.get("/causal-loops", response_model=list[CausalLoopResponse])
def list_causal_loops(project_id: str, db: Session = Depends(get_db)):
    return db.query(CausalLoop).filter_by(project_id=project_id).all()


@router.post("/causal-loops", response_model=CausalLoopResponse)
def create_causal_loop(project_id: str, req: CausalLoopCreate, db: Session = Depends(get_db)):
    cl = CausalLoop(project_id=project_id, **req.model_dump())
    db.add(cl)
    db.commit()
    db.refresh(cl)
    return cl


@router.put("/causal-loops/{loop_id}", response_model=CausalLoopResponse)
def update_causal_loop(project_id: str, loop_id: str, req: CausalLoopUpdate, db: Session = Depends(get_db)):
    cl = db.query(CausalLoop).filter_by(id=loop_id, project_id=project_id).first()
    if not cl:
        raise HTTPException(404, "Causal loop not found")
    for k, v in req.model_dump(exclude_none=True).items():
        setattr(cl, k, v)
    db.commit()
    db.refresh(cl)
    return cl


@router.delete("/causal-loops/{loop_id}")
def delete_causal_loop(project_id: str, loop_id: str, db: Session = Depends(get_db)):
    cl = db.query(CausalLoop).filter_by(id=loop_id, project_id=project_id).first()
    if not cl:
        raise HTTPException(404, "Causal loop not found")
    db.delete(cl)
    db.commit()
    return {"ok": True}


# ── Breakpoint CRUD ──

@router.get("/breakpoints", response_model=list[BreakpointResponse])
def list_breakpoints(project_id: str, db: Session = Depends(get_db)):
    return db.query(Breakpoint).filter_by(project_id=project_id).order_by(Breakpoint.code).all()


@router.post("/breakpoints", response_model=BreakpointResponse)
def create_breakpoint(project_id: str, req: BreakpointCreate, db: Session = Depends(get_db)):
    bp = Breakpoint(project_id=project_id, **req.model_dump())
    db.add(bp)
    db.commit()
    db.refresh(bp)
    return bp


@router.put("/breakpoints/{bp_id}", response_model=BreakpointResponse)
def update_breakpoint(project_id: str, bp_id: str, req: BreakpointUpdate, db: Session = Depends(get_db)):
    bp = db.query(Breakpoint).filter_by(id=bp_id, project_id=project_id).first()
    if not bp:
        raise HTTPException(404, "Breakpoint not found")
    for k, v in req.model_dump(exclude_none=True).items():
        setattr(bp, k, v)
    db.commit()
    db.refresh(bp)
    return bp


@router.delete("/breakpoints/{bp_id}")
def delete_breakpoint(project_id: str, bp_id: str, db: Session = Depends(get_db)):
    bp = db.query(Breakpoint).filter_by(id=bp_id, project_id=project_id).first()
    if not bp:
        raise HTTPException(404, "Breakpoint not found")
    db.delete(bp)
    db.commit()
    return {"ok": True}
