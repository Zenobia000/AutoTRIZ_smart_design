# Work Breakdown Structure (WBS)
# RD Design Copilot MVP v0.5

---

## WBS 總覽

```
1.0 RD Design Copilot MVP
├── 1.1 專案初始化
├── 1.2 Backend - Phase 1: Define
├── 1.3 Backend - Phase 2: Diverge
├── 1.4 Backend - Phase 3: Converge
├── 1.5 Backend - 橫切功能
├── 1.6 LLM Prompt 開發
├── 1.7 Frontend UI
├── 1.8 測試
├── 1.9 部署與文件
└── 1.10 驗收
```

---

## WBS 詳細分解

### 1.1 專案初始化 (Day 1-2)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.1.1 | 建立專案目錄結構 | src/, ui/, tests/, data/ | 0.5d | — |
| 1.1.2 | 設定 pyproject.toml + 依賴 | pyproject.toml | 0.5d | — |
| 1.1.3 | 建立 config.py (環境變數管理) | config.py, .env.example | 0.25d | 1.1.1 |
| 1.1.4 | 建立 database.py (SQLAlchemy engine) | database.py | 0.25d | 1.1.2 |
| 1.1.5 | 定義全部 ORM models (15 tables) | models/*.py | 1d | 1.1.4 |
| 1.1.6 | 定義全部 Pydantic schemas | schemas/*.py | 0.5d | 1.1.5 |
| 1.1.7 | FastAPI main.py 空殼 + CORS | main.py | 0.25d | 1.1.3 |
| 1.1.8 | 驗證: uvicorn 可啟動, /docs 可訪問 | — | 0.25d | 1.1.7 |

**小計: 3.5d → 壓縮至 2d (並行)**

---

### 1.2 Backend - Phase 1: Define (Day 3-5)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.2.1 | 專案 CRUD API | routers/projects.py | 0.5d | 1.1 |
| 1.2.2 | 專案狀態機 Service | services/phase_service.py | 0.5d | 1.2.1 |
| 1.2.3 | 任務定義表 - API + Service | routers/definitions.py, services/definition_service.py | 0.5d | 1.2.1 |
| 1.2.4 | 任務定義表 - LLM 生成端點 | POST /definitions/generate | 0.5d | 1.2.3, 1.6.1 |
| 1.2.5 | 索克拉底問答 - API + Service | routers/questions.py | 0.5d | 1.2.1 |
| 1.2.6 | 索克拉底問答 - LLM 生成端點 | POST /questions/generate | 0.5d | 1.2.5, 1.6.2 |
| 1.2.7 | 矛盾識別 - API + Service | routers/contradictions.py | 0.5d | 1.2.1 |
| 1.2.8 | 矛盾識別 - LLM 識別端點 | POST /contradictions/identify | 0.5d | 1.2.7, 1.6.3 |
| 1.2.9 | Gate 1.1 檢查邏輯 | services/gate_service.py (gate_1_1) | 0.25d | 1.2.4 |
| 1.2.10 | Phase 1: Define 整合驗證 | API 端到端可跑通 | 0.25d | 1.2.9 |

**小計: 4.5d → 壓縮至 3d (並行)**

---

### 1.3 Backend - Phase 2: Diverge (Day 6-14)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.3.1 | 假設台帳 - CRUD API | routers/assumptions.py | 0.5d | 1.1 |
| 1.3.2 | 假設台帳 - AI 自動提取 | 從對話/矛盾中提取假設 | 0.5d | 1.3.1, 1.2.8 |
| 1.3.3 | 假設狀態管理 (pending/verified/disproved) | services/assumption_service.py | 0.25d | 1.3.1 |
| 1.3.4 | 假設 Top 3 標記 + 排序 | 標記致命假設 | 0.25d | 1.3.1 |
| 1.3.5 | TRIZ 解法 - API + Service | routers/triz.py, services/triz_service.py | 0.5d | 1.1 |
| 1.3.6 | TRIZ 解法 - LLM 生成端點 | POST /triz/generate | 0.5d | 1.3.5, 1.6.4 |
| 1.3.7 | SCAMPER 變形 - API + Service | routers/scamper.py, services/scamper_service.py | 0.5d | 1.1 |
| 1.3.8 | SCAMPER 變形 - LLM 生成端點 | POST /scamper/generate | 0.5d | 1.3.7, 1.6.5 |
| 1.3.9 | 方案集合 - CRUD API | routers/alternatives.py | 0.5d | 1.1 |
| 1.3.10 | 方案集合 - LLM 彙整生成 | POST /alternatives/generate | 1d | 1.3.9, 1.3.6, 1.3.8, 1.6.6 |
| 1.3.11 | 方案集合 - 狀態管理 | candidate/must_pass/must_fail/selected/backup/eliminated | 0.25d | 1.3.9 |
| 1.3.12 | MUST 篩選 - API + 評估邏輯 | routers/must.py | 0.5d | 1.3.9 |
| 1.3.13 | MUST 篩選 - Pass/Fail 計算 | 任一 MUST 不過 = 淘汰 | 0.25d | 1.3.12 |
| 1.3.14 | Gate 2.1 檢查邏輯 | services/gate_service.py (gate_2_1) | 0.25d | 1.3.13 |
| 1.3.15 | Phase 2: Diverge 整合驗證 | API 端到端可跑通 | 0.5d | 1.3.14 |

**小計: 6.75d → 壓縮至 5d (並行)**

---

### 1.4 Backend - Phase 3: Converge (Day 15-20)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.4.1 | WANT 條件 - CRUD API | routers/want_criteria.py | 0.5d | 1.1 |
| 1.4.2 | WANT 條件 - 預設模板載入 | 7 個標準 WANT (W1-W7) + 權重建議 | 0.25d | 1.4.1 |
| 1.4.3 | WANT 評分 - API | routers/want_scores.py | 0.5d | 1.4.1 |
| 1.4.4 | WANT 評分 - 加權計算 Service | weighted_score = weight × score | 0.25d | 1.4.3 |
| 1.4.5 | WANT 評分 - 證據完整性檢查 | 標記缺證據的評分 | 0.25d | 1.4.3 |
| 1.4.6 | 風險登錄表 - CRUD API | routers/risks.py | 0.5d | 1.1 |
| 1.4.7 | 風險矩陣計算 (P×S → Level) | services/decision_service.py | 0.25d | 1.4.6 |
| 1.4.8 | Adverse Consequences 彙整 | 按方案彙整風險 | 0.25d | 1.4.7 |
| 1.4.9 | 最小實驗 - CRUD API | routers/experiments.py | 0.5d | 1.1 |
| 1.4.10 | KT 決策記錄 - API + Service | routers/decisions.py | 0.5d | 1.4.4, 1.4.8 |
| 1.4.11 | KT 決策記錄 - LLM 草稿生成 | POST /decisions/generate | 0.5d | 1.4.10, 1.6.7 |
| 1.4.12 | KT 決策記錄 - 簽核邏輯 | PUT /decisions/signoff | 0.25d | 1.4.10 |
| 1.4.13 | Gate 3.1 檢查邏輯 | services/gate_service.py (gate_3_1) | 0.5d | 1.4.5, 1.4.8, 1.4.12 |
| 1.4.14 | Phase 3: Converge 整合驗證 | API 端到端可跑通 | 0.5d | 1.4.13 |

**小計: 5.5d → 壓縮至 4d (並行)**

---

### 1.5 Backend - 橫切功能 (穿插於 Day 3-20)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.5.1 | LLM Service 統一入口 | services/llm_service.py | 1d | 1.1 |
| 1.5.2 | LLM 重試 + 錯誤處理 | 指數退避 3 次重試 | 0.5d | 1.5.1 |
| 1.5.3 | LLM 回應 Pydantic 解析 | structured output 驗證 | 0.5d | 1.5.1 |
| 1.5.4 | 匯出 Service (Markdown) | services/export_service.py | 1d | 1.4 |
| 1.5.5 | 匯出 Service (JSON) | JSON dump 全專案資料 | 0.5d | 1.5.4 |
| 1.5.6 | 匯出 API 端點 | routers/export.py | 0.25d | 1.5.4 |

**小計: 3.75d → 穿插執行，不佔獨立時段**

---

### 1.6 LLM Prompt 開發 (穿插於 Day 3-20)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.6.1 | task_definition.md prompt | 任務定義表生成模板 | 0.5d | — |
| 1.6.2 | socratic_questions.md prompt | 索克拉底六類提問模板 | 0.5d | — |
| 1.6.3 | contradiction_identify.md prompt | TRIZ 矛盾識別模板 | 0.5d | — |
| 1.6.4 | triz_solution.md prompt | TRIZ 解法生成模板 | 0.5d | — |
| 1.6.5 | scamper_variant.md prompt | SCAMPER 七欄變形模板 | 0.5d | — |
| 1.6.6 | alternative_generate.md prompt | 候選方案生成模板 | 0.5d | — |
| 1.6.7 | decision_record.md prompt | KT 決策記錄生成模板 | 0.5d | — |
| 1.6.8 | black_hat_review.md prompt | 黑帽審查模板 | 0.25d | — |
| 1.6.9 | Prompt 品質測試 (每個 prompt 用真實案例測 3 次) | 測試記錄 | 1d | 1.6.1-1.6.8 |

**小計: 4.75d → 穿插執行，與對應 API 同步開發**

---

### 1.7 Frontend UI (Day 21-25)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.7.1 | Streamlit 主框架 + Sidebar 導航 | ui/app.py 骨架 | 0.5d | 1.2-1.4 |
| 1.7.2 | 狀態管理 (session_state) | 專案資料快取 | 0.25d | 1.7.1 |
| 1.7.3 | API Client 封裝 | ui/api_client.py | 0.5d | 1.7.1 |
| 1.7.4 | 首頁 - 專案建立 | 需求輸入 + 約束輸入 | 0.5d | 1.7.3 |
| 1.7.5 | Phase 1 - 任務定義表頁面 | AI 生成 → 編輯 → 確認 | 0.5d | 1.7.3 |
| 1.7.6 | Phase 1 - 索克拉底問答頁面 | 問題顯示 + 回答輸入 | 0.5d | 1.7.3 |
| 1.7.7 | Phase 1 - 矛盾識別頁面 | 矛盾列表 + 確認 | 0.25d | 1.7.3 |
| 1.7.8 | Phase 2 - 假設台帳頁面 | data_editor 可編輯表格 | 0.5d | 1.7.3 |
| 1.7.9 | Phase 2 - TRIZ 解法頁面 | 解法展示 + expander | 0.5d | 1.7.3 |
| 1.7.10 | Phase 2 - SCAMPER 變形頁面 | 七欄表格展示 | 0.5d | 1.7.3 |
| 1.7.11 | Phase 2 - 方案集合頁面 | 方案卡片 + expander | 0.5d | 1.7.3 |
| 1.7.12 | Phase 2 - MUST 篩選頁面 | checkbox 表格 + 結果 | 0.5d | 1.7.3 |
| 1.7.13 | Phase 3 - WANT 評分頁面 | 權重設定 + 評分表格 + 證據欄 | 1d | 1.7.3 |
| 1.7.14 | Phase 3 - 風險評估頁面 | 風險表格 + 矩陣顯示 | 0.5d | 1.7.3 |
| 1.7.15 | Phase 3 - KT 決策記錄頁面 | 完整決策記錄 + 簽核 | 1d | 1.7.3 |
| 1.7.16 | Phase 3 - 最小實驗頁面 | 實驗表單 | 0.25d | 1.7.3 |
| 1.7.17 | Gate 檢查頁面 (Phase Gate 1/2/3) | checklist 展示 | 0.5d | 1.7.3 |
| 1.7.18 | 匯出報告頁面 | 選擇內容 + download_button | 0.25d | 1.7.3 |
| 1.7.19 | UI 整合測試 (全流程點擊) | — | 0.5d | 1.7.4-1.7.18 |

**小計: 9.5d → 壓縮至 5d (並行 + 簡化)**

---

### 1.8 測試 (Day 26-28)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.8.1 | Service 層單元測試 | tests/test_services/*.py | 1d | 1.2-1.5 |
| 1.8.2 | Gate 邏輯單元測試 | tests/test_services/test_gate.py | 0.5d | 1.2.9, 1.3.14, 1.4.13 |
| 1.8.3 | WANT 計算單元測試 | tests/test_services/test_decision.py | 0.25d | 1.4.4 |
| 1.8.4 | 風險矩陣單元測試 | tests/test_services/test_risk.py | 0.25d | 1.4.7 |
| 1.8.5 | API 整合測試 | tests/test_routers/*.py | 1d | 1.2-1.4 |
| 1.8.6 | 端到端場景測試 (真實案例) | 用馬達-減速機案例跑全流程 | 1d | 1.7 |

**小計: 4d → 壓縮至 3d (並行)**

---

### 1.9 部署與文件 (Day 29-30)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.9.1 | Dockerfile (backend) | Dockerfile | 0.25d | 1.2-1.5 |
| 1.9.2 | Dockerfile (frontend) | Dockerfile.ui | 0.25d | 1.7 |
| 1.9.3 | docker-compose.yml | docker-compose.yml | 0.25d | 1.9.1, 1.9.2 |
| 1.9.4 | README.md | 安裝/啟動/使用說明 | 0.5d | 1.9.3 |
| 1.9.5 | .env.example | 環境變數範本 | 0.1d | — |
| 1.9.6 | Docker 啟動驗證 | docker-compose up 測試 | 0.25d | 1.9.3 |

**小計: 1.6d → 壓縮至 1d**

---

### 1.10 驗收 (Day 30)

| WBS | 任務 | 產出 | 工時 | 前置 |
|-----|------|------|------|------|
| 1.10.1 | AC-1 ~ AC-10 驗收檢查 | 驗收報告 | 0.5d | 1.8, 1.9 |
| 1.10.2 | Bug 修復 buffer | — | 0.5d | 1.10.1 |

**小計: 1d**

---

## 甘特圖 (簡化版)

```
        Day:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
              │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
1.1 初始化    ████
1.2 Phase 1        ██████████
1.3 Phase 2                  ██████████████████████████████
1.4 Phase 3                                                ████████████████████
1.5 橫切功能     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
1.6 Prompt       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
1.7 UI                                                                           ██████████████████
1.8 測試                                                                                          ██████████
1.9 部署                                                                                                    ████
1.10 驗收                                                                                                       ██

████ = 主要工作    ░░░░ = 穿插執行
```

---

## 工時統計

| WBS 大類 | 估算工時 | 壓縮後工時 | 佔比 |
|---------|---------|-----------|------|
| 1.1 初始化 | 3.5d | 2d | 7% |
| 1.2 Phase 1: Define | 4.5d | 3d | 10% |
| 1.3 Phase 2: Diverge | 6.75d | 5d | 17% |
| 1.4 Phase 3: Converge | 5.5d | 4d | 13% |
| 1.5 橫切功能 | 3.75d | (穿插) | — |
| 1.6 Prompt | 4.75d | (穿插) | — |
| 1.7 UI | 9.5d | 5d | 17% |
| 1.8 測試 | 4d | 3d | 10% |
| 1.9 部署文件 | 1.6d | 1d | 3% |
| 1.10 驗收 | 1d | 1d | 3% |
| **Buffer** | — | **6d** | **20%** |
| **總計** | **44.85d** | **30d** | **100%** |

> Buffer 20% 用於：prompt 品質調優、LLM 回應格式 debug、UI 微調、未預見問題。

---

## 關鍵路徑

```
1.1 初始化 → 1.2 Phase 1: Define → 1.3 Phase 2: Diverge → 1.4 Phase 3: Converge → 1.7 UI → 1.8 測試 → 1.9 部署 → 1.10 驗收
```

任何一個環節延遲都會影響最終交付。最高風險在：
1. **1.6 Prompt 品質** — LLM 回應格式/品質不穩定需要迭代
2. **1.7 UI 串接** — Streamlit 複雜表格互動可能比預期費時
3. **1.3.10 方案生成** — 最複雜的 LLM 整合點（TRIZ + SCAMPER → 方案）
