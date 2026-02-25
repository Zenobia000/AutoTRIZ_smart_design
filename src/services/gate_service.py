from sqlalchemy.orm import Session

from src.models.definition import TaskDefinition
from src.models.alternative import Alternative
from src.models.must import MustEvaluation
from src.models.want import WantScore
from src.models.risk import Risk
from src.models.decision import DecisionRecord


def check_gate_1(db: Session, project_id: str) -> dict:
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


def check_gate_2(db: Session, project_id: str) -> dict:
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


def check_gate_3(db: Session, project_id: str) -> dict:
    """Gate 3.2: KT 完整 + WANT 有證據 + H 風險有緩解"""
    checks = []

    # KT decision record exists
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

    # WANT scores have evidence
    scores = db.query(WantScore).filter_by(project_id=project_id).all()
    missing = [s for s in scores if not s.evidence]
    checks.append({
        "item": "所有 WANT 評分有證據",
        "passed": len(missing) == 0,
        "note": f"{len(missing)} 個缺證據" if missing else "",
    })

    # H/H* risks have mitigation
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
