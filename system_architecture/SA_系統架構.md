# System Architecture (SA) - RD Design Copilot MVP

---

## 1. 架構原則

> **Simple is better than complex. Flat is better than nested.**
>
> MVP 架構只有三層：UI → API → Data。沒有微服務、沒有訊息佇列、沒有快取層。

---

## 2. 系統架構總覽

```
┌─────────────────────────────────────────────────────────────┐
│                        用戶 (瀏覽器)                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│                     Streamlit UI (Port 8501)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Phase 1  │ │ Phase 2  │ │ Phase 3  │ │ 匯出     │        │
│  │ 定義頁面 │ │ 發散頁面 │ │ 收斂頁面 │ │ 報告頁面 │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (REST API)
┌──────────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                   │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                    API Router 層                         │   │
│  │  /api/v1/projects      專案 CRUD                        │   │
│  │  /api/v1/phases        Phase 狀態管理                   │   │
│  │  /api/v1/definitions   任務定義表                        │   │
│  │  /api/v1/questions     索克拉底問答                      │   │
│  │  /api/v1/contradictions 矛盾識別                        │   │
│  │  /api/v1/assumptions   假設台帳                          │   │
│  │  /api/v1/triz          TRIZ 解法                        │   │
│  │  /api/v1/scamper       SCAMPER 變形                     │   │
│  │  /api/v1/alternatives  方案集合                          │   │
│  │  /api/v1/must          MUST 篩選                        │   │
│  │  /api/v1/want          WANT 評分                        │   │
│  │  /api/v1/risks         風險登錄表                        │   │
│  │  /api/v1/decisions     KT 決策記錄                      │   │
│  │  /api/v1/experiments   最小實驗                          │   │
│  │  /api/v1/gates         Gate 檢查                        │   │
│  │  /api/v1/export        匯出                             │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │  Service 層      │  │  LLM Service    │                     │
│  │  (業務邏輯)      │  │  (AI 呼叫)      │                     │
│  │                  │  │                  │                     │
│  │  - ProjectSvc    │  │  - generate()    │                     │
│  │  - PhaseSvc      │  │  - prompt 模板   │                     │
│  │  - DefinitionSvc │  │  - 回應解析      │                     │
│  │  - AssumptionSvc │  │                  │                     │
│  │  - AlternativeSvc│  │  Claude API      │                     │
│  │  - DecisionSvc   │  │  ↕               │                     │
│  │  - GateSvc       │  │  Anthropic SDK   │                     │
│  │  - ExportSvc     │  │                  │                     │
│  └────────┬─────────┘  └─────────────────┘                     │
│           │                                                     │
│  ┌────────▼─────────────────────────────────────────────────┐  │
│  │                   Data Access 層                           │  │
│  │  SQLAlchemy ORM + SQLite                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     SQLite (data.db)                           │
│  + 本地檔案系統 (exports/, evidence/)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 核心模組拆解

### 3.1 流程引擎（狀態機）

```
Project 狀態:
  DRAFT → PHASE_1 → PHASE_2 → PHASE_3 → COMPLETED

Phase 狀態:
  NOT_STARTED → IN_PROGRESS → GATE_PENDING → GATE_PASSED → COMPLETED

Gate 邏輯:
  Phase Gate 1 (= Gate 1.3): 三個最不能失敗指標已定義 AND 每個有判斷方式
  Phase Gate 2 (= Gate 2.3): ≥3 條架構級路線通過 MUST
  Phase Gate 3 (= Gate 3.3): KT 記錄完整 AND 每個 WANT 有證據 AND 所有 H 風險有緩解
```

### 3.2 LLM Service（核心 AI 引擎）

```
設計原則:
  - 一個 Service class，統一管理所有 LLM 呼叫
  - 每個功能對應一個 prompt 模板（存在 prompts/ 目錄）
  - 輸出用 structured output (JSON mode) 強制格式
  - 錯誤重試 3 次，指數退避

LLM 呼叫點:
  1. generate_task_definition(requirement_text) → TaskDefinition
  2. generate_socratic_questions(task_definition) → List[Question]
  3. identify_contradictions(conversation_history) → List[Contradiction]
  4. generate_triz_solutions(contradiction) → List[TrizSolution]
  5. generate_scamper_variants(subsystem, constraints) → List[ScamperVariant]
  6. generate_alternatives(triz_solutions, scamper_variants) → List[Alternative]
  7. generate_decision_record(must_results, want_results, ac_results) → DecisionRecord
```

### 3.3 資料模型

```
Project
  ├── TaskDefinition (1:1)
  │     ├── mission, hard_constraints, soft_objectives, non_goals
  │     └── critical_metrics (三個最不能失敗指標)
  │
  ├── SocraticQuestion (1:N)
  │     └── category, question, answer, source_assumptions
  │
  ├── Contradiction (1:N)
  │     └── improve_param, worsen_param, engineering_desc, physical_contradiction
  │
  ├── Assumption (1:N)
  │     └── content, source, worst_consequence, verification_method, cost_cycle, status
  │
  ├── TrizSolution (1:N per Contradiction)
  │     └── principle, abstract_strategy, engineering_mappings, cost, experiment
  │
  ├── ScamperVariant (1:N)
  │     └── action, target, mechanism, failure_mode, supply_risk, assumptions, verification
  │
  ├── Alternative (1:N)
  │     ├── name, source, mechanism, assumptions, risks, robust_scores
  │     ├── MustEvaluation (1:1)
  │     ├── WantScore (1:N per WANT dimension)
  │     └── AdverseConsequence (1:N)
  │
  ├── WantCriteria (1:N) — 團隊定義的 WANT 條件 + 權重
  │
  ├── Risk (1:N)
  │     └── description, probability, severity, level, owner, mitigation, monitor
  │
  ├── Experiment (1:N)
  │     └── hypothesis, goal, question, method, success_criteria, failure_action, cost
  │
  ├── DecisionRecord (1:1)
  │     └── statement, must_results, want_results, ac_results, decision, actions, signoff
  │
  └── GateCheck (1:N)
        └── gate_number, checklist_items, status, checked_at
```

---

## 4. 技術選型

| 層級 | 選擇 | 版本 | 理由 |
|------|------|------|------|
| **語言** | Python | 3.11+ | AI 生態最成熟 |
| **Web 框架** | FastAPI | 0.100+ | 自動 OpenAPI doc、async、型別提示 |
| **ORM** | SQLAlchemy | 2.0+ | 成熟穩定 |
| **資料庫** | SQLite | 3.x | 零配置，MVP 足夠 |
| **LLM SDK** | anthropic | latest | Claude API 官方 SDK |
| **LLM Model** | claude-sonnet-4-6 | — | 品質/成本/速度平衡 |
| **前端** | Streamlit | 1.30+ | 最快出 MVP UI |
| **驗證** | Pydantic | 2.0+ | FastAPI 內建 |
| **匯出** | python-docx + markdown | — | Word + Markdown 匯出 |
| **測試** | pytest | — | 標準 |

---

## 5. 目錄結構

```
rd_design_copilot/
├── system_architecture/          # 本文件所在
├── docs/                         # 需求文件
├── src/
│   ├── main.py                   # FastAPI 入口
│   ├── config.py                 # 設定 (API key, DB path, etc.)
│   ├── database.py               # SQLAlchemy engine + session
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── definition.py
│   │   ├── assumption.py
│   │   ├── contradiction.py
│   │   ├── alternative.py
│   │   ├── decision.py
│   │   └── risk.py
│   │
│   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── definition.py
│   │   ├── assumption.py
│   │   └── ...
│   │
│   ├── routers/                  # FastAPI routers
│   │   ├── __init__.py
│   │   ├── projects.py
│   │   ├── definitions.py
│   │   ├── assumptions.py
│   │   ├── alternatives.py
│   │   ├── decisions.py
│   │   ├── gates.py
│   │   └── export.py
│   │
│   ├── services/                 # 業務邏輯
│   │   ├── __init__.py
│   │   ├── llm_service.py        # LLM 呼叫統一入口
│   │   ├── phase_service.py      # 流程狀態機
│   │   ├── definition_service.py
│   │   ├── assumption_service.py
│   │   ├── triz_service.py
│   │   ├── scamper_service.py
│   │   ├── decision_service.py
│   │   ├── gate_service.py
│   │   └── export_service.py
│   │
│   └── prompts/                  # LLM prompt 模板 (Jinja2 或純文字)
│       ├── task_definition.md
│       ├── socratic_questions.md
│       ├── contradiction_identify.md
│       ├── triz_solution.md
│       ├── scamper_variant.md
│       ├── alternative_generate.md
│       ├── decision_record.md
│       └── black_hat_review.md
│
├── ui/
│   └── app.py                    # Streamlit 主程式
│
├── data/                         # SQLite DB + 匯出檔案
│   ├── data.db
│   └── exports/
│
├── tests/
│   ├── test_services/
│   └── test_routers/
│
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## 6. API 設計摘要

### 6.1 核心 API 端點

| Method | Path | 說明 | LLM |
|--------|------|------|-----|
| POST | /api/v1/projects | 建立新專案 | — |
| GET | /api/v1/projects/{id} | 取得專案全貌 | — |
| POST | /api/v1/projects/{id}/definitions/generate | AI 生成任務定義表 | **V** |
| PUT | /api/v1/projects/{id}/definitions | 用戶修改任務定義表 | — |
| POST | /api/v1/projects/{id}/questions/generate | AI 生成索克拉底問題 | **V** |
| POST | /api/v1/projects/{id}/questions/{qid}/answer | 用戶回答問題 | — |
| POST | /api/v1/projects/{id}/contradictions/identify | AI 識別矛盾 | **V** |
| CRUD | /api/v1/projects/{id}/assumptions | 假設台帳 CRUD | — |
| POST | /api/v1/projects/{id}/triz/generate | AI 生成 TRIZ 解法 | **V** |
| POST | /api/v1/projects/{id}/scamper/generate | AI 生成 SCAMPER 變形 | **V** |
| CRUD | /api/v1/projects/{id}/alternatives | 方案集合 CRUD | — |
| POST | /api/v1/projects/{id}/alternatives/generate | AI 生成候選方案 | **V** |
| POST | /api/v1/projects/{id}/must/evaluate | MUST 篩選 | — |
| CRUD | /api/v1/projects/{id}/want-criteria | WANT 條件 CRUD | — |
| POST | /api/v1/projects/{id}/want/score | WANT 評分 + 計算 | — |
| CRUD | /api/v1/projects/{id}/risks | 風險登錄表 CRUD | — |
| POST | /api/v1/projects/{id}/decisions/generate | AI 生成決策記錄草稿 | **V** |
| PUT | /api/v1/projects/{id}/decisions/signoff | 用戶簽核 | — |
| POST | /api/v1/projects/{id}/gates/{n}/check | Gate 檢查 | — |
| GET | /api/v1/projects/{id}/export/markdown | 匯出 Markdown | — |

---

## 7. 部署架構 (MVP)

```
方式 A: 本地開發 (最簡單)
  terminal 1: uvicorn src.main:app --port 8000
  terminal 2: streamlit run ui/app.py --server.port 8501

方式 B: Docker Compose
  docker-compose up
    ├── backend  (FastAPI, port 8000)
    └── frontend (Streamlit, port 8501)
```

---

## 8. 升級路徑 (MVP → v1.0)

| MVP | v1.0 升級 |
|-----|----------|
| SQLite | → PostgreSQL |
| 無認證 | → SSO/LDAP |
| Streamlit | → React SPA |
| 本地檔案 | → S3/MinIO |
| 無 RAG | → 向量 DB + 知識庫 |
| 單用戶 | → 多租戶 |
| 無 WebSocket | → 即時協作 |
