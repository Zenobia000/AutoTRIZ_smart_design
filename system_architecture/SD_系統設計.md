# System Design (SD) - RD Design Copilot MVP

---

## 1. 資料庫設計 (ERD)

```
┌─────────────────────┐
│      projects       │
├─────────────────────┤
│ id          TEXT PK  │  (UUID)
│ name        TEXT     │
│ description TEXT     │
│ status      TEXT     │  (DRAFT/PHASE_I/PHASE_II/PHASE_III/COMPLETED)
│ created_at  DATETIME │
│ updated_at  DATETIME │
└──────────┬──────────┘
           │ 1:1
┌──────────▼──────────┐
│  task_definitions   │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ mission     TEXT     │
│ hard_constraints JSON│  (array of {name, value, source})
│ soft_objectives JSON │  (array of {name, direction})
│ non_goals   JSON     │  (array of string)
│ critical_metrics JSON│  (array of {name, target, method})
│ created_at  DATETIME │
│ updated_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│ socratic_questions   │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ category    TEXT     │  (clarify/assumption/evidence/perspective/consequence/reflection)
│ question    TEXT     │
│ answer      TEXT     │  (nullable, 用戶填)
│ created_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│   contradictions     │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ code        TEXT     │  (C1, C2, ...)
│ improve_param TEXT   │
│ worsen_param  TEXT   │
│ engineering_desc TEXT│
│ physical_contradiction TEXT │
│ source      TEXT     │
│ created_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│    assumptions       │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ code        TEXT     │  (A1, A2, ...)
│ content     TEXT     │
│ source      TEXT     │  (文獻/案例/工程常識/推測)
│ worst_consequence TEXT│
│ verification_method TEXT │
│ cost_cycle  TEXT     │
│ status      TEXT     │  (pending/verified/disproved)
│ is_critical BOOLEAN  │  (Top 3 致命假設)
│ created_at  DATETIME │
│ updated_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│   triz_solutions     │
├─────────────────────┤
│ id              TEXT PK │
│ project_id      TEXT FK │
│ contradiction_id TEXT FK│
│ principle_number INT    │
│ principle_name  TEXT    │
│ abstract_strategy TEXT  │
│ engineering_mappings JSON│ (array of string)
│ cost_description TEXT   │
│ robust_estimate  JSON   │ ({margin, decoupling, recoverability})
│ experiment_desc  TEXT   │
│ created_at      DATETIME│
└─────────────────────────┘

┌─────────────────────┐
│  scamper_variants    │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ subsystem   TEXT     │
│ action      TEXT     │  (S/C/A/M/P/E/R)
│ target      TEXT     │
│ mechanism   TEXT     │
│ failure_mode TEXT    │
│ supply_risk TEXT     │
│ assumptions TEXT     │
│ verification TEXT    │
│ created_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│    alternatives      │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ code        TEXT     │  (方案 A, 方案 B, ...)
│ name        TEXT     │
│ source      TEXT     │  (TRIZ#X + SCAMPER-Y)
│ mechanism   JSON     │  ({physical_principle, structure, key_dimensions})
│ assumptions JSON     │  (array of assumption_ids)
│ risks       JSON     │  ({failure_modes, process_risk, supply_risk})
│ robust_scores JSON   │  ({margin, decoupling, recoverability, complexity, sensitivity})
│ status      TEXT     │  (candidate/must_pass/must_fail/selected/backup/eliminated)
│ created_at  DATETIME │
│ updated_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│  must_evaluations    │
├─────────────────────┤
│ id             TEXT PK │
│ project_id     TEXT FK │
│ alternative_id TEXT FK │
│ results        JSON    │ ({M1: true/false, M2: true/false, ...})
│ overall_pass   BOOLEAN │
│ notes          TEXT    │
│ evaluated_at   DATETIME│
└─────────────────────────┘

┌─────────────────────┐
│   want_criteria      │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ code        TEXT     │  (W1, W2, ...)
│ name        TEXT     │
│ weight      INT      │  (1-10)
│ score_10    TEXT     │  (10分條件描述)
│ score_6     TEXT     │  (6分條件描述)
│ score_2     TEXT     │  (2分條件描述)
│ evidence_type TEXT   │  (計算書/BOM/AVL/...)
└─────────────────────┘

┌─────────────────────┐
│    want_scores       │
├─────────────────────┤
│ id             TEXT PK │
│ project_id     TEXT FK │
│ alternative_id TEXT FK │
│ criteria_id    TEXT FK │
│ score          INT     │ (1-10)
│ evidence       TEXT    │
│ weighted_score INT     │ (自動計算: weight × score)
└─────────────────────────┘

┌─────────────────────┐
│       risks          │
├─────────────────────┤
│ id             TEXT PK │
│ project_id     TEXT FK │
│ alternative_id TEXT FK │ (nullable, 可能是通用風險)
│ description    TEXT    │
│ risk_type      TEXT    │ (technical/process/supply/integration/verification/production)
│ probability    TEXT    │ (L/M/H)
│ severity       TEXT    │ (L/M/H)
│ level          TEXT    │ (L/M/H/H*)
│ owner          TEXT    │
│ mitigation     TEXT    │
│ residual_risk  TEXT    │
│ monitor        TEXT    │
│ created_at     DATETIME│
└─────────────────────────┘

┌─────────────────────┐
│    experiments       │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ assumption_id TEXT FK│
│ goal        TEXT     │
│ question    TEXT     │ (只回答一個問題)
│ method      TEXT     │
│ success_criteria TEXT│
│ failure_action TEXT  │
│ cost_cycle  TEXT     │
│ status      TEXT     │ (planned/in_progress/completed)
│ result      TEXT     │
│ created_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│  decision_records    │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ statement   TEXT     │
│ must_results JSON    │ ({passed: [], eliminated: [{alt, reason}]})
│ want_results JSON    │ ({alt_id: total_score, ...})
│ ac_results   JSON    │ (array of {alt, risk, level, mitigation})
│ primary_choice TEXT  │ (alternative_id)
│ primary_reason TEXT  │
│ backup_choice  TEXT  │ (alternative_id)
│ backup_reason  TEXT  │
│ action_items JSON    │ (array of {task, owner, due})
│ signed_by   TEXT     │
│ signed_at   DATETIME │
│ created_at  DATETIME │
│ updated_at  DATETIME │
└─────────────────────┘

┌─────────────────────┐
│    gate_checks       │
├─────────────────────┤
│ id          TEXT PK  │
│ project_id  TEXT FK  │
│ gate_number INT      │ (1, 2, 3)
│ checklist   JSON     │ (array of {item, passed, note})
│ overall_pass BOOLEAN │
│ checked_at  DATETIME │
└─────────────────────┘
```

---

## 2. LLM Prompt 設計

### 2.1 Prompt 模板結構

每個 prompt 模板遵循統一格式：

```
System: 角色定義 + 約束 + 輸出格式
User: 專案上下文 + 具體指令
Output: JSON schema (用 structured output 強制)
```

### 2.2 關鍵 Prompt 範例

#### task_definition.md

```markdown
# System
你是 RD Design Copilot，專注於早期概念設計階段。
你的任務是將模糊需求轉換為結構化的任務定義表。

## 規則
- Mission 必須包含：使用情境、達成行為、三個最不能失敗指標
- Hard Constraints 必須有數值或明確判斷標準
- 每個指標必須有判斷方式（數值或區間）
- Non-Goals 至少列出 2 項
- 使用繁體中文

## 輸出格式
回傳 JSON，schema 如下：
{
  "mission": "string",
  "hard_constraints": [{"name": "string", "value": "string", "source": "string"}],
  "soft_objectives": [{"name": "string", "direction": "string"}],
  "non_goals": ["string"],
  "critical_metrics": [{"name": "string", "target": "string", "method": "string"}]
}

# User
需求描述：{requirement_text}
補充約束：{constraints}
```

#### triz_solution.md

```markdown
# System
你是 TRIZ 專家，根據矛盾句生成工程解法方向。

## 規則
- 每條矛盾生成 2-3 個解法方向
- 每個解法必須附帶：採用原理、抽象策略、工程對映（具體機構/材料/佈局）、代價
- 不要用形容詞，只用工程語言
- robust 評分預估只給方向提示，不做最終評分

## 輸出格式
JSON array，每個元素：
{
  "principle_number": int,
  "principle_name": "string",
  "abstract_strategy": "string",
  "engineering_mappings": ["string"],
  "cost_description": "string",
  "robust_estimate": {"margin": "string", "decoupling": "string", "recoverability": "string"},
  "experiment_desc": "string"
}

# User
矛盾句：{contradiction}
專案約束：{constraints}
```

### 2.3 Prompt 管理策略

- Prompt 模板存在 `src/prompts/` 目錄下，純 Markdown 文件
- 用 Python f-string 或 Jinja2 做變數替換
- 版本控制 prompt 修改歷史（Git 即可）
- LLM 回應用 Pydantic model 解析驗證

---

## 3. 核心 Service 設計

### 3.1 LLMService

```python
class LLMService:
    """統一 LLM 呼叫入口"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def generate(
        self,
        prompt_template: str,      # prompt 模板路徑
        variables: dict,           # 模板變數
        response_schema: Type[BaseModel],  # 期望的回應 Pydantic model
        max_retries: int = 3
    ) -> BaseModel:
        """載入模板 → 填變數 → 呼叫 LLM → 解析回應 → 驗證 schema"""
        ...
```

### 3.2 GateService

```python
class GateService:
    """Gate 檢查邏輯"""

    def check_gate_1(self, project_id: str) -> GateResult:
        """Gate 1: 三個最不能失敗指標已定義且有判斷方式"""
        definition = self.get_definition(project_id)
        checks = []
        checks.append({
            "item": "三個最不能失敗指標已定義",
            "passed": len(definition.critical_metrics) >= 3
        })
        for metric in definition.critical_metrics:
            checks.append({
                "item": f"指標 '{metric.name}' 有判斷方式",
                "passed": bool(metric.method)
            })
        return GateResult(checklist=checks, overall_pass=all(c["passed"] for c in checks))

    def check_gate_2(self, project_id: str) -> GateResult:
        """Gate 2: ≥3 條架構級路線通過 MUST"""
        alternatives = self.get_alternatives(project_id, status="must_pass")
        checks = [
            {"item": "至少 3 條路線通過 MUST", "passed": len(alternatives) >= 3}
        ]
        for alt in alternatives:
            checks.append({
                "item": f"{alt.code} 有完整方案規格",
                "passed": bool(alt.mechanism and alt.assumptions and alt.risks)
            })
        return GateResult(checklist=checks, overall_pass=all(c["passed"] for c in checks))

    def check_gate_3(self, project_id: str) -> GateResult:
        """Gate 3: KT 完整 + WANT 有證據 + H 風險有緩解"""
        ...
```

### 3.3 DecisionService

```python
class DecisionService:
    """KT 決策計算"""

    def calculate_want_total(self, project_id: str, alternative_id: str) -> int:
        """計算加權總分 = sum(weight × score)"""
        scores = self.get_want_scores(project_id, alternative_id)
        return sum(s.weighted_score for s in scores)

    def evaluate_risk_level(self, probability: str, severity: str) -> str:
        """風險矩陣: P×S → Level"""
        matrix = {
            ("H", "H"): "H*", ("H", "M"): "H", ("H", "L"): "M",
            ("M", "H"): "H",  ("M", "M"): "M", ("M", "L"): "L",
            ("L", "H"): "M",  ("L", "M"): "L", ("L", "L"): "L",
        }
        return matrix.get((probability, severity), "M")

    def check_evidence_completeness(self, project_id: str) -> List[dict]:
        """檢查所有 WANT 評分是否都有證據"""
        scores = self.get_all_want_scores(project_id)
        return [
            {"alternative": s.alternative_id, "criteria": s.criteria_id, "has_evidence": bool(s.evidence)}
            for s in scores
        ]
```

---

## 4. 匯出設計

### 4.1 Markdown 匯出格式

```markdown
# [專案名稱] - RD Design Copilot 報告

## 1. 任務定義表
{task_definition 內容}

## 2. 矛盾列表
{contradictions 表格}

## 3. 假設台帳
{assumptions 表格}

## 4. 方案集合
{alternatives 詳細內容}

## 5. MUST 篩選結果
{must_evaluations 表格}

## 6. WANT 評分結果
{want_scores 表格 + 總分}

## 7. 風險評估
{risks 表格}

## 8. KT 決策記錄
{decision_record 完整 YAML}

## 9. 最小實驗計畫
{experiments 表格}

---
Generated by RD Design Copilot v0.5 | {date}
```

---

## 5. 錯誤處理

| 場景 | 處理方式 |
|------|---------|
| LLM API 超時 | 重試 3 次，指數退避 (2s, 4s, 8s) |
| LLM 回應格式錯誤 | 重試 1 次，附加 "請嚴格遵循 JSON schema" |
| LLM 回應驗證失敗 | 返回錯誤訊息，保留原始回應供 debug |
| DB 寫入失敗 | 回滾 transaction，返回 500 |
| Gate 檢查未通過 | 返回未通過項目清單，不阻止操作（可覆寫） |

---

## 6. 安全考量 (MVP 最小集)

| 項目 | MVP 做法 |
|------|---------|
| API Key | 環境變數 (.env)，不入版控 |
| SQL Injection | SQLAlchemy ORM 參數化查詢 |
| XSS | Streamlit 內建 escape |
| CORS | FastAPI CORS middleware，允許 localhost |
| Rate Limit | MVP 不做，v1.0 加 |
