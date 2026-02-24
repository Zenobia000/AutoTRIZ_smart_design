import json
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.project import Project
from src.models.definition import TaskDefinition
from src.models.contradiction import Contradiction
from src.models.assumption import Assumption
from src.models.alternative import Alternative
from src.models.must import MustEvaluation
from src.models.want import WantCriteria, WantScore
from src.models.risk import Risk
from src.models.decision import DecisionRecord
from src.models.experiment import Experiment

router = APIRouter(prefix="/api/v1/projects/{project_id}/export", tags=["export"])


@router.get("/markdown", response_class=PlainTextResponse)
def export_markdown(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    assumptions = db.query(Assumption).filter_by(project_id=project_id).all()
    alternatives = db.query(Alternative).filter_by(project_id=project_id).all()
    must_evals = db.query(MustEvaluation).filter_by(project_id=project_id).all()
    criteria = db.query(WantCriteria).filter_by(project_id=project_id).all()
    scores = db.query(WantScore).filter_by(project_id=project_id).all()
    risks = db.query(Risk).filter_by(project_id=project_id).all()
    decision = db.query(DecisionRecord).filter_by(project_id=project_id).first()
    experiments = db.query(Experiment).filter_by(project_id=project_id).all()

    lines = []
    name = project.name if project else "Unknown"
    lines.append(f"# {name} - RD Design Copilot 報告\n")

    # 1. Task Definition
    lines.append("## 1. 任務定義表\n")
    if defn:
        lines.append(f"**Mission**: {defn.mission}\n")
        lines.append("### Hard Constraints\n")
        lines.append("| 名稱 | 值 | 來源 |")
        lines.append("|------|-----|------|")
        for c in (defn.hard_constraints or []):
            lines.append(f"| {c.get('name','')} | {c.get('value','')} | {c.get('source','')} |")
        lines.append("\n### Critical Metrics\n")
        lines.append("| 名稱 | 目標 | 判斷方式 |")
        lines.append("|------|------|---------|")
        for m in (defn.critical_metrics or []):
            lines.append(f"| {m.get('name','')} | {m.get('target','')} | {m.get('method','')} |")
    lines.append("")

    # 2. Contradictions
    lines.append("## 2. 矛盾列表\n")
    lines.append("| 編號 | 改善參數 | 惡化參數 | 工程描述 |")
    lines.append("|------|---------|---------|---------|")
    for c in contradictions:
        lines.append(f"| {c.code} | {c.improve_param} | {c.worsen_param} | {c.engineering_desc} |")
    lines.append("")

    # 3. Assumptions
    lines.append("## 3. 假設台帳\n")
    lines.append("| 編號 | 類型 | 內容 | 風險 | 狀態 | Owner |")
    lines.append("|------|------|------|------|------|-------|")
    for a in assumptions:
        lines.append(f"| {a.code} | {a.assumption_type} | {a.content[:60]} | {a.risk_level} | {a.status} | {a.owner} |")
    lines.append("")

    # 4. Alternatives
    lines.append("## 4. 方案集合\n")
    for a in alternatives:
        lines.append(f"### {a.code}: {a.name}\n")
        lines.append(f"- **來源**: {a.source}")
        lines.append(f"- **狀態**: {a.status}")
        lines.append(f"- **機構**: {json.dumps(a.mechanism, ensure_ascii=False)}")
        lines.append("")

    # 5. MUST
    lines.append("## 5. MUST 篩選結果\n")
    lines.append("| 方案 | 結果 | 通過 |")
    lines.append("|------|------|------|")
    for ev in must_evals:
        alt = next((a for a in alternatives if a.id == ev.alternative_id), None)
        code = alt.code if alt else ev.alternative_id
        lines.append(f"| {code} | {json.dumps(ev.results, ensure_ascii=False)} | {'Pass' if ev.overall_pass else 'Fail'} |")
    lines.append("")

    # 6. WANT
    lines.append("## 6. WANT 評分結果\n")
    if criteria:
        header = "| 方案 |" + "|".join(f" {c.code}({c.weight}) " for c in criteria) + "| 總分 |"
        sep = "|------|" + "|".join("------" for _ in criteria) + "|------|"
        lines.append(header)
        lines.append(sep)
        for a in alternatives:
            if a.status in ("must_pass", "selected", "backup"):
                row_scores = []
                total = 0
                for c in criteria:
                    s = next((s for s in scores if s.alternative_id == a.id and s.criteria_id == c.id), None)
                    if s:
                        row_scores.append(f"{s.score}({s.weighted_score})")
                        total += s.weighted_score
                    else:
                        row_scores.append("-")
                lines.append(f"| {a.code} | " + " | ".join(row_scores) + f" | **{total}** |")
    lines.append("")

    # 7. Risks
    lines.append("## 7. 風險評估\n")
    lines.append("| 描述 | 類型 | P | S | Level | 緩解 |")
    lines.append("|------|------|---|---|-------|------|")
    for r in risks:
        lines.append(f"| {r.description} | {r.risk_type} | {r.probability} | {r.severity} | {r.level} | {r.mitigation} |")
    lines.append("")

    # 8. Decision Record
    lines.append("## 8. KT 決策記錄\n")
    if decision:
        lines.append(f"**決策聲明**: {decision.statement}\n")
        lines.append(f"**首選方案**: {decision.primary_choice} — {decision.primary_reason}\n")
        lines.append(f"**備選方案**: {decision.backup_choice} — {decision.backup_reason}\n")
        if decision.signed_by:
            lines.append(f"**簽核**: {decision.signed_by} @ {decision.signed_at}\n")
    lines.append("")

    # 9. Experiments
    lines.append("## 9. 最小實驗計畫\n")
    lines.append("| 目標 | 問題 | 方法 | 狀態 |")
    lines.append("|------|------|------|------|")
    for e in experiments:
        lines.append(f"| {e.goal} | {e.question} | {e.method} | {e.status} |")
    lines.append("")

    lines.append("---")
    lines.append(f"Generated by RD Design Copilot v0.5 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return "\n".join(lines)


@router.get("/json")
def export_json(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    contradictions = db.query(Contradiction).filter_by(project_id=project_id).all()
    assumptions = db.query(Assumption).filter_by(project_id=project_id).all()
    alternatives = db.query(Alternative).filter_by(project_id=project_id).all()
    risks = db.query(Risk).filter_by(project_id=project_id).all()
    decision = db.query(DecisionRecord).filter_by(project_id=project_id).first()
    experiments = db.query(Experiment).filter_by(project_id=project_id).all()

    from src.schemas.project import ProjectResponse
    from src.schemas.definition import TaskDefinitionResponse

    return {
        "project": ProjectResponse.model_validate(project).model_dump() if project else None,
        "definition": TaskDefinitionResponse.model_validate(defn).model_dump() if defn else None,
        "contradictions": [{"code": c.code, "improve_param": c.improve_param, "worsen_param": c.worsen_param, "engineering_desc": c.engineering_desc} for c in contradictions],
        "assumptions": [{"code": a.code, "content": a.content, "type": a.assumption_type, "risk_level": a.risk_level, "status": a.status, "owner": a.owner} for a in assumptions],
        "alternatives": [{"code": a.code, "name": a.name, "status": a.status, "mechanism": a.mechanism} for a in alternatives],
        "risks": [{"description": r.description, "level": r.level, "mitigation": r.mitigation} for r in risks],
        "decision": {"statement": decision.statement, "primary_choice": decision.primary_choice, "signed_by": decision.signed_by} if decision else None,
        "experiments": [{"goal": e.goal, "status": e.status} for e in experiments],
    }
