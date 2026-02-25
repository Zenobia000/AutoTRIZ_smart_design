# Statement of Work (SOW)
# RD Design Copilot MVP v0.5 開發說明書

---

## 1. 專案概述

### 1.1 專案名稱
RD Design Copilot MVP (v0.5)

### 1.2 專案目標
開發一套 AI 輔助的早期概念設計系統 MVP，讓 RD 工程師能從「模糊需求」走到「可審查的 KT 決策記錄」，完成「結構化發散 → 嚴格收斂 → 最小驗證」的完整流程。

### 1.3 一句話定義
> 用最少的技術堆疊（Python + FastAPI + SQLite + Streamlit），跑通概念設計三階段流程，產出可審查的 KT 決策記錄。

---

## 2. 範圍定義

### 2.1 交付範圍 (In Scope)

#### 後端服務
| 編號 | 交付項目 | 說明 |
|------|---------|------|
| BE-1 | FastAPI 專案骨架 | 專案結構、設定管理、DB 初始化 |
| BE-2 | 資料模型 (ORM) | 15 張 table，SQLAlchemy + SQLite |
| BE-3 | 專案管理 API | 專案 CRUD + 狀態機 |
| BE-4 | Phase 1: Define API | 任務定義表、索克拉底問答、矛盾識別 |
| BE-5 | Phase 2: Diverge API | 假設台帳、TRIZ、SCAMPER、方案集合、MUST 篩選 |
| BE-6 | Phase 3: Converge API | WANT 評分、風險登錄、KT 決策記錄、最小實驗 |
| BE-7 | Gate 檢查 API | Gate 1.1/Phase Gate 1/Phase Gate 2 自動化 checklist |
| BE-8 | 匯出 API | Markdown + JSON 匯出 |
| BE-9 | LLM Service | 統一 AI 呼叫入口，7 個 prompt 模板 |

#### 前端 UI
| 編號 | 交付項目 | 說明 |
|------|---------|------|
| FE-1 | Streamlit 主框架 | Sidebar 導航 + 狀態指示 |
| FE-2 | 專案建立頁面 | 需求輸入 + 約束輸入 |
| FE-3 | Phase 1: Define 頁面 (3頁) | 任務定義、索克拉底、矛盾識別 |
| FE-4 | Phase 2: Diverge 頁面 (5頁) | 假設台帳、TRIZ、SCAMPER、方案集合、MUST |
| FE-5 | Phase 3: Converge 頁面 (4頁) | WANT 評分、風險、決策記錄、最小實驗 |
| FE-6 | Gate 檢查頁面 (3頁) | Gate 1.1/Phase Gate 1/Phase Gate 2 checklist 顯示 |
| FE-7 | 匯出頁面 | 選擇內容 + 下載 |

#### LLM Prompt 模板
| 編號 | 交付項目 | 說明 |
|------|---------|------|
| PM-1 | task_definition.md | 任務定義表生成 |
| PM-2 | socratic_questions.md | 索克拉底六類提問 |
| PM-3 | contradiction_identify.md | TRIZ 矛盾識別 |
| PM-4 | triz_solution.md | TRIZ 解法生成 |
| PM-5 | scamper_variant.md | SCAMPER 七欄變形 |
| PM-6 | alternative_generate.md | 候選方案生成 |
| PM-7 | decision_record.md | KT 決策記錄草稿 |
| PM-8 | black_hat_review.md | 黑帽審查 |

#### 測試與文件
| 編號 | 交付項目 | 說明 |
|------|---------|------|
| QA-1 | 單元測試 | Service 層核心邏輯測試 |
| QA-2 | API 整合測試 | 端到端 API 流程測試 |
| QA-3 | 端到端場景測試 | 用真實案例跑通全流程 |
| DOC-1 | README.md | 安裝/啟動/使用說明 |
| DOC-2 | API 文件 | FastAPI 自動生成 OpenAPI |
| DOC-3 | Docker 部署 | Dockerfile + docker-compose.yml |

### 2.2 排除範圍 (Out of Scope)

| 項目 | 排除原因 | 規劃版本 |
|------|---------|---------|
| 用戶認證 / SSO / LDAP | 單用戶 MVP 不需要 | v1.0 |
| 多專案並行管理 | 先做好單專案完整流程 | v1.0 |
| RAG 知識庫 / 向量資料庫 | MVP 用 LLM 內建知識 | v1.0 |
| 因果迴路圖自動繪製 | 用 Mermaid 手動 | v1.0 |
| SWOT 分析 | P1 功能 | v1.0 |
| 一頁式摘要 / FAQ / Playbook | P1-P2 功能 | v1.0 |
| Word/PDF 匯出 | MVP 先用 Markdown + JSON | v1.0 |
| WebSocket 即時更新 | HTTP 夠用 | v1.0 |
| 多語言 (i18n) | MVP 繁體中文 only | v1.0 |
| CI/CD Pipeline | 手動部署 | v1.0 |
| 效能調優 / 快取 | MVP 不需要 | v1.0 |

---

## 3. 技術規格

### 3.1 技術堆疊

| 層級 | 技術 | 版本 |
|------|------|------|
| 語言 | Python | 3.11+ |
| Web 框架 | FastAPI | 0.100+ |
| ORM | SQLAlchemy | 2.0+ |
| 資料庫 | SQLite | 3.x |
| LLM | Claude API (claude-sonnet-4-6) | latest |
| 前端 | Streamlit | 1.30+ |
| 驗證 | Pydantic | 2.0+ |
| 測試 | pytest | latest |
| 容器 | Docker + docker-compose | latest |

### 3.2 系統架構

```
Streamlit (port 8501) → FastAPI (port 8000) → SQLite (data.db)
                                             → Claude API (外部)
```

### 3.3 非功能需求 (MVP 版)

| 需求 | MVP 目標 |
|------|---------|
| LLM 回應時間 | ≤60 秒 |
| 非 LLM 操作回應 | ≤3 秒 |
| 並發用戶 | 1（單用戶） |
| 資料持久化 | SQLite 檔案 |
| 備份 | 手動複製 data.db |
| 安全 | API Key 環境變數、ORM 防 SQL injection |

---

## 4. 驗收標準

### 4.1 功能驗收

| 驗收項目 | 驗收條件 | 驗證方式 |
|---------|---------|---------|
| **AC-1** 專案建立 | 輸入需求後，成功建立專案並生成任務定義表 | 操作驗證 |
| **AC-2** Phase 1: Define 完整 | 任務定義表 → 索克拉底 → 矛盾識別 → Phase Gate 1 通過 | 端到端測試 |
| **AC-3** Phase 2: Diverge 完整 | 假設台帳 → TRIZ → SCAMPER → 方案集合 → MUST → Phase Gate 2 通過 | 端到端測試 |
| **AC-4** Phase 3: Converge 完整 | WANT 評分 → 風險 → 決策記錄 → 簽核 → Phase Gate 3 通過 | 端到端測試 |
| **AC-5** AI 生成品質 | 任務定義表包含所有必填欄位，TRIZ 解法有工程語言 | 人工審查 |
| **AC-6** WANT 計算正確 | 加權總分 = Σ(權重 × 分數)，無計算錯誤 | 自動化測試 |
| **AC-7** Gate 檢查邏輯 | Phase Gate 1/2/3 checklist 正確判斷 pass/fail | 單元測試 |
| **AC-8** 匯出完整 | Markdown 報告包含所有 8 個章節 | 操作驗證 |
| **AC-9** 證據追蹤 | 每個 WANT 評分都有證據欄位，缺證據有警告提示 | 操作驗證 |
| **AC-10** 風險矩陣 | P×S 計算正確，H* 風險有明確標示 | 單元測試 |

### 4.2 技術驗收

| 驗收項目 | 驗收條件 |
|---------|---------|
| 可啟動 | `docker-compose up` 一鍵啟動 |
| API 文件 | `/docs` 端點可查看完整 OpenAPI spec |
| 測試覆蓋 | Service 層核心邏輯測試通過 |
| 資料持久化 | 重啟後資料不遺失 |
| 錯誤處理 | LLM 超時有重試、格式錯誤有回報 |

---

## 5. 開發階段與里程碑

### 5.1 總時程：30 個工作天

```
Week 1 (Day 1-5)    ████████████  M0 + M1: 骨架 + Phase 1: Define
Week 2 (Day 6-10)   ████████████  M2: Phase 2: Diverge (上半)
Week 3 (Day 11-15)  ████████████  M2 + M3: Phase 2: Diverge (下半) + Phase 3: Converge (上半)
Week 4 (Day 16-20)  ████████████  M3: Phase 3: Converge (下半)
Week 5 (Day 21-25)  ████████████  M4: UI 串接
Week 6 (Day 26-30)  ████████████  M5 + M6: 測試 + 文件 + 部署
```

### 5.2 里程碑定義

| 里程碑 | 時程 | 交付物 | 驗收方式 |
|--------|------|--------|---------|
| **M0: 專案骨架** | Day 1-2 | 目錄結構、DB schema、FastAPI 空殼、config | `uvicorn` 可啟動 |
| **M1: Phase 1: Define** | Day 3-5 | 任務定義、索克拉底、矛盾識別 API + prompt | API 可呼叫，回應格式正確 |
| **M2: Phase 2: Diverge** | Day 6-14 | 假設台帳、TRIZ、SCAMPER、方案集合、MUST API + prompt | MUST 篩選邏輯正確 |
| **M3: Phase 3: Converge** | Day 15-20 | WANT、風險、決策記錄、最小實驗、Gate API | WANT 計算正確 |
| **M4: UI 串接** | Day 21-25 | Streamlit 全部頁面串接 API | 全流程可在 UI 操作 |
| **M5: 測試** | Day 26-28 | 單元測試 + API 測試 + 端到端 | 測試全部通過 |
| **M6: 交付** | Day 29-30 | Docker + README + 真實案例驗證 | 一鍵啟動，跑通真實案例 |

---

## 6. 交付物清單

| 類別 | 交付物 | 格式 |
|------|--------|------|
| **原始碼** | Backend (FastAPI) | Python |
| **原始碼** | Frontend (Streamlit) | Python |
| **原始碼** | LLM Prompt 模板 (8 個) | Markdown |
| **原始碼** | 測試程式碼 | Python (pytest) |
| **部署** | Dockerfile | Dockerfile |
| **部署** | docker-compose.yml | YAML |
| **部署** | .env.example | env |
| **文件** | README.md (安裝/啟動/使用) | Markdown |
| **文件** | API 文件 | OpenAPI (自動生成) |
| **文件** | 系統架構文件 (SA/SD) | Markdown |

---

## 7. 假設與前提

| 編號 | 假設 | 影響 |
|------|------|------|
| S-1 | Claude API Key 可用且有足夠 quota | LLM 功能無法運作 |
| S-2 | 開發環境有 Python 3.11+ | 無法啟動 |
| S-3 | 開發環境可訪問 Claude API (網路) | LLM 功能無法運作 |
| S-4 | 單用戶使用，不需考慮並發 | 架構簡化 |
| S-5 | 繁體中文為主要語言 | Prompt 設計以中文為主 |
| S-6 | 不需上線到公網，本地或內網部署 | 無需 HTTPS / CDN / 負載均衡 |

---

## 8. 風險管理

| 風險 | 機率 | 衝擊 | 緩解措施 |
|------|------|------|---------|
| LLM 回應格式不穩定 | 高 | 中 | Pydantic 驗證 + 重試 + fallback 提示 |
| LLM 生成品質不佳 (工程術語不精確) | 中 | 高 | 迭代 prompt，用真實案例測試調整 |
| Streamlit 效能瓶頸 (大表格) | 中 | 低 | 分頁載入，MVP 資料量小 |
| SQLite 並發限制 | 低 | 低 | MVP 單用戶，無影響 |
| Prompt 注入攻擊 | 低 | 中 | 內網部署 + 輸入 sanitize |

---

## 9. 變更管理

- 範圍變更需評估對時程影響，並更新 WBS
- LLM prompt 調整不算範圍變更（屬於品質調優）
- 新增功能超出 MVP 範圍的，記錄到 v1.0 backlog
- 技術選型變更需評估遷移成本

---

## 10. 詞彙表

| 術語 | 定義 |
|------|------|
| Phase 1: Define | 定義問題空間（任務定義 → 索克拉底 → 矛盾識別） |
| Phase 2: Diverge | 假設與發散（假設台帳 → TRIZ → SCAMPER → 方案集合 → MUST） |
| Phase 3: Converge | 收斂與驗證（WANT → 風險 → KT 決策 → 最小實驗） |
| Gate | 階段檢查點，滿足 checklist 才進入下一階段 |
| KT | Kepner-Tregoe 決策分析框架 |
| MUST | 不可妥協的硬約束，Pass/Fail |
| WANT | 希望有但可妥協的目標，加權評分 |
| AC | Adverse Consequences，風險矩陣評估 |
| TRIZ | 發明問題解決理論 |
| SCAMPER | 創意發散七動作 (Substitute/Combine/Adapt/Modify/Put/Eliminate/Rearrange) |
