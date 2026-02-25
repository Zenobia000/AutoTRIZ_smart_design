# AI Agent 架構設計：RD Design Copilot E2E 自動化

> **版本**：v1.1 | **日期**：2026-02-25
> **目的**：從 AI Agent 角度重新梳理 E2E 流程，定義自動化等級與多代理協作機制，重點解決 RD 路徑依賴問題。
> **對齊依據**：`RD_Design_Copilot_整合流程.md` v1.4 + `RD_Design_Copilot_State_Machine.md` v1.2

---

## §1 Multi-Agent 架構總覽

### 1.1 Agent 角色定義

| Agent | 職責 | 核心能力 | 綁定工具 |
|-------|------|---------|---------|
| **Analyst Agent** | 需求解構、索克拉底問答、因果迴路建模、矛盾識別、假設質疑 | 語意理解、結構化拆解、隱含假設偵測 | LLM、Prompt Template、Functional Model Generator |
| **TRIZ Solver Agent** | AutoTRIZ 規則查表 + LLM 原理具體化 + SCAMPER 變形 | 矛盾矩陣查表、分離原理匹配、76 標準解映射、原理實體化 | TRIZ Knowledge Base (Prompt MD)、LLM、RAG |
| **Evaluator Agent** | MUST 規則驗證、KT 決策分析、證據品質評分、Gate 判定 | 規則引擎、加權評分、風險評估 | MUST Rulebook、Evidence Matrix、Risk Register、LLM |
| **Knowledge Agent** | 企業 RAG 檢索、Web 文獻搜尋、跨域類比、知識回寫 | 向量檢索、Web Scraping、文件分類、Citation 生成 | Vector DB、Web Search API、Document Store |

### 1.2 Orchestrator（編排器）

- 負責 Step 流轉、Gate 判定、Agent 調度
- 維護 Process State Machine（對接現有雙層狀態機）
- 管理 Artifact 版本狀態（Draft → Reviewed → Verified → Baselined → Released）

### 1.3 架構圖

```mermaid
graph TB
    subgraph Orchestrator["Orchestrator 編排器"]
        SM["State Machine"]
        GE["Gate Engine"]
    end

    subgraph Agents["Agent Pool"]
        AA["Analyst Agent"]
        TA["TRIZ Solver Agent"]
        EA["Evaluator Agent"]
        KA["Knowledge Agent"]
    end

    subgraph Tools["Tool Layer"]
        LLM["LLM API"]
        TRIZ_KB["TRIZ Knowledge Base"]
        RAG["Enterprise RAG"]
        WEB["Web Search"]
        MUST["MUST Rulebook"]
        EM["Evidence Matrix"]
    end

    subgraph Human["Human-in-the-Loop"]
        RD["RD Engineer"]
        TL["Tech Lead"]
    end

    SM -->|dispatch| AA
    SM -->|dispatch| TA
    SM -->|dispatch| EA
    SM -->|dispatch| KA
    GE -->|gate result| SM

    AA --> LLM
    TA --> TRIZ_KB
    TA --> LLM
    EA --> MUST
    EA --> EM
    KA --> RAG
    KA --> WEB

    EA -->|gate check| GE
    RD -->|approve/reject| GE
    TL -->|approve/reject| GE
```

---

## §2 逐步自動化分級

### 2.1 自動化等級定義

| 等級 | 說明 | AI 角色 | 人類角色 |
|------|------|---------|---------|
| **Fully Auto** | AI 獨立完成，人類僅在最終選擇時介入 | 執行者 | 選擇者 |
| **AI-Driven** | AI 主導產出，人類審核確認 | 主導者 | 審核者 |
| **AI-Assisted** | 人類主導決策，AI 提供分析與建議 | 顧問 | 決策者 |
| **Human-Led** | 人類主導，AI 僅做格式化或紀錄 | 記錄者 | 主導者 |

### 2.2 E2E 步驟自動化對照表

> 步驟名稱與編號完全對齊 `RD_Design_Copilot_State_Machine.md` Step 編號對照表。

| Step | 正式名稱 | Phase | 自動化等級 | 主要 Agent | 人類角色 | 路徑依賴風險 | 核心工件 |
|------|---------|-------|-----------|-----------|---------|-------------|---------|
| **1** | **問題界定** (白帽 + 5W1H) | I | AI-Assisted | Analyst + Knowledge | 提供原始需求、確認約束句 | 低 | Constraint |
| **2** | **理解全貌** (索克拉底問答) | I | **AI-Driven** | Analyst + Knowledge | 參與問答、確認假設與矛盾 | **高** — 慣用架構偏見 | Contradiction, Assumption |
| **3** | **系統建模** (因果迴路 + TRIZ 矛盾 + 斷路點) | I | **AI-Driven** | Analyst + TRIZ Solver | 校準矛盾句、確認斷路點 | **高** — 傾向忽略矛盾 | Contradiction, Breakpoint |
| **4** | **假設與驗證規劃** (HDA + 未知集合) | II | AI-Assisted | Analyst + Knowledge | 填寫假設台帳、定義未知集合 | 中 | Assumption |
| **5-0** | **Anti-Anchor Sprint** (反路徑依賴) | II | **Fully Auto** | Analyst + Knowledge | 審核非典型架構 | **最高** — Anti-Anchor 核心 | — |
| **5a** | **TRIZ 解矛盾** (矩陣查表 + 原理具體化) | II | **Fully Auto** | TRIZ Solver + Knowledge | 僅選擇 | **高** — 解法錨定 | Concept Route (部分) |
| **5b** | **子系統定義** (受影響子系統識別) | II | AI-Driven | Analyst | 確認子系統清單 | 中 | Concept Route (部分) |
| **5c** | **SCAMPER 模組變形** (每子系統 × 7 動作) | II | **Fully Auto** | TRIZ Solver + Knowledge | 僅選擇 | 高 — 變形慣性 | Concept Route (部分) |
| **5d** | **AI 方案生成** (整合 TRIZ + SCAMPER) | II | **AI-Driven** | Analyst + TRIZ Solver | 審核方案規格 | 中 | Concept Route, Interface |
| **5e** | **MUST 快篩** (Go/No-Go 淘汰) | II | **AI-Driven** | Evaluator | 確認 MUST 判定結果 | 低 | Concept Route |
| **P** | **Pre-CAD 設計審查** (Pre-CAD Gate) | II | **AI-Driven** | Evaluator | 審核 Gate P 結果、決策保留路線 | 低 | Pre-CAD Review Report |
| **6** | **設計審查** (CAD Gate - MVP CAD Review) | III | AI-Assisted | Evaluator + Knowledge | 繪製 MVP CAD、填寫 DR EM、黑帽質疑 | 低 | Evidence Matrix, Risk, MVP CAD Model |
| **6e** | **證據補齊** (Evidence Closure) | III | AI-Assisted | Knowledge + Evaluator | 設計/執行最小實驗、收集證據 | 低 | Evidence |
| **7** | **決策與行動** (KT Decision Analysis + 最小實驗) | III | Human-Led | Evaluator | 執行 KT 決策 (MUST→WANT→AC)、簽核 | 低 | Decision Record |
| **8** | **內化與傳達** (費曼) | III | **Fully Auto** | Knowledge | 無需介入（知識回寫自動化） | 無 | Asset |

### 2.3 與 State Machine R&R 對照

| Step | State Machine 中的 Human R&R | State Machine 中的 AI R&R | Agent 映射 |
|------|---------------------------|-------------------------|-----------|
| 1 | 定義 Mission / Hard Constraints / Soft Objectives | 改寫約束句、生成缺口問卷 | Analyst Agent |
| 2 | 參與索克拉底問答、識別矛盾 | 固定執行六類提問、匯總矛盾列表 | Analyst Agent |
| 3 | 輔助因果迴路圖、正式化矛盾句 | 協助繪製因果迴路、提供 TRIZ 模板 | Analyst + TRIZ Solver |
| 4 | 填寫假設台帳、定義未知集合 | 提供模板、整理未知因子 | Analyst + Knowledge |
| 5 | 定義子系統、審查方案、執行 MUST | Anti-Anchor / TRIZ / SCAMPER / 方案生成 / MUST 快篩 | TRIZ Solver + Analyst + Evaluator |
| P | 依 Pre-CAD 模板審查、決策保留路線 | 提供模板、匯總審查結果 | Evaluator |
| 6 | 繪製 MVP CAD、填 DR EM、黑帽質疑 | 提供模板、失效案例比對 | Evaluator + Knowledge |
| 6e | 設計/執行最小實驗 | 協助實驗設計、歸檔證據 | Knowledge |
| 7 | KT 決策 (WANT 評分 + AC)、簽核 | 提供 KT 模板、整理風險矩陣 | Evaluator |
| 8 | 製作摘要、編寫 FAQ | 知識沉澱為可重用資產 | Knowledge |

---

## §3 打破路徑依賴的 AI 機制

### 3.1 問題定義

RD 路徑依賴的典型表現：

| 症狀 | 描述 | 影響的 Step |
|------|------|-----------|
| **慣用架構偏見** | 直接套用過去成功方案的架構 | Step 2 理解全貌 |
| **矛盾盲視** | 忽略或低估技術矛盾，跳過 TRIZ | Step 3 系統建模 |
| **錨定效應** | 第一個想到的方案成為基準，後續方案僅為微調 | Step 5-0 / 5a / 5c |
| **隱含假設** | 將假設當作事實，未質疑技術前提 | Step 2-4 |
| **經驗慣性** | 只搜尋熟悉領域的解法，忽略跨域靈感 | Step 5a / 5c |

### 3.2 AI 對抗機制

#### 機制 1：Assumption Challenge（假設質疑）
- **觸發點**：Step 2 索克拉底問答過程中
- **執行者**：Analyst Agent
- **對齊**：整合流程 §Step 2 六類提問中的「假設」與「反思」類
- **作法**：
  1. 從索克拉底問答中提取所有隱含假設（如「必須用齒輪傳動」）
  2. 對每個假設提出反問：「如果不用 X，還有什麼替代方案？」
  3. 產出 Assumption Register，標記 `challenged` / `confirmed`
- **產出物**：Assumption 工件（Draft），供 Step 4 假設台帳引用

#### 機制 2：Forced Divergence（強制發散）
- **觸發點**：Step 5-0 Anti-Anchor Sprint + Step 5a TRIZ 解矛盾
- **執行者**：TRIZ Solver Agent + Analyst Agent
- **對齊**：整合流程 §5.1 Anti-Anchor Sprint 規則
- **作法**：
  1. Step 5-0 產出 3 種「非典型架構」概念（整合流程原文規則）
  2. Step 5a 每個矛盾至少產出 3 條工程對映
  3. 至少 1 條必須是「跟競品在物理介面或核心機制上不相容」的路線
- **閾值**：Anti-Anchor Gate — 三條概念路線中至少一條非對標且初步通過 M1 + M4

#### 機制 3：Cross-Domain Analogical Search（跨域類比搜尋）
- **觸發點**：Step 5a / 5c 並行執行期間
- **執行者**：Knowledge Agent
- **作法**：
  1. 將核心矛盾抽象為功能語言（如「在有限空間內散熱」→「受限空間的能量轉移」）
  2. 搜尋異業專利與論文（醫療器材、航太、消費電子）
  3. 將異業解法翻譯回 eBike 領域語言
- **產出物**：≥2 條跨域類比方案，附 citation（KB-/WEB- 格式）

#### 機制 4：Anti-Anchor Gate（反錨定閘門）
- **觸發點**：Step 5-0 → Step 5a 之間（對齊 State Machine 的 Anti-Anchor Gate）
- **執行者**：Evaluator Agent
- **對齊**：整合流程 §5.1 Anti-Anchor Gate 檢查點
- **作法**：
  1. 檢查三條概念路線是否有至少一條「非對標」
  2. 非對標路線須初步通過 M1（空間約束）和 M4（解耦程度）
  3. 不通過 → 回退 Step 5-0 重新發散

#### 機制 5：Diversity Score 指標
- **觸發點**：Step 5e MUST 快篩後、進入 Gate P 前
- **執行者**：Evaluator Agent
- **定義**：基於候選方案的功能結構向量，計算成對餘弦距離的平均值
- **公式**：`DS = mean(1 - cos_sim(route_i, route_j))` for all i ≠ j
- **門檻**：DS ≥ 0.4 且保留路線 ≥ 3 條（含 ≥1 條 Anti-Anchor）才能進入 Gate P

---

## §4 Agent 間協作流程

### 4.1 主流程序列圖

```mermaid
sequenceDiagram
    participant RD as RD Engineer
    participant ORC as Orchestrator
    participant AA as Analyst Agent
    participant TA as TRIZ Solver Agent
    participant EA as Evaluator Agent
    participant KA as Knowledge Agent

    Note over ORC: Phase I: 定義問題空間

    RD->>ORC: 提交設計需求
    ORC->>AA: Step 1 問題界定 - 結構化約束句
    ORC->>KA: Step 1 - 檢索歷史案例/產業基準
    AA-->>ORC: Constraint (Draft)
    KA-->>ORC: 知識補充 (KB-/WEB-)
    ORC->>EA: Gate 1 檢查
    EA-->>ORC: Gate 1 通過 (DRAFT→PHASE_I)

    ORC->>AA: Step 2 理解全貌 - 索克拉底六類提問
    ORC->>KA: Step 2 - 歷史假設/失效機制文獻
    AA-->>ORC: Contradiction (Draft) + Assumption (Draft)
    ORC->>AA: Step 2 - Assumption Challenge (假設質疑)
    AA-->>ORC: Assumption Register
    ORC->>RD: 審核矛盾列表 + 假設清單
    RD-->>ORC: 確認/修正
    ORC->>EA: Gate 2 檢查
    EA-->>ORC: Gate 2 通過

    ORC->>AA: Step 3 系統建模 - 因果迴路圖
    ORC->>TA: Step 3 - TRIZ 矛盾正式化 (LLM翻譯 + 規則驗證)
    ORC->>KA: Step 3 - FMEA/8D 歷史因果鏈
    AA-->>ORC: 因果迴路圖 + 斷路點
    TA-->>ORC: TRIZ 矛盾句 (Contradiction Verified)
    ORC->>RD: 校準矛盾句
    RD-->>ORC: 確認
    ORC->>EA: Gate 3 檢查
    EA-->>ORC: Gate 3 通過 (PHASE_I→PHASE_II)

    Note over ORC: Phase II: 假設與發散

    ORC->>AA: Step 4 假設與驗證規劃 - 假設台帳
    ORC->>KA: Step 4 - 過往驗證方法/成本紀錄
    AA-->>ORC: Assumption (Verified)
    ORC->>RD: 確認假設台帳 + 未知集合
    RD-->>ORC: 確認
    ORC->>EA: Gate 4 檢查
    EA-->>ORC: Gate 4 通過

    ORC->>AA: Step 5-0 Anti-Anchor Sprint
    ORC->>KA: Step 5-0 - 跨域架構搜尋
    AA-->>ORC: 3 種非典型架構概念
    ORC->>EA: Anti-Anchor Gate 檢查
    EA-->>ORC: Anti-Anchor Gate 通過

    Note over ORC: Step 5 內部並行發散
    par TRIZ 解矛盾 (每條矛盾獨立)
        ORC->>TA: Step 5a - 矩陣查表 + 原理具體化
        ORC->>KA: Step 5a - 佐證搜尋 (專利/文獻)
        TA-->>ORC: 每條矛盾 ≥3 條工程對映
    and SCAMPER 變形 (每個子系統獨立)
        ORC->>AA: Step 5b - 子系統定義
        AA-->>ORC: 子系統清單
        ORC->>TA: Step 5c - SCAMPER 模組變形
        TA-->>ORC: 每子系統 × 7 動作變形
    end

    ORC->>AA: Step 5d AI 方案生成 - 整合 TRIZ + SCAMPER
    AA-->>ORC: Concept Route (Draft) + Interface Contract

    ORC->>EA: Step 5e MUST 快篩
    EA-->>ORC: 快篩結果 (保留 3-5 條路線)

    ORC->>EA: Diversity Score 檢查
    alt DS < 0.4 或 Anti-Anchor 路線 = 0
        ORC->>TA: 補充非常規路線
        TA-->>ORC: 額外路線
    end

    ORC->>EA: Gate P 檢查 (Pre-CAD Gate)
    EA-->>ORC: Gate P 結果
    ORC->>RD: Step P Pre-CAD 設計審查
    RD-->>ORC: 保留 3-5 條路線
    ORC->>EA: Gate C 檢查 (CAD Gate)
    EA-->>ORC: Gate C 結果 (PHASE_II→PHASE_III)

    Note over ORC: Phase III: 收斂與驗證

    RD->>ORC: Step 6 設計審查 - MVP CAD + DR EM
    ORC->>KA: Step 6 - 歷史失效案例比對
    ORC->>EA: Step 6 - 證據品質評分

    loop 證據補齊迴圈
        ORC->>EA: 檢查證據缺口
        alt 北極星證據 < E2
            ORC->>AA: Step 6e 證據補齊 - 實驗設計
            ORC->>KA: Step 6e - 方法檢索
            RD->>ORC: 實驗數據回傳
            ORC->>EA: 更新 Evidence Matrix
        end
    end

    ORC->>RD: Step 7 決策與行動 - KT Decision Analysis
    ORC->>EA: Step 7 - KT 評分輔助 (WANT + AC)
    RD-->>ORC: KT 決策記錄簽核
    ORC->>EA: Gate 7 檢查
    EA-->>ORC: Gate 7 通過

    ORC->>KA: Step 8 內化與傳達 - 知識回寫
    KA-->>ORC: 回寫完成 (6 類資產)
    ORC->>EA: Gate 8 檢查
    EA-->>ORC: Gate 8 通過 (PHASE_III→COMPLETED)
```

### 4.2 並行處理規則

> 對齊 State Machine §平行處理說明：「不同矛盾句的 TRIZ 解法、不同子系統的 SCAMPER 變形可並行執行」。

| 可並行的組合 | 前置條件 | 說明 |
|-------------|---------|------|
| 不同矛盾句的 5a (TRIZ 解矛盾) | Gate 4 通過 + Anti-Anchor Gate 通過 | 每條矛盾獨立求解 |
| 不同子系統的 5c (SCAMPER 變形) | 5b 子系統清單已定義 | 每個子系統獨立變形 |
| 5a (TRIZ) 與 5b→5c (子系統→SCAMPER) | Anti-Anchor Gate 通過 | TRIZ 和 SCAMPER 為互補路徑 |
| Knowledge Agent 預檢索 + 主流程 | 任何 Step | Knowledge Agent 可提前快取 |

> **注意**：5b（子系統定義）依賴 5a（TRIZ 解矛盾）的解法方向指出受影響子系統，但不同矛盾的 5a 可與不同子系統的 5c 並行。所有並行產出匯聚到 5d (AI 方案生成) 做交叉組合，再由 5e (MUST 快篩) 統一淘汰。

### 4.3 Gate 自動化判定

> 對齊 State Machine §Gate 與 Phase 轉換對照表，完整列出所有 Gate。

| Gate | 位置 | Gate 類型 | Phase 轉換 | 可否自動 | 判定邏輯 | Fallback |
|------|------|-----------|-----------|---------|---------|---------|
| **Gate 1** | Step 1 → Step 2 | 內部 Gate | **DRAFT → PHASE_I** | AI-Driven | 三個最不能失敗指標已明確且可量測 | 人類覆審 |
| **Gate 2** | Step 2 → Step 3 | 內部 Gate | Phase I 內部 | AI-Driven | ≥10 條假設 + Top 3 致命假設 + ≥3 條核心矛盾 | 人類覆審 |
| **Gate 3** | Step 3 → Step 4 | 內部 Gate | **PHASE_I → PHASE_II** | AI-Driven | ≥1 因果迴路 + ≥3 斷路點 + 每條矛盾有 TRIZ 正式句 | 人類覆審 |
| **Gate 4** | Step 4 → Step 5 | 內部 Gate | Phase II 內部 | AI-Driven | Top 3 假設每個有 1-2 週內可完成的驗證設計 | 人類覆審 |
| **Anti-Anchor** | Step 5-0 → Step 5a | 內部 Gate | Phase II 內部 | **Fully Auto** | ≥1 非對標路線且初步通過 M1 + M4 | 自動回退 5-0 |
| **Gate P** | Step 5 → Step P | **Pre-CAD Gate** | Phase II 內部 | AI-Driven | ≥3 條架構級路線 + ≥1 Anti-Anchor + 每條有完整方案規格 + DS ≥ 0.4 | 人類覆審 |
| **Gate C** | Step P → Step 6 | **CAD Gate** | **PHASE_II → PHASE_III** | Human-Led | 候選收斂至 3-5 條 + Interface Contract 已更新 + 最小 CAD 範圍明確 | N/A |
| **Gate 6** | Step 6 → Step 6e | 內部 Gate | Phase III 內部 | AI-Driven | 北極星指標證據 ≥ E2，否則進入 6e 迴圈 | 人類覆審 |
| **Gate 7** | Step 7 → Step 8 | 內部 Gate | Phase III 內部 | Human-Led | KT 決策記錄完整已簽核 + 所有 H 風險有緩解 | N/A |
| **Gate 8** | Step 8 → Done | 內部 Gate | **PHASE_III → COMPLETED** | AI-Driven | 所有核心工件 Baselined → Released | 人類覆審 |

### 4.4 Artifact State 轉換（對齊 State Machine）

| Step | 核心工件 | 狀態轉換 |
|------|---------|---------|
| Step 1 → Gate 1 | Constraint | Draft → Reviewed |
| Step 2 → Gate 2 | Contradiction, Assumption | Draft → Reviewed |
| Step 3 → Gate 3 | Contradiction | Reviewed → Verified |
| Step 3 → Gate 3 | Breakpoint | Draft → Reviewed |
| Step 4 → Gate 4 | Assumption | Reviewed → Verified |
| Step 5e → Gate P | Concept Route, Interface | Draft → Reviewed |
| Step P → Gate C | Concept Route | Reviewed → Verified |
| Step P → Gate C | Pre-CAD Review Report | Draft → Reviewed |
| Step 6 → Gate 6 | Evidence Matrix, Risk | Draft → Reviewed |
| Step 6 → Gate C | MVP CAD Model | Draft → Reviewed |
| Step 7 → Gate 7 | Concept Route | Verified → Baselined |
| Step 7 → Gate 7 | Decision Record | Draft → Reviewed |
| Step 8 → Gate 8 | All Core Artifacts | Baselined → Released |

---

## §5 打破路徑依賴的 AI 機制（詳細設計）

### 5.1 路徑依賴風險熱力圖

```
Step:    1     2     3     4    5-0   5a    5b    5c    5d    5e     P     6    6e     7     8
Risk:   🟢   🔴   🔴   🟡   🔴   🔴   🟡   🟡   🟡   🟢   🟢   🟢   🟢   🟢   ⚪
AI介入: ◐    ●    ●    ◐    ●    ●    ●    ●    ●    ●    ●    ◐    ◐    ○    ●

圖例：🔴 高風險  🟡 中風險  🟢 低風險  ⚪ 無風險
      ● Fully Auto / AI-Driven  ◐ AI-Assisted  ○ Human-Led
```

> **設計原則**：路徑依賴風險越高的步驟，AI 介入程度越深。正是因為人類在 Step 2（慣用架構）、Step 3（矛盾盲視）、Step 5-0/5a（錨定效應）最容易陷入慣性，才需要 AI 強制介入打破錨定。

### 5.2 機制與 Step 對應表

| AI 機制 | 觸發 Step | Agent | 對齊整合流程章節 |
|---------|----------|-------|----------------|
| Assumption Challenge | Step 2 | Analyst | §Step 2 索克拉底六類提問 |
| Forced Divergence | Step 5-0 + 5a | TRIZ Solver + Analyst | §5.1 Anti-Anchor Sprint + §5a TRIZ 解矛盾 |
| Cross-Domain Search | Step 5a/5c 並行 | Knowledge | §5.0 知識增強輸入 (Web 外部專利/新材料) |
| Anti-Anchor Gate | Step 5-0 → 5a | Evaluator | §5.1 Anti-Anchor Gate 檢查點 |
| Diversity Score | Step 5e → Gate P | Evaluator | §Gate 5 檢查點 (≥3 路線 + ≥1 Anti-Anchor) |

---

## §6 技術實作建議

### 6.1 推薦框架：LangGraph

選擇理由：
- 原生支援有狀態的多 Agent 圖（State Graph）
- 與現有雙層狀態機設計高度吻合
- 支援條件分支、並行節點、人類介入節點（`interrupt_before` / `interrupt_after`）
- Python 生態，可直接對接 FastAPI 後端

### 6.2 Agent-Tool 綁定

```yaml
analyst_agent:
  llm: claude-sonnet-4-6
  tools:
    - functional_model_generator  # Step 3 產出因果迴路圖 + 功能樹
    - assumption_extractor        # Step 2 假設質疑
    - scamper_checklist           # Step 5c SCAMPER 模板 (交由 TRIZ Solver 執行)
    - anti_anchor_generator       # Step 5-0 非典型架構生成
  prompts:
    - system: "你是一位機械工程系統分析師..."

triz_solver_agent:
  llm: claude-sonnet-4-6
  tools:
    - triz_parameter_mapper       # Step 3 自然語言 → 39 參數
    - contradiction_matrix_lookup # Step 5a-1 矛盾矩陣查表
    - separation_principle_match  # Step 5a-2 物理矛盾 → 分離原理
    - standard_solution_match     # Step 5a-3 Su-Field → 76 標準解
    - principle_instantiator      # Step 5a-4 抽象原理 → 工程手段
    - scamper_transformer         # Step 5c SCAMPER 模組變形
  knowledge_base:
    - triz_knowledge_base/01_39_parameters.md
    - triz_knowledge_base/02_contradiction_matrix.md
    - triz_knowledge_base/03_40_principles.md
    - triz_knowledge_base/04_separation_principles.md
    - triz_knowledge_base/05_76_standard_solutions.md

evaluator_agent:
  llm: claude-sonnet-4-6
  tools:
    - must_rule_checker           # Step 5e MUST 快篩
    - kt_scorer                   # Step 7 KT 加權評分 (WANT + AC)
    - evidence_quality_assessor   # Step 6 E-level 評估
    - diversity_score_calculator  # Gate P 前方案多樣性
    - pre_cad_reviewer            # Step P 5 維度審查
    - anti_anchor_gate_checker    # Step 5-0→5a 反錨定檢查
  templates:
    - MUST_Rulebook_Template.md
    - Pre_CAD_Review_Template.md
    - Evidence_Matrix_Risk_Register_Template.md

knowledge_agent:
  llm: claude-haiku-4-5  # 快速檢索用輕量模型
  tools:
    - enterprise_rag_search       # 企業知識庫 (FMEA/8D/決策/規範)
    - web_patent_search           # 專利搜尋 (Google Patents / Espacenet)
    - web_literature_search       # 論文搜尋
    - cross_domain_translator     # 異業→本業翻譯
    - knowledge_writeback         # Step 8 回寫知識庫 (6 類資產)
  citation_format:
    rag: "KB-{領域}-{序號}"       # e.g., KB-FMEA-042
    web: "WEB-{類型}-{序號}"      # e.g., WEB-PAT-003
```

### 6.3 State Management 對接

```yaml
process_states:
  # 對應 State Machine 的 Process State
  - DRAFT → PHASE_I → PHASE_II → PHASE_III → COMPLETED
  # Step-level
  - IDLE → STEP_1_ACTIVE → STEP_2_ACTIVE → STEP_3_ACTIVE
    → STEP_4_ACTIVE → STEP_5_ACTIVE (含 5-0/5a/5b/5c/5d/5e)
    → STEP_P_ACTIVE → STEP_6_ACTIVE → STEP_6E_ACTIVE (迴圈)
    → STEP_7_ACTIVE → STEP_8_ACTIVE → COMPLETED

artifact_states:
  # 對應 State Machine 的 Artifact State
  - Draft → Reviewed → Verified → Baselined → Released

agent_state:
  - idle → running → waiting_human → completed → error

orchestrator_state:
  current_step: "step_5a"
  current_phase: "PHASE_II"
  parallel_tasks: ["triz_c001", "triz_c002", "scamper_subsys_a"]
  gate_results:
    gate_1: "passed"
    gate_2: "passed"
    gate_3: "passed"
    gate_4: "passed"
    anti_anchor: "passed"
    gate_p: "pending"
  human_pending: []
  artifact_versions:
    constraint: "reviewed"
    contradiction: "verified"
    assumption: "verified"
    concept_route: "draft"
```

---

## §7 驗證方式

### 7.1 E2E 驗證場景：eBike 馬達散熱

1. **輸入**：「eBike 中置馬達在長坡連續高負載下溫度超標，需在 150×80mm 空間內解決」
2. **預期結果**：
   - Step 1：Constraint (Draft) 含三個最不能失敗指標，Gate 1 通過
   - Step 2：索克拉底問答產出 ≥10 假設 + ≥3 矛盾，Assumption Challenge 至少質疑「必須用風冷」
   - Step 3：因果迴路圖含熱-機-振耦合，TRIZ 矛盾句正式化（改善散熱 vs 惡化空間）
   - Step 5-0：3 種非典型架構，≥1 條非對標（如磁力傳動），Anti-Anchor Gate 通過
   - Step 5a：每條矛盾 ≥3 條 TRIZ 工程對映，含 ≥1 條非風冷方案（相變材料、液冷、熱管）
   - Step 5c：SCAMPER 對散熱子系統 × 7 動作變形
   - Step 5e：MUST 快篩後保留 3-5 條，Diversity Score ≥ 0.4
   - Step P：Pre-CAD 審查收斂至 3-5 條
   - Step 8：散熱方案知識回寫至企業知識庫（6 類資產）

### 7.2 檢查清單

- [ ] 每個 Step 名稱與 `RD_Design_Copilot_State_Machine.md` Step 編號對照表完全一致
- [ ] 每個 Gate 的判定邏輯與 `整合流程.md` Gate 檢查點一致
- [ ] Artifact State 轉換與 State Machine §Gate 與 Phase 轉換對照表一致
- [ ] Step 5 內部子步驟（5-0/5a/5b/5c/5d/5e）順序與整合流程 §5.2 流程架構圖一致
- [ ] 並行規則與 State Machine §平行處理說明一致（TRIZ 與 SCAMPER 並行，非 5a+5b+5c 全並行）
- [ ] MUST 規則 (M1-M6) 與 MUST_Rulebook_Template.md 一致
- [ ] Pre-CAD 審查 5 維度與 Pre_CAD_Review_Template.md 一致
- [ ] Knowledge Agent 的 citation 格式（KB-/WEB-）與整合流程 §1.4 知識引用規範一致
- [ ] AutoTRIZ 子步驟（5a-1 至 5a-5）與整合流程 §5a AutoTRIZ 執行模式表一致
- [ ] KT 決策在 Step 7（非 Step 5e），MUST 快篩在 Step 5e（非 Step 7）

---

## 附錄 A：與現有文件的對應關係

| 本文件章節 | 對應的 E2E 文件 | 對應章節 |
|-----------|----------------|---------|
| §1 Agent 定義 | PRD_RD_Design_Copilot.md | §AI 角色邊界表 |
| §2.2 自動化對照表 | RD_Design_Copilot_State_Machine.md | §Step 編號對照 + §R&R |
| §2.3 R&R 對照 | RD_Design_Copilot_State_Machine.md | §各 Step R&R |
| §3 路徑依賴機制 | PRD_RD_Design_Copilot.md | §Pain Points |
| §4.1 序列圖 | RD_Design_Copilot_整合流程.md | §流程總覽 + 各 Step |
| §4.2 並行規則 | RD_Design_Copilot_State_Machine.md | §平行處理說明 |
| §4.3 Gate 判定 | 整合流程.md + State_Machine.md | §Gate 與 Phase 轉換對照 |
| §4.4 Artifact 轉換 | RD_Design_Copilot_State_Machine.md | §Gate 關鍵工件狀態轉換 |
| §5.2 機制對應 | RD_Design_Copilot_整合流程.md | §5.1 Anti-Anchor + §5a TRIZ |
| §6.2 TRIZ KB | triz_knowledge_base/README.md | §注入策略 |
| §6.3 State Management | RD_Design_Copilot_State_Machine.md | §雙層狀態機 |
| §7.2 MUST 驗證 | MUST_Rulebook_Template.md | 全文 |
| §7.2 Pre-CAD 驗證 | Pre_CAD_Review_Template.md | 全文 |
| §7.2 Evidence 驗證 | Evidence_Matrix_Risk_Register_Template.md | 全文 |
