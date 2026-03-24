# Statement of Work (SOW)
# RD Design Copilot v1.0 開發說明書

> **版本**: v1.0 | **日期**: 2026-03-13 | **依據**: docs/e2e 全套設計文件

---

## 1. 專案概述

### 1.1 專案名稱
RD Design Copilot v1.0 — AI 驅動的早期概念設計決策平台

### 1.2 一句話定義
> 將 SCAMPER/TRIZ 發散、KT Decision Analysis 收斂、矛盾收斂圖完全收斂、8-Gate 證據驅動，整合為一套結構化設計流程，使 Pre-CAD 階段的信心可量化、決策可追溯、知識可沉澱。

### 1.3 核心問題 (量化)

| 指標 | 現狀 | v1.0 目標 |
|------|------|----------|
| 架構級返工次數 | 3-5 次/專案 | ≤2 次 |
| 設計審查效率 | 3-4 小時/會議 | ≤2 小時 |
| 假設驗證覆蓋率 | <30% | ≥80% |
| 方案探索路線數 | 1-2 條 | ≥3 條 |
| 決策可追溯性 | 低 | 100% |
| 工具採用率 | N/A | ≥70% |

### 1.4 目標用戶

| 角色 | 主要用途 | 核心痛點 |
|------|---------|---------|
| **RD 工程師** | 日常概念設計 | 受限於過往經驗，缺跨域知識 |
| **RD 主管** | 設計審查與決策 | 決策依據不足，風險不可見 |
| **PM** | 需求對齊 | 溝通落差，反覆對齊會議 |
| QA 工程師 | 風險評估 / FMEA | 需要早期風險可見性 |
| 製造工程師 | DFM 評估 | 需要早期可製造性回饋 |

---

## 2. 系統架構總覽

### 2.1 技術堆疊

| 層級 | 技術 | 說明 |
|------|------|------|
| 後端框架 | FastAPI (Python 3.11+) | 非同步 REST API |
| ORM | SQLAlchemy 2.0+ | 資料模型映射 |
| 資料庫 | SQLite → PostgreSQL (v1.1) | MVP 用 SQLite，上線遷移 PG |
| LLM | Claude API (claude-sonnet-4-6) | 5 類 Agent 呼叫 |
| 前端 | React + TypeScript | 6+1 頁架構 (Apple 設計哲學) |
| 驗證 | Pydantic 2.0+ | 輸入/輸出 Schema |
| 測試 | pytest + Playwright | 單元 + E2E |
| 容器 | Docker + docker-compose | 一鍵部署 |

### 2.2 四層 Agent 架構

| Agent | 職責 | LLM 呼叫 | 規則引擎 |
|-------|------|----------|---------|
| **Analyst Agent** | 問題定義、索克拉底提問、假設萃取 | ✓ | — |
| **TRIZ Solver Agent** | TRIZ 三路徑求解、Anti-Anchor | ✓ | ✓ (矩陣查表) |
| **Evaluator Agent** | MUST 篩選、Pre-CAD 評分、KT 計算 | ✓ (深度分析) | ✓ (規則判定) |
| **Knowledge Agent** | RAG 知識檢索、Web 搜尋、知識沉澱 | ✓ | — |

### 2.3 8-Gate 系統

| Gate | 位置 | 階段轉換 | 核心判定 |
|------|------|---------|---------|
| Gate 1.1 | Step 1.1→1.2 | DRAFT→PHASE_1 | Mission + ≥3 KPI 各有量測方法 |
| Gate 1.2 | Step 1.2→1.3 | Phase 1 內部 | ≥10 假設 + ≥3 高風險 + ≥3 矛盾 |
| Phase Gate 1 | Step 1.3→2.1 | PHASE_1→PHASE_2 | ≥1 CLD + ≥3 斷路點 + 矛盾正式化 |
| Gate 2.1 | Step 2.1→2.2 | Phase 2 內部 | ≥3 高風險假設各有實驗 |
| Gate 2.2 | Step 2.2→2.3 | Phase 2 內部 | ≥3 方案 + MUST 通過 |
| Phase Gate 2 | Step 2.3→3.1 | PHASE_2→PHASE_3 | ≥1 Pre-CAD overall_pass |
| Gate 3.2 | Step 3.2→3.3 | Phase 3 內部 | DecisionRecord 簽核 + WANT 有證據 |
| Phase Gate 3 | Step 3.3→Done | PHASE_3→COMPLETED | 所有核心工件 Released |

---

## 3. 工作分解結構 (WBS) — Top-Down

### 3.0 總覽圖

```
RD Design Copilot v1.0
├── WP-1: 基礎設施 (Infrastructure)
│   ├── WP-1.1: 後端骨架
│   ├── WP-1.2: 資料模型 + 遷移
│   ├── WP-1.3: LLM Service 統一入口
│   ├── WP-1.4: 認證 + 權限
│   └── WP-1.5: 前端骨架 + Design System
│
├── WP-2: Phase 1 — Define (定義問題空間)
│   ├── WP-2.1: 任務定義模組
│   ├── WP-2.2: 索克拉底七類提問引擎
│   ├── WP-2.3: 假設萃取 + 矛盾識別
│   ├── WP-2.4: 因果迴路圖 (CLD) + 斷路點
│   └── WP-2.5: Gate 1.1 / 1.2 / Phase Gate 1
│
├── WP-3: Phase 2 — Diverge (發散與探索)
│   ├── WP-3.1: 假設台帳 + Unknown Factors
│   ├── WP-3.2: Anti-Anchor Sprint
│   ├── WP-3.3: TRIZ 統一求解引擎 ★ (核心複雜度)
│   ├── WP-3.4: 子系統建議 + SCAMPER 變形
│   ├── WP-3.5: 矛盾回饋迴路 (SCAMPER→TRIZ)
│   ├── WP-3.6: 方案集合 + Interface Contract
│   ├── WP-3.7: MUST 快篩 (M1-M6)
│   ├── WP-3.8: Pre-CAD 5D 審查 + AI 分析
│   └── WP-3.9: Gate 2.1 / 2.2 / Phase Gate 2
│
├── WP-4: Phase 3 — Converge (收斂與決策)
│   ├── WP-4.1: 證據矩陣 (DR EM) + 聚合
│   ├── WP-4.2: 風險登錄 (FMEA-like)
│   ├── WP-4.3: 最小實驗設計 + 證據閉環
│   ├── WP-4.4: WANT 標準模板 + KT 評分
│   ├── WP-4.5: KT 決策記錄
│   ├── WP-4.6: Gate 3.2 / Phase Gate 3
│   └── WP-4.7: 知識沉澱 (自動回寫)
│
├── WP-5: 前端 UI (6+1 頁)
│   ├── WP-5.0: Dashboard (專案列表)
│   ├── WP-5.1: Brief 頁 (任務定義)
│   ├── WP-5.2: Explore 頁 (索克拉底 + CLD)
│   ├── WP-5.3: Track 頁 (假設台帳 Kanban)
│   ├── WP-5.4: Create 頁 (TRIZ + SCAMPER + MUST + Pre-CAD) ★
│   ├── WP-5.5: Review 頁 (證據矩陣 + 風險)
│   └── WP-5.6: Decide 頁 (WANT + KT 決策 + 匯出)
│
├── WP-6: 品質保證 (QA)
│   ├── WP-6.1: 單元測試
│   ├── WP-6.2: API 整合測試
│   ├── WP-6.3: E2E 場景測試 (真實案例)
│   └── WP-6.4: Prompt 品質調優
│
└── WP-7: 部署與文件
    ├── WP-7.1: Docker 部署
    ├── WP-7.2: API 文件 (OpenAPI)
    └── WP-7.3: 使用手冊
```

---

## 4. 工作包詳細定義

### WP-1: 基礎設施 (Infrastructure)

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 1.1 | 後端骨架 | FastAPI 專案結構、config、middleware、error handler | BE | 2d | — | ✓ 可與 1.5 並行 |
| 1.2 | 資料模型 + DB 遷移 | 27 張 ORM table、Alembic migration | BE | 3d | 1.1 | |
| 1.3 | LLM Service 統一入口 | `LLMService` + retry + token 管理 + prompt loader | BE | 2d | 1.1 | ✓ 可與 1.2 並行 |
| 1.4 | 認證 + 權限 | JWT / SSO stub、user model、permission middleware | BE | 2d | 1.1 | ✓ 可與 1.2/1.3 並行 |
| 1.5 | 前端骨架 + Design System | React scaffold、路由、共用元件庫 (按鈕/卡片/表格/表單) | FE | 5d | — | ✓ 可與 1.1 並行 |
| | **小計** | | | **14d** | | |

### WP-2: Phase 1 — Define

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 2.1 | 任務定義模組 | `POST/GET /definitions` API + Task Definition prompt + Schema | BE | 2d | 1.2 | ✓ 可與 2.2 並行 |
| 2.2 | 索克拉底七類提問引擎 | `POST/GET /questions` API + 7-class prompt + answer 收集 | BE | 3d | 1.2, 1.3 | ✓ 可與 2.1 並行 |
| 2.3 | 假設萃取 + 矛盾識別 | `POST /assumptions/extract` + `POST /contradictions` + identify prompt | BE | 3d | 2.2 | |
| 2.4 | 因果迴路圖 + 斷路點 | `POST/GET /causal-loops` + breakpoint CRUD + TRIZ 正式化 | BE | 4d | 2.3 | |
| 2.5 | Gate 1.1 / 1.2 / PG1 | Gate checker (3 個) + Phase 轉換邏輯 | BE | 2d | 2.4 | |
| | **小計** | | | **14d** | | |

### WP-3: Phase 2 — Diverge ★ (最高複雜度)

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 3.1 | 假設台帳 + Unknown Factors | Assumption CRUD + PDCA 狀態機 + disprove 影響分析 + U 因子 CRUD | BE | 4d | 2.5 | ✓ 可與 3.2 並行 |
| 3.2 | Anti-Anchor Sprint | `POST /alternatives/anti-anchor` + 3 非典型架構生成 prompt | BE | 3d | 2.5 | ✓ 可與 3.1 並行 |
| 3.3 | TRIZ 統一求解引擎 | `POST /triz/solve` → 分類(TC/PC/SF) + 參數映射 + 矩陣查表 + 三路徑實例化 | BE | 8d | 1.3, 2.4 | |
| 3.4 | 子系統建議 + SCAMPER | `GET /scamper/subsystem-suggestions` + `POST /scamper/perform` (7 動作 × N 子系統) | BE | 4d | 3.3 | |
| 3.5 | 矛盾回饋迴路 | `POST /scamper/feedback-contradictions` → 去重 → 自動建 Contradiction → 回饋 TRIZ | BE | 3d | 3.4 | |
| 3.6 | 方案集合 + Interface Contract | Alternative CRUD + mechanism/assumptions/risks/robust_scores + 6 維 Interface Contract | BE | 3d | 3.4, 3.5 | |
| 3.7 | MUST 快篩 (M1-M6) | `POST /must/evaluate` + 6 條規則引擎 + Go/No-Go 結果 | BE | 3d | 3.6 | |
| 3.8 | Pre-CAD 5D 審查 | `POST /pre-cad-reviews` + `POST /{id}/ai-analyze` + 5 維度 1-5 分 + radar chart data | BE | 4d | 3.7 | |
| 3.9 | Gate 2.1 / 2.2 / PG2 | Gate checker (3 個) + Phase 轉換邏輯 | BE | 2d | 3.8 | |
| | **小計** | | | **34d** | | |

### WP-4: Phase 3 — Converge

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 4.1 | 證據矩陣 (DR EM) | `GET /experiments/evidence-matrix` + Assumption × Evidence 聚合 + E0-E4 分級 | BE | 3d | 3.9 | ✓ 可與 4.2 並行 |
| 4.2 | 風險登錄 (FMEA-like) | Risk CRUD + P×S 計算 + L/M/H/H* 分級 + 歷史失效比對 | BE | 3d | 3.9 | ✓ 可與 4.1 並行 |
| 4.3 | 最小實驗設計 + 證據閉環 | Experiment CRUD + evidence_level 更新 + 閉環迴圈邏輯 | BE | 3d | 4.1 | |
| 4.4 | WANT 標準模板 + KT 評分 | `POST /want/criteria/seed` W1-W6 + weighted_score 計算 | BE | 3d | 4.1, 4.2 | |
| 4.5 | KT 決策記錄 | Decision CRUD + MUST/WANT/Risk 彙總 + 簽核邏輯 | BE | 3d | 4.4 | |
| 4.6 | Gate 3.2 / Phase Gate 3 | Gate checker (2 個) + Phase 轉換 | BE | 2d | 4.5 | |
| 4.7 | 知識沉澱 (自動回寫) | `POST /knowledge/writeback` + 6 類資產自動沉澱 | BE | 3d | 4.6 | |
| | **小計** | | | **20d** | | |

### WP-5: 前端 UI (6+1 頁)

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 5.0 | Dashboard | 專案列表、Phase 進度條、快速統計 | FE | 3d | 1.5 | ✓ 可與後端並行 |
| 5.1 | Brief 頁 | Mission 輸入、約束表、KPI 列表、AI 任務定義生成 | FE | 4d | 5.0, 2.1 | ✓ |
| 5.2 | Explore 頁 | 索克拉底 Q&A tabs、矛盾列表、互動式 CLD 圖、斷路點標記 | FE | 6d | 5.0, 2.4 | ✓ 可與 5.1 並行 |
| 5.3 | Track 頁 | 假設 Kanban (4 欄拖拉)、Unknown Factors 列表、PDCA 面板 | FE | 5d | 5.0, 3.1 | ✓ 可與 5.2 並行 |
| 5.4 | Create 頁 ★ | 7 個 Accordion (Anti-Anchor / TRIZ 3-path Tabs / 子系統 / SCAMPER / 方案卡片 / MUST 矩陣 / Pre-CAD 5D 雷達圖) | FE | 10d | 5.0, 3.8 | |
| 5.5 | Review 頁 | Tabs: 證據矩陣熱力圖 (E0→E4)、風險 P×S 矩陣、最小實驗列表 | FE | 6d | 5.0, 4.2 | ✓ 可與 5.4 並行 |
| 5.6 | Decide 頁 | WANT 排行榜、KT 決策記錄 (MUST→WANT→Risk 三層漏斗)、匯出 checklist | FE | 5d | 5.0, 4.5 | ✓ 可與 5.5 並行 |
| | **小計** | | | **39d** | | |

### WP-6: 品質保證

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 6.1 | 單元測試 | Service 層核心邏輯測試 (TRIZ Engine / Gate / MUST / WANT) | BE | 5d | WP-2~4 | 隨開發進行 |
| 6.2 | API 整合測試 | 端到端 API 流程測試 (Phase 1→2→3 完整鏈路) | BE | 3d | WP-2~4 | |
| 6.3 | E2E 場景測試 | 用 eBike 真實案例跑通全流程 | QA | 3d | WP-5 | |
| 6.4 | Prompt 品質調優 | 7 個 prompt 模板迭代 + 真實案例評測 | BE | 5d | WP-2~3 | ✓ 持續進行 |
| | **小計** | | | **16d** | | |

### WP-7: 部署與文件

| WBS | 工作包 | 產出物 | 人力 | 工時 | 前置 | 可並行 |
|-----|--------|--------|------|------|------|--------|
| 7.1 | Docker 部署 | Dockerfile + docker-compose + .env.example | DevOps | 2d | WP-1 | ✓ |
| 7.2 | API 文件 | OpenAPI spec (FastAPI 自動生成) + 補充說明 | BE | 1d | WP-2~4 | |
| 7.3 | 使用手冊 | 安裝/啟動/操作流程/FAQ | Tech Writer | 3d | WP-5 | |
| | **小計** | | | **6d** | | |

---

## 5. 人力配置與角色定義

### 5.1 角色需求

| 角色 | 代號 | 人數 | 核心技能 | 負責範圍 |
|------|------|------|---------|---------|
| **後端工程師 (Senior)** | BE-S | 1 | FastAPI, SQLAlchemy, LLM API, TRIZ 領域知識 | WP-1.1~1.3, WP-3.3 (TRIZ 引擎), WP-3.5 |
| **後端工程師 (Mid)** | BE-M | 1 | FastAPI, CRUD, 測試 | WP-2.x, WP-3.1/3.2/3.4/3.6~3.9, WP-4.x |
| **前端工程師 (Senior)** | FE-S | 1 | React, TypeScript, 資料視覺化 (D3/Recharts), 拖拉 UI | WP-1.5, WP-5.2 (CLD 互動), WP-5.4 (Create 頁) |
| **前端工程師 (Mid)** | FE-M | 1 | React, TypeScript, 表單, 表格 | WP-5.0/5.1/5.3/5.5/5.6 |
| **QA 工程師** | QA | 0.5 | pytest, Playwright, 測試設計 | WP-6.x |
| **PM** | PM | 0.5 | 需求對齊, Sprint 管理, 驗收 | 全程 |

### 5.2 最小團隊配置

- **最精簡 (2 人)**: 1 全端 Senior + 1 全端 Mid → 工期 ~14 週
- **建議 (4 人)**: 2 BE + 2 FE → 工期 ~8 週
- **加速 (5 人)**: 2 BE + 2 FE + 1 QA → 工期 ~7 週

---

## 6. 並行化排程策略

### 6.1 並行工作流圖

```
Week 1  ─┬─ [BE-S] WP-1.1 骨架 (2d) → WP-1.3 LLM Service (2d)
          │  [BE-M] WP-1.2 資料模型 (3d) → WP-1.4 認證 (2d)
          └─ [FE-S+FE-M] WP-1.5 前端骨架 + Design System (5d)

Week 2  ─┬─ [BE-S] WP-2.2 索克拉底引擎 (3d)  ──┐
          │  [BE-M] WP-2.1 任務定義 (2d) ────────┤
          └─ [FE-S] WP-5.0 Dashboard (3d)       │ ← 並行
             [FE-M] WP-5.1 Brief 頁 (4d)        │ ← 並行
                                                  ↓
Week 3  ─┬─ [BE-S] WP-2.3 假設萃取 + 矛盾 (3d) ───→ WP-2.4 CLD (4d 跨週)
          │  [BE-M] WP-2.5 Gate 1.x (2d) → WP-3.1 假設台帳 (4d 跨週)
          └─ [FE-S] WP-5.2 Explore 頁 (6d 跨週)  ← 並行
             [FE-M] WP-5.3 Track 頁 (5d 跨週)     ← 並行

Week 4  ─┬─ [BE-S] WP-3.3 TRIZ 引擎 ★ (8d 跨 Week 4-5)
          │  [BE-M] WP-3.2 Anti-Anchor (3d) → WP-3.4 SCAMPER (4d)
          └─ [FE-S] WP-5.2 完成 → WP-5.4 Create 頁 ★ (10d 跨 Week 4-6)
             [FE-M] WP-5.3 完成 → WP-5.5 Review 頁 (6d)

Week 5  ─┬─ [BE-S] WP-3.3 TRIZ 續 → WP-3.5 矛盾回饋 (3d)
          │  [BE-M] WP-3.6 方案集合 (3d) → WP-3.7 MUST (3d)
          └─ [FE-M] WP-5.5 完成 → WP-5.6 Decide 頁 (5d)

Week 6  ─┬─ [BE-S] WP-3.8 Pre-CAD (4d) → WP-3.9 Gate 2.x (2d)
          │  [BE-M] WP-4.1 證據矩陣 (3d) + WP-4.2 風險登錄 (3d) ← 並行
          └─ [FE-S] WP-5.4 Create 頁完成
             [FE-M] WP-5.6 Decide 頁完成

Week 7  ─┬─ [BE-S] WP-4.3 實驗閉環 (3d) → WP-4.7 知識沉澱 (3d)
          │  [BE-M] WP-4.4 WANT (3d) → WP-4.5 KT 決策 (3d)
          └─ [FE-S+FE-M] 前後端整合 + UI 調整

Week 8  ─┬─ [BE-S] WP-4.6 Gate 3.x (2d) + WP-6.4 Prompt 調優
          │  [BE-M] WP-6.1 單元測試 (5d) + WP-6.2 API 測試 (3d)
          └─ [FE-S+FE-M] WP-6.3 E2E 測試 + WP-7.x 部署文件
```

### 6.2 關鍵路徑 (Critical Path)

```
WP-1.1 → WP-1.2 → WP-2.2 → WP-2.3 → WP-2.4 → WP-3.3 (TRIZ) → WP-3.4 → WP-3.5 → WP-3.6 → WP-3.7 → WP-3.8 → WP-4.x → 交付

總長: ~55 工作天 (11 週) — 但 4 人並行可壓縮到 ~8 週
```

### 6.3 並行化節省分析

| 策略 | 節省天數 | 說明 |
|------|---------|------|
| BE-S / BE-M 並行 | -15d | Phase 1 的 2 個模組可並行；Phase 2 假設台帳 / Anti-Anchor 可並行；Phase 3 證據 / 風險可並行 |
| FE / BE 並行 | -20d | 前端開發在 API contract 確定後即可開始，不需等 API 完成 |
| 前端頁面間並行 | -10d | Dashboard / Brief / Explore / Track / Review / Decide 前 5 頁可 2 人分工 |
| Prompt 調優並行 | -5d | Prompt 調優與開發同步進行 |
| **總節省** | **~50d** | 從 143 人天壓縮到 40 工作天 (8 週) |

---

## 7. Prompt 模板清單

| 編號 | 模板 | 對應 Agent | 對應 Step |
|------|------|-----------|----------|
| PM-1 | `task_definition.md` | Analyst | Step 1.1 |
| PM-2 | `socratic_questions.md` | Analyst | Step 1.2 |
| PM-3 | `contradiction_identify.md` | Analyst | Step 1.2-1.3 |
| PM-4 | `triz_solution.md` | TRIZ Solver | Step 2.2.2 |
| PM-5 | `scamper_variant.md` | TRIZ Solver | Step 2.2.4 |
| PM-6 | `alternative_generate.md` | TRIZ Solver | Step 2.2.5 |
| PM-7 | `decision_record.md` | Evaluator | Step 3.2 |
| PM-8 | `black_hat_review.md` | Evaluator | Step 3.1 |
| PM-9 | `anti_anchor.md` | TRIZ Solver | Step 2.2.1 |
| PM-10 | `assumption_extract.md` | Analyst | Step 2.1 |

---

## 8. API 端點總覽

### 8.1 核心業務 API (35+ 端點)

| 模組 | 端點數 | 關鍵端點 |
|------|--------|---------|
| 專案管理 | 4 | `POST/GET /projects`, `GET /:id` |
| 任務定義 | 3 | `POST/GET /definitions` |
| 索克拉底問答 | 4 | `POST/GET /questions`, `POST /:qid/answer` |
| 矛盾管理 | 4 | `POST/GET /contradictions`, `POST /:cid/formalize` |
| 因果迴路 | 3 | `POST/GET /causal-loops`, breakpoint CRUD |
| 假設台帳 | 5 | `POST/GET/PUT /assumptions`, `POST /extract`, `POST /:aid/disprove` |
| Unknown Factors | 3 | `POST/GET /unknown-factors` |
| TRIZ 求解 | 3 | `POST /triz/solve`, `GET /triz/results/:rid` |
| SCAMPER | 3 | `POST /scamper/perform`, `GET /subsystem-suggestions`, `POST /feedback-contradictions` |
| 方案管理 | 4 | `POST/GET/PUT /alternatives`, `POST /anti-anchor` |
| MUST 篩選 | 2 | `POST /must/evaluate`, `GET /must/results` |
| Pre-CAD 審查 | 3 | `POST /pre-cad-reviews`, `POST /:rid/ai-analyze`, `GET /pre-cad-reviews` |
| 實驗 + 證據 | 4 | `POST/GET /experiments`, `GET /evidence-matrix`, `PUT /:eid/update-evidence` |
| 風險登錄 | 3 | `POST/GET /risks` |
| WANT 評分 | 3 | `POST/GET /want/criteria`, `POST /want/criteria/seed` |
| KT 決策 | 3 | `POST/GET /decisions` |
| Gate 檢查 | 1 | `GET /gates/:gate_id/check` (統一入口, 8 種 gate_id) |
| 匯出 | 1 | `POST /export` |
| 知識回寫 | 1 | `POST /knowledge/writeback` |

### 8.2 知識 + 輔助 API

| 模組 | 端點數 | 關鍵端點 |
|------|--------|---------|
| RAG 搜尋 | 2 | `GET /knowledge/rag/search`, `GET /knowledge/cross-domain` |
| Web 搜尋 | 1 | `GET /knowledge/web/search` |
| 認證 | 2 | `POST /auth/login`, `GET /user/profile` |
| 系統 | 1 | `GET /health` |

---

## 9. 資料模型摘要 (27 Entity)

### 9.1 核心實體

| Entity | 欄位數 | 狀態機 | 關鍵欄位 |
|--------|--------|--------|---------|
| Project | 6 | DRAFT→PHASE_1→PHASE_2→PHASE_3→COMPLETED | status, phase |
| Definition (Constraint) | 8 | Draft→Reviewed | mission, hard_constraints, kpis |
| Question | 7 | Draft→Reviewed | type_class (7 種), text, answer |
| Contradiction | 10 | Draft→Reviewed→Verified | improve_param, worsen_param, contradiction_type |
| CausalLoop | 5 | Draft→Reviewed | diagram_json |
| Breakpoint | 6 | Draft→Reviewed | location, triz_principle_hints |
| Assumption | 12 | Open→Experimenting→Validated/Refuted | worst_consequence, min_method, source_refs |
| UnknownFactor | 7 | — | levels, range_desc, assumption_refs |
| TrizSolution | 10 | — | classification (TC/PC/SF), param_mapping, matrix_lookup |
| Alternative | 14 | draft→must_pass→selected/backup/killed | mechanism, interface_contract, robust_scores |
| Scamper | 7 | — | action (S/C/A/M/P/E/R), new_contradictions |
| Must | 8 | — | rule_id (M1-M6), evaluation_result |
| PreCadReview | 10 | Draft→Reviewed | 5D scores, overall_pass, ai_analysis |
| Experiment | 10 | Draft→Verified | evidence_level (E0-E4), artifact_id |
| Risk | 12 | Draft→Reviewed | probability, severity, level (L/M/H/H*) |
| Want | 10 | — | weight, user_score, weighted_score |
| Decision | 12 | Draft→Reviewed | selected_route_id, signed_by |
| Gate | 6 | — | gate_id, check_result, failed_reason |

### 9.2 參考資料 (規則引擎)

| 資料 | 類型 | 數量 |
|------|------|------|
| TRIZ 39 參數 | 靜態 KB | 39 |
| TRIZ 矛盾矩陣 | 39×39 稀疏矩陣 | ~200 有效格 |
| TRIZ 40 原理 | 靜態 KB + 子原理 | 40+100 |
| 4 分離原理 | 靜態 KB | 4 |
| 76 標準解 | 靜態 KB | 76 |
| MUST 規則 M1-M6 | 可配置規則 | 6 |
| WANT 標準 W1-W6 | 種子模板 | 6 |

---

## 10. 里程碑與交付時程 (4 人團隊)

```
Week 1 ███████  M0: 基礎設施完成 (BE骨架 + DB + FE骨架)
Week 2 ███████  M1: Phase 1 API 完成 + Dashboard + Brief 頁
Week 3 ███████  M2: Phase 1 完整 (CLD + Gates) + Explore + Track 頁
Week 4 ███████  M3-1: TRIZ 引擎 + Anti-Anchor + Create 頁 (上半)
Week 5 ███████  M3-2: SCAMPER + 矛盾回饋 + MUST + Create 頁 (下半)
Week 6 ███████  M4: Pre-CAD + Phase 3 API (上半) + Review 頁
Week 7 ███████  M5: Phase 3 完整 + Decide 頁 + 前後端整合
Week 8 ███████  M6: 測試 + Prompt 調優 + 部署 + 文件
```

| 里程碑 | 時程 | 交付物 | 驗收方式 |
|--------|------|--------|---------|
| **M0** | Week 1 | BE/FE 骨架 + DB Schema + Design System | `docker-compose up` 可啟動 |
| **M1** | Week 2 | Phase 1 API (定義 + 索克拉底 + 矛盾) + 2 頁 UI | API 可呼叫，UI 可操作 |
| **M2** | Week 3 | Phase 1 完整 (CLD + Gates) + 4 頁 UI | Phase 1 端到端跑通 |
| **M3** | Week 4-5 | Phase 2 API 完整 (TRIZ + SCAMPER + MUST) | TRIZ 三路徑回傳結構化結果 |
| **M4** | Week 6 | Pre-CAD + Phase 3 API (證據 + 風險) + Review 頁 | Phase 2 端到端跑通 |
| **M5** | Week 7 | Phase 3 完整 (WANT + KT + 知識沉澱) + 全 UI | Phase 3 端到端跑通 |
| **M6** | Week 8 | 測試通過 + Docker 部署 + 文件 + eBike 案例驗證 | 真實案例全流程通過 |

---

## 11. 驗收標準

### 11.1 功能驗收

| 編號 | 驗收項目 | 驗收條件 | 驗證方式 |
|------|---------|---------|---------|
| AC-01 | 專案建立 | 輸入需求後成功建立專案並生成任務定義表 | 操作驗證 |
| AC-02 | 索克拉底問答 | 七類提問各≥2 題，共 14-21 題，品質可用 | 人工審查 |
| AC-03 | 矛盾識別 | 自動識別≥3 條矛盾，正確分類 TC/PC/SF | 人工審查 |
| AC-04 | CLD 生成 | 因果迴路圖正確表達反饋迴路 + 可標記斷路點 | 操作驗證 |
| AC-05 | Phase 1 完整 | 任務定義→索克拉底→矛盾→CLD→Phase Gate 1 通過 | E2E 測試 |
| AC-06 | 假設台帳 PDCA | 假設狀態 Open→Experimenting→Validated/Refuted 正確流轉 | 單元測試 |
| AC-07 | TRIZ 三路徑 | `POST /triz/solve` 回傳 TC+PC+SF 三路徑結構化結果 | API 測試 |
| AC-08 | SCAMPER 變形 | 7 動作 × N 子系統正確生成 + new_contradictions 回饋 | API 測試 |
| AC-09 | MUST 篩選 | M1-M6 規則正確判定 Go/No-Go | 單元測試 |
| AC-10 | Pre-CAD 5D | 5 維度 1-5 分 + overall_pass 邏輯正確 | 單元測試 |
| AC-11 | Phase 2 完整 | 假設台帳→TRIZ→SCAMPER→MUST→Pre-CAD→Phase Gate 2 通過 | E2E 測試 |
| AC-12 | 證據矩陣聚合 | Assumption × Evidence 聚合正確，E0-E4 正確計算 | 單元測試 |
| AC-13 | WANT 計算 | weighted_score = Σ(weight × score)，無計算錯誤 | 自動化測試 |
| AC-14 | KT 決策記錄 | 包含 MUST/WANT/Risk 完整彙總 + 簽核 | 操作驗證 |
| AC-15 | Phase 3 完整 | 證據→WANT→決策→知識沉澱→Phase Gate 3 通過 | E2E 測試 |
| AC-16 | 8-Gate 系統 | 所有 8 個 Gate 正確判定 pass/fail + Phase 轉換 | 單元測試 |
| AC-17 | 匯出功能 | Markdown + JSON 匯出包含所有核心章節 | 操作驗證 |

### 11.2 技術驗收

| 編號 | 驗收項目 | 驗收條件 |
|------|---------|---------|
| TA-01 | 一鍵啟動 | `docker-compose up` 前後端可用 |
| TA-02 | API 文件 | `/docs` 端點完整 OpenAPI spec |
| TA-03 | 測試覆蓋 | Service 層核心邏輯 ≥80% 覆蓋率 |
| TA-04 | 資料持久化 | 重啟後資料不遺失 |
| TA-05 | 錯誤處理 | LLM 超時有重試、格式錯誤有回報 |
| TA-06 | 回應時間 | LLM ≤60s，非 LLM ≤3s |

---

## 12. 風險管理

| 風險 | 機率 | 衝擊 | 緩解措施 |
|------|------|------|---------|
| **TRIZ 引擎複雜度超預期** | 高 | 高 | TRIZ 引擎為關鍵路徑，優先排入 Week 4 由 Senior BE 負責；KB 解析已有 prototype |
| **LLM 回應格式不穩定** | 高 | 中 | Pydantic 嚴格驗證 + retry + 結構化 prompt (JSON mode) |
| **CLD 互動圖前端複雜度** | 中 | 中 | 評估 React Flow / D3 成本；MVP 可降級為 Mermaid 靜態圖 |
| **矛盾回饋迴路無限遞迴** | 中 | 高 | 設深度 >3 層告警 + 循環偵測；分級 Fatal/Major/Minor |
| **前端 Create 頁 7 Accordion 過複雜** | 中 | 中 | 拆為子元件獨立開發；考慮改為 Tab 切換 |
| **Prompt 品質不達標** | 中 | 高 | 提早 (Week 2) 用真實案例跑 prompt；每 Sprint 迭代調優 |
| **團隊 TRIZ 領域知識不足** | 中 | 中 | 準備 TRIZ 39 參數 + 40 原理速查手冊；PM 提供 eBike 案例 context |

---

## 13. 排除範圍 (v1.1+ Backlog)

| 項目 | 排除原因 | 規劃版本 |
|------|---------|---------|
| PostgreSQL 遷移 | MVP 用 SQLite 即可 | v1.1 |
| RAG 向量資料庫整合 | MVP 用 LLM 內建知識 | v1.1 |
| WebSocket 即時更新 | HTTP 夠用 | v1.1 |
| 多語言 (i18n) | 繁體中文 only | v1.1 |
| CI/CD Pipeline | 手動部署 | v1.1 |
| SWOT 分析模組 | P2 功能 | v1.1 |
| Word/PDF 匯出 (排版精美) | MVP 先 Markdown + JSON | v1.1 |
| 多專案比較儀表板 | 先做好單專案 | v1.1 |
| 效能調優 / 快取 | MVP 不需要 | v1.1 |

---

## 14. 變更管理

- 範圍變更需評估對關鍵路徑影響，並更新 WBS
- LLM prompt 調整不算範圍變更（屬於品質調優）
- 新增功能超出 v1.0 範圍的，記錄到 v1.1 backlog
- 前端設計降級 (互動圖→靜態圖) 需 PM 同意
- TRIZ 引擎範圍縮減 (例如只做 TC 路徑) 需評估產品完整性

---

## 15. 詞彙表

| 術語 | 定義 |
|------|------|
| Phase 1: Define | 定義問題空間（任務定義 → 索克拉底七類提問 → 矛盾識別 → CLD + 斷路點） |
| Phase 2: Diverge | 假設與發散（假設台帳 → TRIZ 三路徑 → SCAMPER → 方案集合 → MUST → Pre-CAD） |
| Phase 3: Converge | 收斂與驗證（證據矩陣 → 風險登錄 → 最小實驗 → WANT → KT 決策 → 知識沉澱） |
| Gate | 階段檢查點，滿足 checklist 才進入下一階段 (共 8 個) |
| KT | Kepner-Tregoe 決策分析框架 |
| MUST | 不可妥協的硬約束，Pass/Fail (M1-M6) |
| WANT | 希望有但可妥協的目標，加權評分 (W1-W6) |
| AC | Adverse Consequences，風險矩陣評估 |
| TRIZ | 發明問題解決理論 (TC: 技術矛盾 / PC: 物理矛盾 / SF: 物質場) |
| SCAMPER | 創意發散七動作 (Substitute/Combine/Adapt/Modify/Put/Eliminate/Rearrange) |
| CLD | Causal Loop Diagram，因果迴路圖 |
| Pre-CAD | CAD 前審查，5 維度 (空間/成本/安全/解耦/供應) 1-5 分評估 |
| DR EM | Design Review Evidence Matrix，設計審查證據矩陣 |
| E0-E4 | 證據等級：E0 無數據 → E4 量產驗證 |
| Interface Contract | 介面契約，6 維度 (包封/載荷/訊號/熱/基準/維修) |
| Anti-Anchor | 反錨定衝刺，生成 ≥1 個與既有方案不相容的非典型架構 |
| Contradiction Convergence | 矛盾收斂圖，DAG 結構追蹤所有矛盾直到完全收斂 |
