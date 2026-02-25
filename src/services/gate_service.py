from sqlalchemy.orm import Session

from src.models.definition import TaskDefinition
from src.models.alternative import Alternative
from src.models.want import WantScore
from src.models.risk import Risk
from src.models.decision import DecisionRecord
from src.models.assumption import Assumption
from src.models.contradiction import Contradiction
from src.models.causal_loop import CausalLoop, Breakpoint
from src.models.experiment import Experiment
from src.models.pre_cad_review import PreCadReview


def check_gate_1_1(db: Session, project_id: str) -> dict:
    """Gate 1.1: 三個最不能失敗指標已定義且有判斷方式"""
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    checks = []

    if not defn:
        checks.append({"item": "任務定義表已建立", "passed": False, "note": "尚未建立"})
        return {"checklist": checks, "overall_pass": False}

    checks.append({"item": "任務定義表已建立", "passed": True, "note": ""})
    checks.append({"item": "Mission 已填寫", "passed": bool(defn.mission), "note": ""})

    metrics = defn.critical_metrics or []
    checks.append({
        "item": "至少三個最不能失敗指標",
        "passed": len(metrics) >= 3,
        "note": f"目前 {len(metrics)} 個",
    })

    for m in metrics:
        checks.append({
            "item": f"指標「{m.get('name', '?')}」有判斷方式",
            "passed": bool(m.get("method")),
            "note": "",
        })

    return {
        "checklist": checks,
        "overall_pass": all(c["passed"] for c in checks),
    }


def check_gate_1_2(db: Session, project_id: str) -> dict:
    """Gate 1.2: ≥10 假設 + Top 3 高風險已標記 + ≥3 矛盾"""
    checks = []

    assumptions = db.query(Assumption).filter_by(project_id=project_id).all()
    checks.append({
        "item": "至少 10 條假設",
        "passed": len(assumptions) >= 10,
        "note": f"目前 {len(assumptions)} 條",
    })

    top = [a for a in assumptions if a.risk_level in ("High", "Medium-High")]
    checks.append({
        "item": "至少 3 條高風險假設已標記",
        "passed": len(top) >= 3,
        "note": f"目前 {len(top)} 條",
    })

    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    checks.append({
        "item": "至少 3 條矛盾",
        "passed": len(contradictions) >= 3,
        "note": f"目前 {len(contradictions)} 條",
    })

    return {"checklist": checks, "overall_pass": all(c["passed"] for c in checks)}


def check_gate_1_3(db: Session, project_id: str) -> dict:
    """Gate 1.3 (Phase Gate 1): ≥1 因果迴路 + ≥3 斷路點 + 所有矛盾已分類"""
    checks = []

    loops = db.query(CausalLoop).filter_by(project_id=project_id).all()
    checks.append({
        "item": "至少 1 條因果迴路",
        "passed": len(loops) >= 1,
        "note": f"目前 {len(loops)} 條",
    })

    breakpoints = db.query(Breakpoint).filter_by(project_id=project_id).all()
    checks.append({
        "item": "至少 3 個斷路點",
        "passed": len(breakpoints) >= 3,
        "note": f"目前 {len(breakpoints)} 個",
    })

    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    unclassified = [c for c in contradictions if not c.contradiction_types]
    checks.append({
        "item": "所有矛盾已分類 (TC/PC/SF)",
        "passed": len(unclassified) == 0 and len(contradictions) > 0,
        "note": f"{len(unclassified)} 條缺分類" if unclassified else "",
    })

    return {"checklist": checks, "overall_pass": all(c["passed"] for c in checks)}


def check_gate_2_1(db: Session, project_id: str) -> dict:
    """Gate 2.1: Top 3 高風險假設各有對應驗證設計 (Experiment)"""
    checks = []

    top_assumptions = (
        db.query(Assumption)
        .filter_by(project_id=project_id)
        .filter(Assumption.risk_level.in_(["High", "Medium-High"]))
        .all()
    )
    checks.append({
        "item": "至少 3 條高風險假設",
        "passed": len(top_assumptions) >= 3,
        "note": f"目前 {len(top_assumptions)} 條",
    })

    for a in top_assumptions[:3]:
        exp = db.query(Experiment).filter_by(project_id=project_id, assumption_id=a.id).first()
        checks.append({
            "item": f"{a.code} 有驗證設計 (實驗)",
            "passed": exp is not None,
            "note": "",
        })

    return {"checklist": checks, "overall_pass": all(c["passed"] for c in checks)}


def check_gate_2_2(db: Session, project_id: str) -> dict:
    """Gate 2.2: ≥3 條架構級路線通過 MUST"""
    passed_alts = (
        db.query(Alternative)
        .filter_by(project_id=project_id)
        .filter(Alternative.status.in_(["must_pass", "selected", "backup"]))
        .all()
    )
    checks = [
        {
            "item": "至少 3 條路線通過 MUST",
            "passed": len(passed_alts) >= 3,
            "note": f"目前 {len(passed_alts)} 條",
        }
    ]
    for alt in passed_alts:
        has_spec = bool(alt.mechanism and alt.assumptions and alt.risks)
        checks.append({
            "item": f"{alt.code} 有完整方案規格",
            "passed": has_spec,
            "note": "",
        })

    return {
        "checklist": checks,
        "overall_pass": all(c["passed"] for c in checks),
    }


def check_gate_2_3(db: Session, project_id: str) -> dict:
    """Gate 2.3 (Phase Gate 2): ≥3 路線已選 + robust_scores + Pre-CAD Review 通過"""
    checks = []

    selected = (
        db.query(Alternative)
        .filter_by(project_id=project_id)
        .filter(Alternative.status.in_(["selected", "backup", "must_pass"]))
        .all()
    )
    checks.append({
        "item": "至少 3 條路線已篩選",
        "passed": len(selected) >= 3,
        "note": f"目前 {len(selected)} 條",
    })

    for alt in selected[:3]:
        has_robust = bool(alt.robust_scores and any(v for v in (alt.robust_scores or {}).values()))
        checks.append({
            "item": f"{alt.code} 有穩健性評分",
            "passed": has_robust,
            "note": "",
        })

    passed_reviews = (
        db.query(PreCadReview)
        .filter_by(project_id=project_id, overall_pass=True)
        .all()
    )
    checks.append({
        "item": "至少 1 條路線通過 Pre-CAD Review",
        "passed": len(passed_reviews) >= 1,
        "note": f"目前 {len(passed_reviews)} 條通過",
    })

    return {"checklist": checks, "overall_pass": all(c["passed"] for c in checks)}


def check_gate_3_2(db: Session, project_id: str) -> dict:
    """Gate 3.2: KT 完整 + WANT 有證據 + H 風險有緩解"""
    checks = []

    dr = db.query(DecisionRecord).filter_by(project_id=project_id).first()
    checks.append({
        "item": "KT 決策記錄已建立",
        "passed": dr is not None,
        "note": "",
    })
    if dr:
        checks.append({
            "item": "決策記錄已簽核",
            "passed": dr.signed_by is not None,
            "note": "",
        })

    scores = db.query(WantScore).filter_by(project_id=project_id).all()
    missing = [s for s in scores if not s.evidence]
    checks.append({
        "item": "所有 WANT 評分有證據",
        "passed": len(missing) == 0,
        "note": f"{len(missing)} 個缺證據" if missing else "",
    })

    high_risks = (
        db.query(Risk)
        .filter_by(project_id=project_id)
        .filter(Risk.level.in_(["H", "H*"]))
        .all()
    )
    unmitigated = [r for r in high_risks if not r.mitigation]
    checks.append({
        "item": "所有 H/H* 風險有緩解措施",
        "passed": len(unmitigated) == 0,
        "note": f"{len(unmitigated)} 個未緩解" if unmitigated else "",
    })

    return {
        "checklist": checks,
        "overall_pass": all(c["passed"] for c in checks),
    }


def check_gate_3_3(db: Session, project_id: str) -> dict:
    """Gate 3.3 (Phase Gate 3): 決策已簽核 + H 風險已緩解 + 行動項已整理"""
    checks = []

    dr = db.query(DecisionRecord).filter_by(project_id=project_id).first()
    checks.append({
        "item": "KT 決策記錄已簽核",
        "passed": dr is not None and dr.signed_by is not None,
        "note": "",
    })

    high_risks = (
        db.query(Risk)
        .filter_by(project_id=project_id)
        .filter(Risk.level.in_(["H", "H*"]))
        .all()
    )
    unmitigated = [r for r in high_risks if not r.mitigation]
    checks.append({
        "item": "所有 H/H* 風險有緩解措施",
        "passed": len(unmitigated) == 0,
        "note": f"{len(unmitigated)} 個未緩解" if unmitigated else "",
    })

    has_actions = dr is not None and bool(dr.action_items)
    checks.append({
        "item": "知識資產已整理 (action items)",
        "passed": has_actions,
        "note": "",
    })

    return {"checklist": checks, "overall_pass": all(c["passed"] for c in checks)}
