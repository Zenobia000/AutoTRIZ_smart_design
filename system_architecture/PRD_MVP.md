# PRD - RD Design Copilot MVP (v0.5)

---

## MVP 哲學

> **"Talk is cheap. Show me the code."** — Linus Torvalds
>
> MVP 只做一件事：讓一個 RD 工程師能從「模糊需求」走到「可審查的 KT 決策記錄」。
> 不做帳號系統、不做多租戶、不做花俏 UI。先跑通核心流程。

---

## 1. MVP 範圍定義

### 1.1 做什麼（In Scope）

| 功能 | MVP 版本 | 說明 |
|------|---------|------|
| F1.1 任務定義表生成 | **V** | LLM 生成，用戶確認/修改 |
| F1.2 索克拉底問答 | **V** | LLM 生成 6 類提問 |
| F1.3 矛盾識別 | **V** | LLM 從對話中提取 TRIZ 矛盾句 |
| F2.1 假設台帳管理 | **V** | CRUD + 狀態追蹤 |
| F2.2 TRIZ 解法生成 | **V** | LLM 生成結構化解法 |
| F2.3 SCAMPER 變形 | **V** | LLM 生成 7 欄結構化輸出 |
| F2.4 方案集合管理 | **V** | CRUD + 結構化存儲 |
| F2.5 MUST 快篩 | **V** | Pass/Fail 表格 |
| F3.2 風險登錄表 | **V** | CRUD |
| F3.3 KT WANT 評分 | **V** | 加權計算，強制證據欄 |
| F3.4 Adverse Consequences | **V** | 風險矩陣 |
| F3.5 KT 決策記錄生成 | **V** | LLM 生成草稿，人簽核 |
| F3.6 最小實驗設計 | **V** | 結構化表單 |
| Gate 1/2/3 檢查 | **V** | 簡單 checklist 驗證 |

### 1.2 不做什麼（Out of Scope for MVP）

| 功能 | 原因 |
|------|------|
| 用戶認證/SSO | 先單用戶跑通流程 |
| 多專案管理 | 先做好一個專案的完整流程 |
| F1.4 因果迴路圖自動繪製 | 用 Mermaid 手動畫，P1 再自動化 |
| F3.1 SWOT 分析 | P1 |
| F4.1-F4.4 溝通沉澱 | P1，MVP 先用 Markdown 匯出 |
| 知識庫/RAG | P1，MVP 先用 LLM 內建知識 |
| 向量資料庫 | 不需要，MVP 沒有 RAG |
| WebSocket 即時更新 | 不需要，HTTP 夠用 |

---

## 2. MVP 用戶旅程（單一 Happy Path）

```
用戶輸入需求描述
    ↓
[Phase I] AI 生成任務定義表 → 用戶修改確認
    ↓                         → AI 提出索克拉底問題 → 用戶回答
    ↓                         → AI 識別矛盾 → 用戶確認
    ↓                         → Gate 1 檢查
    ↓
[Phase II] AI 建立假設台帳 → 用戶補充/修改
    ↓                       → AI 生成 TRIZ 解法
    ↓                       → AI 生成 SCAMPER 變形
    ↓                       → 用戶彙整方案集合
    ↓                       → MUST 快篩
    ↓                       → Gate 2 檢查
    ↓
[Phase III] 用戶設定 WANT 權重
    ↓                        → 用戶基於證據評分
    ↓                        → AI 計算加權分
    ↓                        → 風險評估 (AC)
    ↓                        → AI 生成 KT 決策記錄草稿
    ↓                        → 用戶簽核
    ↓                        → Gate 3 檢查
    ↓
匯出 Markdown 報告
```

---

## 3. MVP 成功標準

| 指標 | 目標 |
|------|------|
| 一個 RD 能在 2 小時內走完全流程 | Yes |
| 產出的 KT 決策記錄包含所有必填欄位 | 100% |
| 每個 WANT 評分都有證據欄位 | 100% |
| 方案至少生成 3 條架構級路線 | Yes |
| 系統回應時間 | LLM 步驟 ≤60s，其他 ≤3s |

---

## 4. MVP 技術約束

| 約束 | MVP 選擇 | 理由 |
|------|---------|------|
| 部署方式 | 本地 Docker 或直接 `python main.py` | 最快能跑 |
| 資料庫 | SQLite | 零配置，單檔案 |
| LLM | Claude API (claude-sonnet-4-6) | 品質/成本平衡 |
| 前端 | Streamlit 或 簡單 React SPA | Streamlit 最快出 MVP |
| 檔案儲存 | 本地檔案系統 | 不需要 S3 |
| 認證 | 無 | 單用戶 MVP |

---

## 5. MVP 里程碑

| 里程碑 | 時程 | 交付物 |
|--------|------|--------|
| M0: 專案骨架 | Day 1-2 | FastAPI + SQLite + 基本 model |
| M1: Phase I 核心 | Day 3-7 | 任務定義表 + 索克拉底 + 矛盾識別 |
| M2: Phase II 核心 | Day 8-14 | 假設台帳 + TRIZ + SCAMPER + 方案集合 + MUST |
| M3: Phase III 核心 | Day 15-21 | KT WANT + AC + 決策記錄 + Gate |
| M4: UI 串接 | Day 22-28 | Streamlit UI 走通全流程 |
| M5: 端到端測試 | Day 29-30 | 用真實案例跑一遍 |
