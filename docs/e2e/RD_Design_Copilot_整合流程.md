# RD Design Copilot 整合方法論 (E2E)

**一句話定位**：把「系統性決策流程」的治理骨架與「SCAMPER/TRIZ」的發散引擎深度耦合，形成一套 **「結構化發散 → 嚴格收斂 → 最小驗證」** 的早期設計流程。並透過 **「數位線索 (Digital Thread)」** 連結所有設計工件及其證據，建立 **「可驗證的 Gate (Evidence-driven Gate)」** 以驅動決策。TRIZ 推理採用 **AutoTRIZ 混合架構**（規則骨架 + LLM 生成補足），搭配 **企業知識庫 RAG + 網路文獻搜尋** 作為知識增強層。

---

## 核心哲學

```
混沌 → 結構 → 證據 → 決策 → 資產
      ↑              ↓
   SCAMPER/TRIZ    Robust篩選
   (擴大可能性)    (殺掉脆弱)
```

**三個不變原則**：

1.  **先把未知寫下來**（假設台帳）
2.  **先留多條路**（Set-Based + SCAMPER/TRIZ 變體）
3.  **先切斷連鎖死法**（失效路徑 + 最小實驗）

---

## 0) E2E 流程對齊：PPT 與 Copilot 語言 Mapping

為了確保 RD 團隊能清楚了解每個工程階段與 Copilot 的產出及證據要求，我們將外部（高階）與內部（詳細）的流程語言進行對齊。

**高階流程 (PPT/NPI):**

*   **設計發想 (Design Ideation)** → Copilot Phase 1 & 2
*   **CAD / 模擬驗證 (CAD / Simulation Verification)** → Copilot Phase 2 & 3 (特別是 Evidence Closure)
*   **打樣 / 測試驗證 (Prototyping / Test Verification)** → Copilot Phase 3 (特別是 Evidence Closure)
*   **設計審查 (Design Review)** → Copilot Phase 3 (Step 3.1 & 3.2)
*   **NPI (New Product Introduction)** → Copilot Phase 3 (Decision & Assetization)

---

## 1) 核心概念：雙層狀態機與數位線索 (Digital Thread)

為了實現 E2E 落地，我們需要同時管理「活動步驟」與「工件生命週期」。

### 1.1 雙層狀態機

*   **上層：流程狀態機** (即目前的 Step 1.1~3.3) - 描述團隊活動的推進。
*   **下層：工件狀態機** - 描述每個設計工件 (Artifact) 的生命週期流轉。
    *   **工件狀態流轉範例**：Draft → Reviewed → Verified (with Evidence) → Baseline → Released

### 1.2 數位線索 (Digital Thread)

所有設計工件及其相關數據、版本、證據都將被系統性連結，確保可追溯、可驗證。

### 1.3 核心工件物件 (Copilot Minimal Data Model Schema)

Copilot 最小資料模型將圍繞以下 6 個核心物件，實現專家知識數位化與可複用流程：

1.  **Constraint**：需求、硬限制、軟目標、非目標。
2.  **Contradiction (TRIZ)**：改善參數、惡化參數、工程描述、物理矛盾。
3.  **Breakpoint**：斷路點：介入位置、可操作參數。
4.  **Concept Route**：架構路線：機制、介面契約、預估 BOM、風險、Evidence Matrix。
5.  **Evidence**：仿真報告、計算書、測試報告、供應商回覆、量測數據。
6.  **Risk**：風險登錄 (FMEA-like)，包含失效模式、機率、嚴重度、緩解措施。

### 1.4 知識增強層：企業知識庫 RAG + 網路文獻搜尋

Copilot 在流程各階段透過兩條知識通道，自動注入佐證與補述資料：

```
┌─────────────────────────────────────────────────────────────┐
│                  知識增強層 (Knowledge Augmentation)          │
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────────┐     │
│  │  企業知識庫 (RAG)     │    │  網路文獻搜尋 (Web)      │     │
│  │                      │    │                          │     │
│  │  • 歷史失效案例       │    │  • 學術論文 / 期刊        │     │
│  │  • 過往設計決策       │    │  • 專利檢索              │     │
│  │  • 內部規範 / SOP     │    │  • 產業標準 / 法規        │     │
│  │  • 測試報告           │    │  • 競品分析 / 拆解報告    │     │
│  │  • 供應商評鑑紀錄     │    │  • 材料 / 製程資料庫      │     │
│  │  • FMEA / 8D 報告    │    │  • 技術白皮書             │     │
│  └──────────┬───────────┘    └────────────┬──────────────┘     │
│             │                              │                  │
│             └──────────┬───────────────────┘                  │
│                        ▼                                      │
│            Copilot 各步驟自動檢索與注入                         │
└─────────────────────────────────────────────────────────────┘
```

#### 各步驟知識注入對照表

| Step | 企業知識庫 RAG 用途 | 網路文獻搜尋用途 |
|------|-------------------|----------------|
| **Step 1.1** 問題界定 | 過往類似案例約束、歷史 KPI 數據 | 產業基準 (benchmark)、法規更新 |
| **Step 1.2** 理解全貌 | 歷史假設與驗證結果、內部 know-how | 學術文獻中的失效機制研究 |
| **Step 1.3** 系統建模 | FMEA/8D 歷史失效模式、因果數據 | TRIZ 矛盾矩陣參考文獻、跨領域案例 |
| **Step 2.1** 假設驗證 | 過往驗證方法與成本紀錄 | 最新測試方法論、量測技術 |
| **Step 2.2** 創造調整 | 內部專利庫、過往方案評分紀錄 | 外部專利檢索、新材料/新製程文獻 |
| **Step 2.3** Pre-CAD | 歷史 DFM 評估報告 | 製程能力參考資料 |
| **Step 3.1** 設計審查 | 歷史失效案例比對 (同產品/同模組/同機制) | 材料特性資料庫、仿真參數參考 |
| **Step 3.2** 決策行動 | 過往決策記錄與教訓學習 (Lessons Learned) | 競品/產業趨勢佐證 |
| **Step 3.3** 內化傳達 | 知識庫回寫 (新增 Lessons Learned) | — |

#### 知識引用規範

所有從 RAG 或 Web 檢索注入的資料，必須附帶來源標記以確保可追溯性：

```yaml
知識引用格式:
  RAG來源:
    引用ID: "KB-{領域}-{序號}"     # e.g., KB-FMEA-042, KB-DEC-017
    來源文件: "{文件名稱/編號}"
    相關性: "High / Medium / Low"
    摘要: "{簡述引用內容}"

  Web來源:
    引用ID: "WEB-{類型}-{序號}"    # e.g., WEB-PAT-003, WEB-STD-012
    URL: "{來源網址}"
    類型: "論文 / 專利 / 標準 / 白皮書 / 其他"
    發佈日期: "{yyyy-mm-dd}"
    相關性: "High / Medium / Low"
    摘要: "{簡述引用內容}"
```

### 1.5 AutoTRIZ 混合架構：規則骨架 + LLM 生成補足

> **設計原則**：TRIZ 推理骨架高度規則化（矛盾矩陣、分離原則、76 標準解、ARIZ），但「把人話翻成 TRIZ 結構」與「把抽象原理落地成具體設計」這兩端永遠需要語意理解。Copilot 採用 **AutoTRIZ 混合式架構**：規則引擎管流程，LLM 負責模糊地帶。
>
> 參考：Jiang et al. (2025) AutoTRIZ — Automating engineering innovation with TRIZ and large language models.

```mermaid
flowchart TD
    subgraph LLM_Zone ["LLM 驅動區（語意/模糊）"]
        A["Problem Statement<br>人話 / 需求 / 抱怨"] --> B["Problem Structuring<br>問題結構化"]
        B -->|"LLM + NLP"| D["Candidate Params<br>候選 39 參數 + 矛盾候選"]
    end

    subgraph Rule_Zone ["規則引擎區（確定性）"]
        B -->|"rule + ontology"| C["Function Model<br>功能 / 物質 / 場 / 交互作用"]
        C --> E{"Contradiction Type<br>矛盾分類"}
        D --> E
        E -->|"Technical"| F["Contradiction Matrix<br>查表 → 原理 Top-N"]
        E -->|"Physical"| G["Separation Principles<br>分離原則"]
        E -->|"Su-Field"| H["76 Standards<br>標準解"]
    end

    subgraph Hybrid_Zone ["混合區（規則 + LLM）"]
        F --> I["Instantiation<br>原理具體化"]
        G --> I
        H --> I
        I -->|"LLM + constraints"| J["Solution Concepts<br>方案集"]
        J --> K["Ranking and Evaluation<br>可行性 / 成本 / 風險"]
        K --> L["Structured TRIZ Report<br>可解釋報告"]
        L --> M["Human-in-the-loop<br>人審 / 迭代補問"]
    end
```

#### TRIZ Prompt Markdown 參照表

知識庫以結構化 Markdown 存放，由規則引擎 (`triz_engine.py`) 啟動時解析為 in-memory 資料結構：

```
rd_assistant_design_system/triz_knowledge_base/
├── 01_39_parameters.md          # 39 工程參數 + LLM 語意映射提示
├── 02_contradiction_matrix.md   # 39×39 矛盾矩陣 (row-based lookup)
├── 03_40_principles.md          # 40 發明原理 + 子原理 + 工程提示
├── 04_separation_principles.md  # 物理矛盾 4 大分離原則
└── 05_76_standard_solutions.md  # Su-Field 76 標準解 (5 大類)
```

Prompt 模板（由 `triz_solve_service.py` 調用，注入 KB 內容後送 LLM）：

```
src/prompts/
├── triz_classify.md             # 矛盾類型分類 (TC/PC/SF) — 無 KB 注入
├── triz_param_mapping.md        # 自然語言 → 39 參數 ID — 注入 39 params 全量表格
├── triz_tc_solve.md             # 技術矛盾具體化 — 注入矩陣查表結果 + 選中原理詳情
├── triz_pc_solve.md             # 物理矛盾分離策略 — 注入 4 大分離原則全量
└── triz_sf_solve.md             # Su-Field 標準解具體化 — 注入匹配的標準解清單
```

> **注入策略**：39 參數表格 + 分離原則 → 全量注入（~6,500 token）；矩陣查表結果 + 原理詳情 → 按需注入（僅推薦的原理）；76 標準解 → 按 Su-Field 狀態匹配後注入相關子集。

#### 模組分工：規則 vs LLM（已實作）

| 模組 | 執行方式 | 實作位置 | 說明 |
|------|---------|---------|------|
| **矛盾類型分類** (TC/PC/SF) | **LLM** | `triz_classify.md` | 從工程描述判斷矛盾類型，語意理解不可規則化 |
| **39 參數映射** (自然語言→參數 ID) | **LLM + KB** | `triz_param_mapping.md` | 注入 39 參數全量表格，LLM 做語意消歧 |
| **矛盾矩陣查表 → 原理推薦** | 規則引擎 | `triz_engine.lookup_matrix()` | 39×39 矩陣確定性查表，零 LLM 成本 |
| **原理詳情檢索** | 規則引擎 | `triz_engine.get_principles()` | 從 40 原理 KB 中取出子原理 + 工程提示 |
| **分離原則 KB 注入** | 規則引擎 | `triz_engine.format_separations_for_prompt()` | 4 大分離原則全量格式化 |
| **76 標準解匹配** | 規則引擎 | `triz_engine.get_standards_for_state()` | Su-Field 狀態 → 對應類別的標準解 |
| **技術矛盾具體化** (抽象→工程設計) | **LLM + KB** | `triz_tc_solve.md` | 注入矩陣結果 + 原理詳情，LLM 落地為工程手段 |
| **物理矛盾分離策略** | **LLM + KB** | `triz_pc_solve.md` | 注入分離原則全量，LLM 選擇策略並具體化 |
| **Su-Field 標準解具體化** | **LLM + KB** | `triz_sf_solve.md` | 注入匹配的標準解，LLM 翻譯為工程方案 |
| **報告結構模板** | 規則引擎 | Pydantic schemas | 固定章節與欄位（`UnifiedTrizResult`） |

> **LLM calls per solve**：最多 4 次（分類 1 + 參數映射 1 + TC/PC/SF 具體化 1-2）。矩陣查表和原理/標準解檢索為零成本規則引擎。

#### Copilot 流程對映

| AutoTRIZ 階段 | 對應 Copilot Step | 主要執行方式 | API 端點 |
|--------------|-------------------|-------------|---------|
| Problem Structuring | **Step 1.1-1.2** (問題界定 + 理解全貌) | LLM 抽取 + 人校準 | `POST /contradictions/identify` |
| Function Model + 矛盾定義 | **Step 1.3** (系統建模 + TRIZ 矛盾正式化) | LLM 輔助翻譯 + 規則驗證 | — |
| 統一求解 (分類→路由→具體化) | **Step 2.2.2** (TRIZ 解矛盾) | **規則引擎查表 + LLM 具體化** | `POST /triz/solve` |
| Instantiation + Solution | **Step 2.2.3-2.2.5** (子系統 + SCAMPER + 方案生成) | LLM 生成 + RAG 佐證 | — |
| Ranking & Evaluation | **Step 2.2.6 / Step 3.2** (MUST 快篩 / KT 決策) | 規則引擎 + 人審 | — |

---

## Gate 與 Phase 轉換 (更新)

系統有 8 個 Step-level Gate（每步一個），其中 4 個同時觸發 Phase 轉換：

| Gate | 位置 | Gate 類型 | Phase 轉換 |
|------|------|-----------|-----------|
| Gate 1.1 | Step 1.1 完成 | 內部 Gate | **DRAFT → PHASE_1** |
| Gate 1.2 | Step 1.2 完成 | 內部 Gate | Phase 1 內部 |
| Phase Gate 1 (= Gate 1.3) | Step 1.3 完成 | 內部 Gate | **PHASE_1 → PHASE_2** |
| Gate 2.1 | Step 2.1 完成 | 內部 Gate | Phase 2 內部 |
| **Gate 2.2** | Step 2.2 完成 | **Pre-CAD Gate** | Phase 2 內部 (產出 MVP CAD 候選集) |
| **Phase Gate 2 (= Gate 2.3)** | Step 3.1 完成 | **CAD Gate** | **PHASE_2 → PHASE_3** (設計凍結或進入詳細設計) |
| Gate 3.2 | Step 3.2 完成 | 內部 Gate | Phase 3 內部 |
| Phase Gate 3 (= Gate 3.3) | Step 3.3 完成 | 內部 Gate | **PHASE_3 → COMPLETED** |

---

## 流程總覽 (8 步驟 × 六帽 × SCAMPER/TRIZ)

> **v1.3 更新**：引入 Pre-CAD Gate (Gate 2.2) 與 CAD Gate (Phase Gate 2)，將設計審查分層。

```mermaid
graph TD
    subgraph Phase1 ["Phase 1: Define (定義問題空間) (Week 1-2)"]
        S1["Step 1.1: 問題界定<br>(白帽)<br>(工件: Constraint)"] --> S2["Step 1.2: 理解全貌<br>(索克拉底)<br>(工件: Contradiction)"]
        S2 --> S3["Step 1.3: 系統建模<br>(藍帽)<br>(工件: Contradiction, Breakpoint)"]
    end

    subgraph Phase2 ["Phase 2: Diverge (假設與發散) (Week 2-4)"]
        S4["Step 2.1: 假設驗證<br>(HDA)<br>+未知集合<br>(工件: Assumption Ledger)"]
        S5_Main["Step 2.2: 創造與調整 (綠帽/紅帽)<br>(工件: Concept Route, Interface)"]
        S_P["Step 2.3: Pre-CAD 審查 (縮減候選集)<br>(工件: Pre-CAD Review Report)"]

        S4 --> S5_Main
        S5_Main --> SP_Gate["Pre-CAD Gate (Gate 2.2)"]
        SP_Gate --> S_P
    end

    subgraph Phase3 ["Phase 3: Converge (收斂與驗證) (Week 4-8)"]
        S6["Step 3.1: 設計審查<br>(MVP CAD Review)<br>(工件: Evidence Matrix, Risk)"]
        S6e["Step 3.1.loop: 證據補齊<br>(最小實驗/仿真)<br>(工件: Evidence)"]
        S7["Step 3.2: 決策行動<br>(KT Decision)<br>(工件: Decision Record)"]
        S8["Step 3.3: 內化傳達<br>(費曼)<br>(工件: Asset)"]

        S_P --> C_Gate["CAD Gate (Phase Gate 2)"]
        C_Gate --> S6
        S6 --> S6e
        S6e --> S6
        S6 --> S7
        S7 --> S8
    end

    S3 --> S4
    S8 --> End([完成])

    subgraph KnowledgeLayer ["知識增強層"]
        RAG[("企業知識庫<br>(RAG)")]
        WEB[("網路文獻搜尋<br>(Web)")]
    end

    RAG -.->|"歷史案例/規範"| S1
    RAG -.->|"FMEA/8D"| S3
    RAG -.->|"內部專利/方案"| S5_Main
    RAG -.->|"失效案例比對"| S6
    WEB -.->|"產業基準/法規"| S1
    WEB -.->|"TRIZ文獻/跨領域"| S3
    WEB -.->|"專利/新材料"| S5_Main
    WEB -.->|"材料特性/仿真參數"| S6
    S8 -.->|"Lessons Learned 回寫"| RAG
```

---

# Phase 1: Define (定義問題空間)

## Step 1.1: 問題界定 (白帽 + 5W1H)

### 1.1.1 目的
把模糊需求變成「可檢查句」，為後續 TRIZ 矛盾定義打基礎。
**核心工件**：Constraint (Draft)

### 1.1.2 輸入
- 客戶/PM 需求描述
- 過往類似案例（如有）
- 空間/成本/製程約束
- **[RAG]** 企業知識庫中過往類似專案的約束定義、歷史 KPI 達成數據
- **[Web]** 產業基準 (benchmark) 數據、最新法規與標準要求

### 1.1.3 AI 協助任務

```yaml
任務清單:
  - 將需求改寫成約束句
  - 生成缺口問卷
  - 列出已知事實 vs 未知缺口
```

### 1.1.4 輸出模板

**任務定義表 v1.1 (工件: Constraint)**

| 欄位 | 內容 | 證據來源 (Artifact ID) |
|------|------|--------------------|
| **Mission** | 在【使用情境】下，系統必須【達成行為】，且【三個最不能失敗的指標】不得超標 | PRD-001 |
| **Hard Constraints** | 絕對不能違反的限制（空間、法規、成本上限） | REG-001, COST-001 |
| **Soft Objectives** | 可 trade-off 的目標（效率、重量、噪音） | MRD-002 |
| **Non-Goals** | 這版明確不追求的東西 | STRATEGY-003 |
| **三個最不能失敗指標** | 1. [指標名稱] (判斷方式: [方法]) 2. [指標名稱] (...) 3. [指標名稱] (...) | KPI-001 |

**Gate 1.1 檢查點**
> ✅ 「三個最不能失敗指標」被明確說出，且每個指標有「可量測」或「可判斷」的方式。
> ✅ 核心工件 Constraint 狀態: Draft -> Reviewed。

---

## Step 1.2: 理解全貌 (索克拉底問答)

### 1.2.1 目的
把「大家以為理所當然」的前提翻出來，為 TRIZ 矛盾識別做準備。
**核心工件**：Contradiction (Draft), Assumption (Draft)

### 1.2.2 知識增強輸入
- **[RAG]** 歷史假設台帳中「被推翻的假設」清單，避免重複犯錯
- **[RAG]** 類似產品的內部 know-how 文件、設計規範
- **[Web]** 學術文獻中的失效機制研究、產業趨勢報告

### 1.2.3 索克拉底六類提問 (AI 固定執行)

| 類型 | 問題範例 |
|------|---------|
| **澄清** | 你說的「小空間」是體積還是外形約束？ |
| **假設** | 你假設熱可以靠外殼散掉，證據是什麼？ |
| **證據** | 過去類似產品在相同功率下的溫升記錄？ |
| **觀點** | 若把控制器外置，誰會反對？原因？ |
| **後果** | 若 NVH 超標，最壞代價是什麼？ |
| **反思** | 我們現在最可能「自欺欺人」的是哪一條？ |

### 1.2.4 輸出：矛盾初步識別 (工件: Contradiction)

**矛盾列表 v1.1** (為 Step 1.3 TRIZ 準備)

| 編號 | 我想改善 | 但會惡化 | 來源 (假設/情境/數據) |
|------|---------|---------|--------------------|
| C1 | 體積更小 | 散熱能力 | A001 |
| C2 | 轉速更高 | NVH | R002 (風險) |
| C3 | 成本更低 | 可靠性 | Constraint-001 |

**Gate 1.2 檢查點**
> ✅ 至少列出 10 條關鍵假設，標出 Top 3「錯了就翻車」的假設。
> ✅ 至少識別 3 條核心矛盾。
> ✅ 核心工件 Contradiction, Assumption 狀態: Draft -> Reviewed。

---

## Step 1.3: 系統建模 (因果迴路 + TRIZ 矛盾定義)

### 1.3.1 目的
找到耦合點（未知會放大的地方），並將矛盾正式化為 TRIZ 句式。
**核心工件**：Contradiction (Verified), Breakpoint (Draft)

### 1.3.2 知識增強輸入
- **[RAG]** FMEA/8D 歷史報告中的失效因果鏈，直接匯入因果迴路圖
- **[RAG]** 過往專案的耦合點分析結果
- **[Web]** TRIZ 矛盾矩陣參考文獻、跨領域類比案例 (e.g., 汽車/航太的類似耦合問題)

### 1.3.3 因果迴路圖建立

```mermaid
flowchart LR
    subgraph CausalLoop ["熱-機-振 耦合迴路"]
        P[功率/負載] --> H[發熱增加]
        H --> T[溫度上升]
        T --> R[效率下降]
        R --> P
        T --> D[零件變形]
        D --> N[NVH上升]
        N --> E[客訴壓力]
        E --> C[設計更改]
        C --> K[複雜度上升]
        K --> D
    end
```

### 1.3.4 TRIZ 矛盾正式化 (工件: Contradiction)

> **AutoTRIZ 標註**：此步驟是 TRIZ 流程中「最難規則化」的環節——把口語化的工程問題翻譯成 TRIZ 結構（39 參數、矛盾類型、物理矛盾）。Copilot 使用 **LLM 輔助翻譯 + 規則驗證** 的混合模式：
> - **LLM 負責**：從 Step 1.1-1.2 的自然語言描述中抽取候選改善/惡化參數、判斷矛盾類型
> - **規則引擎負責**：驗證參數是否為合法的 39 參數、矛盾句式是否完整、是否有重複/遺漏
> - **人校準**：RD 確認 LLM 產出的矛盾句是否反映真正的工程矛盾

**TRIZ 矛盾句模板**

```
矛盾 [編號]:
  改善參數: [TRIZ 39參數之一]
  惡化參數: [TRIZ 39參數之一]
  工程表述: 當 [動作] 時，[指標A] 改善，但 [指標B] 惡化
  物理矛盾: [同一物件] 需要同時具備 [屬性X] 和 [非屬性X]
```

**範例**

```yaml
矛盾 C1:
  改善參數: 9-速度
  惡化參數: 31-有害副作用(噪音)
  工程表述: 當轉速提高時，輸出功率密度改善，但 NVH 惡化
  物理矛盾: 轉子需要同時「高轉速」和「低振動」
```

### 1.3.5 輸出：斷路點識別 (工件: Breakpoint)

| 斷路點編號 | 位置 | 可能解法方向 | TRIZ 原理提示 |
|--------|------|-------------|--------------|
| BP001 | 馬達-減速機界面 | 隔熱隔振分區 | #1分割, #2分離 |
| BP002 | 控制器 | 雙路徑散熱 | #40複合材料 |
| BP003 | 裝配界面 | 浮動支撐 | #15動態化 |

**Phase Gate 1 (= Gate 1.3) 檢查點**
> ✅ 明確點名 3 個斷路點，每個斷路點有對應 TRIZ 原理提示。
> ✅ 每條核心矛盾都有 TRIZ 正式句。
> ✅ 核心工件 Contradiction 狀態: Reviewed -> Verified。
> ✅ 核心工件 Breakpoint 狀態: Draft -> Reviewed。

---

# Phase 2: Diverge (假設與發散)

## Step 2.1: 假設與驗證規劃 (HDA)

### 2.1.1 假設台帳 (Assumption Ledger) (工件: Assumption)

**必填 6 欄**

| 假設編號 | 假設內容 | 依據來源 (Artifact ID) | 若錯了最壞後果 | 最小驗證方法 | 驗證成本/週期 |
|---------|---------|--------------------|--------------|-------------|--------------|
| A001 | 外殼可帶走 80% 熱量 | Data-HT001 (歷史數據) | 溫升超標 30°C | 熱阻測試 | 1週/$500 |
| A002 | 裝配偏心 < 0.1mm | Spec-SUP002 (供應商規格) | 共振提前 | CMM 抽檢 | 3天/$200 |
| A003 | 阻尼器壽命 > 5000hr | Report-LT001 (類似產品報告) | 早期失效 | 加速壽命 | 2週/$1000 |

### 2.1.2 未知集合 (U) 表達

```yaml
未知因子:
  u1_負載變化: [低, 中, 高]
  u2_環境溫度: [常溫, 高溫]
  u3_裝配偏心: [小, 中, 大]
  u4_摩擦係數: [低, 高]
  u5_供應公差: [穩定, 不穩定]
```

**Gate 2.1 檢查點**
> ✅ Top 3 假設每個都有「可在 1-2 週內完成」的驗證設計，包含明確的最小驗證方法、成本與週期。
> ✅ 核心工件 Assumption 狀態: Reviewed -> Verified。

---

## Step 2.2: 創造與調整 (TRIZ → 子系統 → SCAMPER → 方案 → MUST)

> **這是整合流程的核心步驟**：用 TRIZ 解矛盾找方向，用 SCAMPER 做模組級變形，輸出結構化可審查的方案集合。此階段結束後，產出的候選方案將進入 **Pre-CAD Gate (Step 2.3)** 進行首次收斂。
> **核心工件**：Concept Route (Draft), Interface (Draft)

### 2.2.0 知識增強輸入
- **[RAG]** 內部專利庫、過往方案的 SCAMPER 變形紀錄與評分結果
- **[RAG]** 歷史 Concept Route 的成功/失敗原因分析
- **[Web]** 外部專利檢索 (e.g., Google Patents, Espacenet)，識別可用的解法方向
- **[Web]** 新材料/新製程文獻、學術期刊中的創新機構設計

### 2.2.1 Anti-Anchor Sprint (反路徑依賴機制)

**目的**：刻意打破資深 RD 的路徑依賴和對標思維，主動探索非典型架構。

*   **產出 3 種「非典型架構」概念**：
    1.  不同能量傳遞/減速概念 (e.g., 非齒輪傳動, 磁力傳動)
    2.  不同感測/控制閉環概念 (e.g., 無感測器控制, 基於視覺的動態調整)
    3.  不同模組拆分/維修策略概念 (e.g., 模組化快拆, 耗材一體化設計)
*   **規則**：**至少 1 條必須是「跟競品在物理介面或核心機制上不相容」的路線**。

**Gate 2.2.1 檢查點 (Step 2.2.1 → Step 2.2.2)**
> ✅ 三條概念路線中，至少有一條是「非對標」且初步判斷能通過 MUST 的 **M1 (空間約束)** 和 **M4 (解耦程度)**。

### 2.2.2 流程架構 (更新)

```mermaid
graph TD
    subgraph Step2_2 ["Step 2.2: 創造與調整 (更新)"]
        InputC["矛盾句 (C-001~N)"] --> S2_2_1["2.2.1: Anti-Anchor Sprint<br>產出 3 種非典型架構 (至少 1 種非對標)"]
        InputBP["斷路點 (BP-001~N)"] --> S2_2_1
        S2_2_1 --> AntiAnchorGate{"經 Gate 2.2.1 篩選"}
        AntiAnchorGate --> S2_2_2["2.2.2: TRIZ 解矛盾<br>輸入: 矛盾句<br>輸出: 原理+策略+工程對映"]

        S2_2_2 --"解法方向<br>(工程對映指出受影響子系統)"--> S2_2_3["2.2.3: 子系統定義<br>(散熱/支撐/傳動/控制器/隔振)"]
        S2_2_3 --"每個子系統"--> S2_2_4["2.2.4: SCAMPER 模組變形<br>對每個子系統 × 7 動作<br>輸出: 七欄規格"]

        S2_2_2 --> S2_2_5["2.2.5: AI 方案生成<br>整合 TRIZ + SCAMPER<br>附帶: 機制+假設+風險+robust+最小驗證+Interface Contract"]
        S2_2_4 --> S2_2_5

        S2_2_5 --> S2_2_6["2.2.6: MUST 快篩<br>Go/No-Go 淘汰 (可機器執行規則)<br>留下 3-5 條架構級路線"]
    end
```

### 2.2.2 TRIZ 解矛盾 (每條矛盾執行)

> **AutoTRIZ 統一求解**：此步驟透過 `POST /triz/solve` 端點，對每條矛盾執行「分類 → 三路徑路由 → 具體化」的統一求解流程。一次 API 呼叫完成所有路徑，回傳 `UnifiedTrizResult`。
>
> ```
> POST /triz/solve { contradiction_id }
>         │
>   ┌─────┴─────┐
>   │ 1. 分類矛盾 │ ← LLM (triz_classify.md)
>   │ TC? PC? SF? │   一條矛盾可同時屬於多種類型
>   └─────┬─────┘
>         │
>   ┌─────┼──────────────────┬──────────────────┐
>   ▼     ▼                  ▼                  ▼
> Path A: TC              Path B: PC          Path C: SF
>   │                       │                   │
>   ├ 參數映射 (LLM+KB)     ├ 注入 4 分離原則    ├ 狀態分類→標準解匹配
>   ├ 矩陣查表 (規則引擎)   │   (規則引擎 KB)    │   (規則引擎)
>   ├ 原理詳情 (規則引擎)   ├ LLM 策略選擇       ├ LLM 具體化
>   ├ LLM 具體化            │   (triz_pc_solve)  │   (triz_sf_solve)
>   │   (triz_tc_solve)     │                   │
>   └───────┬───────────────┴───────────────────┘
>           ▼
>   UnifiedTrizResult {
>     classification, param_mapping, matrix_lookup,
>     technical_solutions[], separation_solutions[], sufield_solutions[]
>   }
> ```
>
> | 子步驟 | 執行方式 | 動作 | 實作位置 |
> |--------|---------|------|---------|
> | 2.2.2-0 矛盾類型分類 | **LLM** | 判定 TC/PC/SF（可複選） | `triz_classify.md` |
> | 2.2.2-A1 參數映射 | **LLM + KB** | 自然語言 → 39 參數 ID | `triz_param_mapping.md` |
> | 2.2.2-A2 矩陣查表 | **規則引擎** | improve × worsen → 推薦原理 IDs | `triz_engine.lookup_matrix()` |
> | 2.2.2-A3 原理詳情 | **規則引擎** | 取出推薦原理的子原理 + 工程提示 | `triz_engine.get_principles()` |
> | 2.2.2-A4 TC 具體化 | **LLM + KB** | 注入矩陣結果 + 原理詳情 → 工程手段 | `triz_tc_solve.md` |
> | 2.2.2-B1 PC 分離策略 | **LLM + KB** | 注入 4 大分離原則全量 → 策略選擇 | `triz_pc_solve.md` |
> | 2.2.2-C1 SF 標準解匹配 | **規則引擎** | Su-Field 狀態 → 對應類別標準解 | `triz_engine.get_standards_for_state()` |
> | 2.2.2-C2 SF 具體化 | **LLM + KB** | 注入匹配的標準解 → 工程方案 | `triz_sf_solve.md` |
> | 2.2.2-5 品質校驗 | **規則 + 人審** | 檢查工程對映是否違反已知約束 | UI 三 Tab 佈局人審 |

**TRIZ 統一輸出規格 (`UnifiedTrizResult`) (工件: Concept Route 的一部分)**

```yaml
UnifiedTrizResult:
  contradiction_id: [矛盾 ID]
  classification:
    types: [technical, physical, sufield]  # LLM 分類結果（可複選）
    sufield_state: [incomplete / harmful / insufficient / ...]  # 若為 SF
    reasoning: [分類推理說明]

  # Path A: 技術矛盾
  param_mapping:
    improve_params: [{triz_id: 14, triz_name: "Strength", confidence: "high"}, ...]
    worsen_params: [{triz_id: 1, triz_name: "Weight", confidence: "high"}, ...]
  matrix_lookup: [1, 8, 15, 34]  # 矩陣推薦的原理 IDs
  technical_solutions:
    - principle_number: 1
      principle_name: "Segmentation"
      abstract_strategy: [原理的抽象描述]
      engineering_mappings: [具體機構/材料/佈局]
      cost_description: [代價]
      robust_estimate: {noise_sensitivity: low}
      experiment_desc: [驗證方式]

  # Path B: 物理矛盾
  separation_solutions:
    - separation_type: "space"
      separation_name: "Separation in Space"
      strategy: [分離策略]
      engineering_mappings: [具體手段]
      cost_description: [代價]
      experiment_desc: [驗證方式]

  # Path C: Su-Field
  sufield_solutions:
    - standard_code: "1.1.1"
      standard_name: [標準解名稱]
      sufield_model: [Su-Field 模型描述]
      engineering_mappings: [具體手段]
      cost_description: [代價]
      experiment_desc: [驗證方式]
```

### 2.2.3/2.2.4 子系統定義 + SCAMPER 模組級變形

**對每個子系統執行 SCAMPER**

子系統清單（依專案調整）：
- 散熱系統
- 支撐結構
- 傳動機構
- 控制器
- 隔振系統

**SCAMPER 輸出規格 (固定 7 欄) (工件: Concept Route 的一部分)**

| 欄位 | 說明 |
|------|------|
| **1. 變形動作** | S/C/A/M/P/E/R |
| **2. 變形對象** | 哪個模組/界面/參數 |
| **3. 物理機制** | 為什麼可改善某指標（工程語言） |
| **4. 新增失效模式** | 會怎麼死 |
| **5. 製程/供應風險** | 是否可量產 |
| **6. 假設台帳** | 需要哪些前提成立 |
| **7. 最小驗證** | 用什麼測試打掉不確定 |

### 2.2.5 AI 方案生成規格 (工件: Concept Route, Interface)

**每個方案必須附帶**

```yaml
方案_[編號]:
  名稱: [簡短描述]
  來源: [TRIZ原理#X + SCAMPER動作Y]

  機制說明:
    物理原理: [為什麼有效]
    結構描述: [用工程語言，不要形容詞]
    關鍵尺寸: [如有]

  **Interface Contract (介面契約):**
    幾何包絡 (Envelope): [CAD Model ID / Description]
    主要載荷/扭矩路徑 (Load path): [Description / Diagram ID]
    感測/控制訊號 (Signal path): [Description / Protocol]
    熱路徑 (Thermal path): [Description / Diagram ID]
    製造裝配基準 (Datum / tolerance intent): [Description]
    服務維修拆解路徑 (Serviceability path): [Description]

  假設清單:
    - A_xx: [前提假設1] (Artifact ID)
    - A_yy: [前提假設2] (Artifact ID)

  風險評估:
    新增失效模式: [會怎麼死] (Link to Risk-001)
    製程風險: [量產可行性]
    供應風險: [材料/零件可得性]

  robust預評分:
    Margin: [1-5]
    Decoupling: [1-5]
    Recoverability: [1-5]
    Complexity: [1-5] (越低越好)
    Sensitivity: [1-5] (越低越好)

  最小驗證:
    驗證目標: [打掉哪個假設]
    方法: [測試/計算/樣品]
    週期: [預估]
    成本: [預估]
```

### 2.2.6 MUST 快篩 (黑帽篩選) (可機器執行規則)

> **注意**：此階段使用 KT MUST 條件做「快速淘汰」，完整的 WANT 評分在 Step 3.2 執行。

**MUST Rulebook (可機器執行)**：每條 MUST 規則都將包含 Input 欄位、判定公式、證據類型和 Fail 處置。詳見附錄 A.1。

**快篩 MUST 條件清單** (詳情參考 `附錄 A.1: MUST Rulebook 模板`)

| MUST | 條件 | 判斷方式 | 證據類型 |
|------|------|---------|---------|
| M1 | 空間約束：可塞進目標空間 | 3D 模型干涉檢查 | CAD Model |
| M2 | 成本預估：BOM ≤ 目標上限 | BOM 粗估計算 | Spreadsheet (BOM-001) |
| M3 | 安全餘裕：三指標有合理 margin | 工程判斷/粗估 | Calculation / Expert Judgement |
| M4 | 解耦程度：無致命耦合迴路 | 因果迴路圖分析 | Diagram (CLD-001) |
| M5 | 可行性：製程/供應基本可行 | 經驗判斷/供應鏈初步確認 | SC-Response-001 |
| **M6** | **製造路徑可行性** | 關鍵製程初步評估 | DFM-001 (初步) |

**快篩表 (工件: Concept Route 的一部分)**

| 方案 | M1 | M2 | M3 | M4 | M5 | M6 | 結果 | 證據 (Artifact ID) |
|------|----|----|----|----|----|----|----|--------------------|
| A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | → Step 3.1 | CAD-A001, BOM-A001 |
| B | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | **淘汰** | BOM-B001 |

**篩選規則**
1.  任一 MUST 不通過 = 直接淘汰。
2.  通過者進入 Set-Based 集合（建議 3-5 條，包含至少 1 條 Anti-Anchor 路線）。
3.  完整 KT Decision Analysis（MUST+WANT+AC）在 Step 3.2 執行。

**Gate 2.2 檢查點 (進入 Pre-CAD Gate)**
> ✅ 至少保留 3 條「架構級」路線，其中包含至少 1 條 Anti-Anchor 路線。
> ✅ 每條路線都有完整的方案規格 (機制、假設、風險、最小驗證)。
> ✅ 每條路線都產出初步的 **Interface Contract**。
> ✅ 每條路線的 **MUST Rule** 都經過判斷，並提供對應的初步證據 (哪怕是 E1/E2 等級)。
> ✅ 核心工件 Concept Route 狀態: Draft -> Reviewed。

---

## Step 2.3: Pre-CAD 設計審查 (Pre-CAD Gate)

> **目的**：在投入大量 CAD 繪製和詳細模擬之前，利用「可驗證的最小資訊」篩選和縮減候選設計方案，將發想階段的 20+ 個點子收斂到 3–5 條最優架構路線，避免資源浪費。
> **核心工件**：Concept Route (Verified), Pre-CAD Review Report (Draft)

### 2.3.1 Pre-CAD 審查內容 (不需要 CAD 的審查)

審查主要基於每條 Concept Route 提供的：
*   **方案規格** (機制、假設、風險、最小驗證)
*   **Interface Contract (介面契約草案)**
*   **MUST 快篩結果** (Step 2.2.6)

### 2.3.2 Pre-CAD 審查表 (工件: Pre-CAD Review Report)

詳情參考 `附錄 A.4: Pre-CAD Review Report 模板`。此模板將引導團隊從以下維度進行審查：

1.  **MUST (硬限制)**：確認方案在空間、重量、成本、供應、法規等硬性約束下的可行性。
2.  **解耦程度 (Decoupling)**：方案是否有效降低了系統耦合點，提升了模組獨立性。
3.  **可驗證性 (Testability)**：方案的核心假設能否透過 1-2 週的最小實驗快速驗證。
4.  **主要風險機制 (Failure Mechanism)**：識別方案最可能導致失效的物理機制 (e.g., 污染、磨耗、共振、熱衰退)。
5.  **最小 CAD 工作量 (MVP CAD Effort)**：評估為進行第一輪粗仿真/干涉檢查，需要繪製哪些最少的幾何模型。

### 2.3.3 Pre-CAD Gate 輸出

*   保留 3–5 條「架構級差異顯著」的 Concept Route。
*   每條保留路線都需更新其「介面契約草案」並提供「最小驗證計畫」。

**Gate 2.2 檢查點**
> ✅ 經 Pre-CAD 審查，候選 Concept Route 已收斂至 3–5 條。
> ✅ 每條保留路線的 Interface Contract 已更新。
> ✅ 每條保留路線都明確了下一步進行 MVP CAD 的最小幾何範圍。
> ✅ 核心工件 Concept Route 狀態: Reviewed -> Verified (通過 Pre-CAD Gate)。
> ✅ 核心工件 Pre-CAD Review Report 狀態: Draft -> Reviewed。

---

# Phase 3: Converge (收斂與驗證)

## Step 3.1: 設計審查 (CAD Gate - MVP CAD Review)

> **核心思想**：針對通過 Gate 2.2 的候選方案，進行 MVP CAD 的初步審查，利用有限的 CAD/模擬成果快速識別潛在的設計缺陷、製造困難或整合問題，並將「證據缺口」轉化為下一步的最小實驗。此階段即為 **CAD Gate (Phase Gate 2)**。
> **核心工件**：Concept Route (Verified), Evidence Matrix (Draft), Risk (Reviewed), MVP CAD Model (Draft)

### 3.1.1 Design Review Evidence Matrix (DR EM) (工件: Evidence Matrix)

每條方案路線 (3~5 條) 都將對應一張矩陣，其為 Step 3.1 的主要產出。詳情參考 `附錄 A.2: Evidence Matrix 模板`。

| 類別 | 要求/規格 | 目前證據 (Artifact ID) | 證據品質 (E0-E4) | 證據缺口 (Gap Description) | 下一步最小實驗 (Artifact ID) | Owner | Due |
| -- | ----- | ---- | ---- | -- | ------- | ----- | --- |
| KPI001 | 騎乘體驗: 起步扭矩建立時間 ≤ 200ms | Sim-Torque001 | E1 | 實際馬達響應未驗證 | Exp-Motor001 (台架測試) | 張三 | 2026/03/15 |
| NVH002 | 低速爬坡噪音 ≤ 60dB | - | E0 | 無任何數據 | Exp-NVH001 (樣品測量) | 李四 | 2026/03/20 |
| DFM003 | 關鍵件裝配時間 ≤ 5min | DFM-Review001 | E1 | 組裝工藝未實際驗證 | Exp-ASM001 (手工組裝測試) | 王五 | 2026/03/22 |

**證據品質定義 (E0-E4):**

*   **E0: 只有推論** (Only inference)
*   **E1: 有計算/估算** (Calculation/Estimation available)
*   **E2: 有仿真或 Bench Test** (Simulation or Bench Test available)
*   **E3: 有實測 (接近真實情境)** (Field Test/Near-real-world measurement)
*   **E4: 量產條件下證據** (Evidence under Mass Production conditions)

### 3.1.2 知識增強輸入
- **[RAG]** 歷史失效案例庫 (FMEA、8D、Warranty Claim)，自動比對當前方案的失效風險
- **[RAG]** 過往 Evidence Matrix 填寫紀錄，加速證據分類與缺口識別
- **[Web]** 材料特性資料庫 (e.g., MatWeb, CES EduPack 公開數據)、仿真參數參考文獻
- **[Web]** 產業標準中的測試方法與合格基準 (e.g., ISO, IEC, SAE)

### 3.1.3 歷史失效案例比對 (Failure Mode Transfer)

Copilot 的比對策略將分為三層，確保從歷史失效案例中獲取最大洞察：

1.  **同產品/同平台**：直接相關的失效。
2.  **同模組 (齒輪/軸承/油封/感測器)**：模組層級的失效模式。
3.  **同機制 (磨耗、污染、疲勞、共振、熱衰退、黏滑)**：物理失效機制層級的失效，能提供跨領域的創新洞察。

輸出結果將直接與「風險登錄表 (Risk Register)」連結。

### 3.1.4 生產技術配對 (DFM/DFA Early Assessment)

*   **M6 (製造路徑可行性)** 已在 Step 2.2 的 MUST Rulebook 中進行初步篩選。
*   在 Step 3.1，將進行更細緻的 DFM/DFA 評估，例如：Process Window, Cycle Time, 良率風險。

### 3.1.5 公式驗證升級為 Model Card / Assumption Card

針對關鍵模型 (公式/仿真)，產出以下「卡片」以管理其假設與風險：

*   **Model Card**: 適用範圍 (validity range)、關鍵假設 (assumptions)、敏感度 (sensitivity)、驗證方式 (validation plan)、失效模式 (model risk)。
*   **Assumption Card**: (與 Assumption Ledger 連結)

**Phase Gate 2 (= Gate 2.3) 檢查點 (進入 Phase 3)**
> ✅ 每條方案路線都具備一份經過初步填寫的 **Evidence Matrix** (DR EM) 並隨附 MVP CAD 模型。
> ✅ **北極星指標** (定義於 Step 1.1) 的目前證據等級 **≥ E2** (仿真或 Bench Test)。
> ✅ **Top 10 風險** (定義於 Step 3.1.6) 都對應到「證據缺口」與「下一步最小實驗」，並指定 Owner 和 Due Date。
> ✅ 核心工件 Concept Route 狀態: Reviewed -> Verified (通過 CAD Gate)。
> ✅ 核心工件 Evidence Matrix 狀態: Draft -> Reviewed。
> ✅ 核心工件 Risk 狀態: Draft -> Reviewed。
> ✅ 核心工件 MVP CAD Model 狀態: Draft -> Reviewed。

---

## Step 3.1.loop: 證據補齊 (Evidence Closure)

**目的**：針對 Step 3.1 審查中發現的證據缺口，執行快速的最小實驗、仿真或供應商確認，以將證據等級提升至 Gate 3.2 的要求。這是一個獨立的迴圈，允許設計團隊在不影響主流程推進的情況下，專注於補足關鍵證據。

*   **觸發條件**：在 Step 3.1 審查中發現證據缺口，且該缺口屬於「可透過最小實驗在 1-2 週內補足」。
*   **活動**：執行最小實驗、快速仿真、供應商數據收集、文獻回顧等。
*   **輸出**：新的 Evidence (Verified) 工件，更新至 Evidence Matrix。
*   **迴圈**：完成 Step 3.1.loop 後，返回 Step 3.1 重新審查 Evidence Matrix。

---

## Step 3.2: 決策與行動 (KT Decision Analysis + 最小實驗)

> **重要更新**：本步驟整合 Kepner-Tregoe 決策分析框架，取代原本模糊的 Robust 評分。
> 完整框架詳見：`KT_Robust_決策框架.md`
> **核心工件**：Concept Route (Baslined), Decision Record (Draft), Evidence (Verified)

### 3.2.1 決策原則

**選 Robust，不選最優**

> 在早期，你要的不是「算出來最好」的設計，而是「最不怕未知」的設計。

**KT 如何實現這個原則**：
- MUST 條件：確保「不能壞的」不會壞（硬約束淘汰）
- WANT 條件：量化「抗未知能力」（加權評分）
- Adverse Consequences：確保「風險可控」（風險調整）

### 3.2.2 KT 決策流程 (四階段)

```
┌─────────────────────────────────────────────────────────────────┐
│  Stage 1: MUST 篩選                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 不滿足任一 MUST → 直接淘汰 (已在 Step 2.2.6 執行)             ││
│  └─────────────────────────────────────────────────────────────┘│
│                              ↓                                   │
│  Stage 2: WANT 評分                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 權重(團隊共識) × 滿足程度(基於 EVIDENCE) = 加權分數         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              ↓                                   │
│  Stage 3: Adverse Consequences (工件: Risk 評估)                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 機率 × 嚴重度 = 風險等級 → 調整或淘汰                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              ↓                                   │
│  Stage 4: 決策記錄 (工件: Decision Record)                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 主路線 + 備援 + 行動項目 + 簽核                             ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2.3 MUST 條件 (Go/No-Go) (已在 Step 2.2.6 完成)

**核心原則**：MUST 是「不可妥協」的硬約束，不滿足 = 直接淘汰。

### 3.2.4 WANT 條件 (加權評分)

**核心原則**：WANT 是「希望有但可妥協」的目標，用 權重×滿足程度 計算。

**關鍵改進**：每個評分必須有「可觀察的工程條件」和「證據 (Artifact ID)」，不是 AI 主觀判斷。

**標準 WANT 條件 (含評分標準) (工件: Constraint 的一部分)**

| WANT | 權重 | 10分條件 | 6分條件 | 2分條件 | 證據要求 (Artifact ID) |
|------|------|---------|---------|---------|--------------------|
| W1 餘裕深度 | 10 | 餘裕 ≥50% | 餘裕 ≥20% | 餘裕 <10% | Calc-SafetyFactor001 |
| W2 解耦程度 | 9 | 完全獨立 | 耦合點=2 | 耦合點≥4 | CLD-001 |
| W3 可恢復性 | 7 | 可熱插拔 | 可現場調整 | 需返廠 | Service-Doc001 |
| W4 簡潔度 | 8 | 零件 -30% | 零件 ±10% | 零件 +30% | BOM-Final001 |
| W5 公差鈍感 | 9 | 無敏感公差 | 敏感公差≤2 | 敏感公差≥5 | Sim-Tolerance001 |
| W6 供應韌性 | 6 | 全通用件 | 關鍵件≥2家 | 多獨家 | SC-Audit-001 |
| W7 驗證可行性 | 10 | 1週內驗證 | 4週內驗證 | 無法早期驗證 | TestPlan-001 |

### 3.2.5 Adverse Consequences (風險評估) (工件: Risk)

**風險矩陣 (與 Risk Register 連結)**

```
            嚴重度
            Low    Medium    High
機    High    M       H        H*
率    Medium  L       M        H
      Low     L       L        M

H* = 極高風險（考慮淘汰）
H  = 需顯著緩解
M  = 需緩解措施
L  = 可接受
```

### 3.2.6 KT 決策記錄模板 (工件: Decision Record)

```yaml
KT_決策記錄:
  決策聲明: "選擇一個 [目標]，滿足 [約束]，以達成 [結果]"
  日期: [yyyy-mm-dd]
  決策者: [姓名/角色]

  MUST_結果:
    通過: [方案列表]
    淘汰:
      - 方案X: [淘汰原因]

  WANT_結果:
    方案A: [總分] 分 (證據連結: EM-A001)
    方案C: [總分] 分 (證據連結: EM-C001)
    證據清單:
      - W1: [證據描述] (Artifact ID)
      - W2: [證據描述] (Artifact ID)

  風險評估:
    方案A:
      - [風險]: [等級] → [緩解措施] (Link to Risk-A001)

  決策:
    主路線: [方案] (Concept Route ID)
    理由: [為何選擇]
    備援: [方案] (Concept Route ID)
    理由: [為何作為備援]

  行動項目:
    - [ ] [任務] - Owner: [人] - Due: [日期] (Link to Action-001)

  簽核:
    決策者: _______________
    審核者: _______________
```

### 3.2.7 最小實驗設計 (已在 Step 3.1.loop 閉環)

本階段的最小實驗設計主要用於補足決策所需的最終證據，或確認主路線的關鍵假設。

### 3.2.8 行動計畫 (三階段) (更新)

**Phase 1 (Week 1-2): 把混沌變結構**
- [ ] 需求/限制模板完成
- [ ] 問題樹 + 矛盾列表 v0
- [ ] 假設台帳 v0
- [ ] **Anti-Anchor Sprint 完成，產出至少 1 條非對標路線**
- [ ] 方案集合 v0（至少 3 條，含 Interface Contract）
- [ ] MUST/WANT 條件定義 + 權重共識
- [ ] 風險登錄表 + Top 3 最小實驗設計

**Phase 2 (Week 3-6): 把結構變證據**
- [ ] 完成 Top 3 最小實驗
- [ ] **完成 Step 3.1 Evidence-based Design Review，Evidence Matrix 狀態: Reviewed**
- [ ] **完成所有 Step 3.1.loop 的證據補齊迴圈，北極星指標證據等級 ≥ E2**
- [ ] 執行 KT Decision Analysis（MUST→WANT→AC）
- [ ] 更新假設台帳（推翻也要記）
- [ ] 方案縮到 1-2 條，保留備援
- [ ] KT 決策記錄完成並簽核

**Phase 3 (Week 7-8): 把證據變資產**
- [ ] 約束庫沉澱（MUST/WANT 條件模板）
- [ ] 失效路徑庫沉澱
- [ ] 形成「下一案可重用」的 playbook
- [ ] **所有 Baseline 工件狀態: Baseline -> Released**

**Gate 3.2 檢查點**
> ✅ 所有方案都經過 Step 2.2.6 MUST 篩選。
> ✅ 每個 WANT 評分都有證據 (Artifact ID) 支撐 (不可為 E0)。
> ✅ 所有 H 風險都有緩解措施，且該措施的證據等級 ≥ E1。
> ✅ KT 決策記錄完整且已簽核 (Decision Record 狀態: Draft -> Reviewed)。
> ✅ 決策能被解釋：為何選「最穩」不是「最強」。
> ✅ 核心工件 Concept Route 狀態: Verified -> Baslined。

---

## Step 3.3: 內化與傳達 (費曼)

### 3.3.0 知識回寫 (Knowledge Writeback)

流程完成後，以下資產自動回寫至企業知識庫，供未來專案 RAG 檢索使用：

| 回寫內容 | 知識庫分類 | 用途 |
|---------|-----------|------|
| 最終 Decision Record | 決策紀錄庫 | 未來類似專案的決策參考 |
| 被推翻的假設 (Assumption Ledger) | Lessons Learned 庫 | 避免後續專案重複犯錯 |
| Evidence Matrix (含證據等級) | 證據範本庫 | 加速未來審查的證據收集 |
| Risk Register + 緩解措施 | FMEA/風險庫 | 歷史失效案例比對 |
| MUST/WANT 條件模板 | 約束庫 | 可複用的篩選條件 |
| Interface Contract (定版) | 介面規範庫 | 標準化介面定義 |

### 3.3.1 一頁式 (給老闆/跨部門)

```
┌─────────────────────────────────────────────────────────────┐
│                    [專案名稱] 設計決策摘要                    │
├─────────────────────────────────────────────────────────────┤
│ 我們選了什麼？                                               │
│   → [主路線簡述] (Link to Concept Route ID)                  │
│                                                              │
│ 為何它最 Robust？                                            │
│   → [三點關鍵理由] (Link to Decision Record ID)              │
│                                                              │
│ 未知有哪些？怎麼管理？                                       │
│   → [Top 3 風險 + 緩解措施] (Link to Risk Register ID)       │
│                                                              │
│ 下一步？                                                     │
│   → [最小實驗計畫 + 時程] (Link to Test Plan ID)             │
│                                                              │
│ 需要的支援？                                                 │
│   → [資源/決策/資訊]                                         │
└─────────────────────────────────────────────────────────────┘
```

### 3.3.2 RD 團隊 FAQ

| 問題 | 答案 |
|------|------|
| AI 會不會取代我？ | 不會。AI 是副駕，擴大可能性空間；工程師做最終判斷。 |
| AI 錯了誰負責？ | 人負責。AI 要有證據鏈，每個建議都可追溯假設。 |
| 我為什麼要填假設台帳？ | 因為返工最貴。台帳讓未知可見、可管理。 |
| SCAMPER/TRIZ 不就是喊創意？ | 不是。它們有固定輸出格式，必須附機制、風險、驗證。 |
| **我為什麼要填 Evidence Matrix？** | 審查不是看你說了什麼，是看你有沒有證據。它幫你追蹤證據缺口與下一步。 |

**Phase Gate 3 (= Gate 3.3) 檢查點**
> ✅ 新人看得懂。
> ✅ 老闆聽得懂。
> ✅ 工程師願意用。
> ✅ 所有核心工件狀態: Baslined -> Released。
> ✅ 核心工件 Decision Record 狀態: Reviewed -> Released。

---

# 附錄 A: 模板與規範

## 附錄 A.1: MUST Rulebook 模板 (可機器執行)

每條 MUST 規則都將被定義如下，以實現 Copilot 的自動化審查：

| MUST ID | 條件描述 | Input 欄位 (來自何種工件) | 判定公式 / 邏輯 | 證據類型 (Required Artifact) | Fail 處置 |
|---------|----------|------------------------|--------------------|----------------------------|-----------|
| M1 | 空間約束 | Concept Route.Interface.Envelope.CAD_ID | CAD Model干涉檢查 (與 Constraint.Hard_Constraints.Volume) | CAD Model (Verified) | 淘汰 |
| M2 | 成本預估 | Concept Route.BOM.Estimated_Cost | 比較 Concept Route.BOM.Estimated_Cost 與 Constraint.Hard_Constraints.Cost_Upper_Limit | Spreadsheet (Reviewed) | 淘汰 |
| M3 | 安全餘裕 | Concept Route.Safety_Margin.KPI_ID | KPI_ID (e.g. Stress_Margin) >= 1.2 | Calculation / Simulation Report (Reviewed) | 淘汰 |
| M4 | 解耦程度 | Concept Route.Coupling_Points | 關鍵耦合點數量 <= 2 (判斷自 CLD-ID) | CLD (Verified) / Expert Judgement | 淘汰 |
| M5 | 供應可行性 | Concept Route.Key_Components.Supplier_Audit_ID | 關鍵零組件是否有至少 2 家通過 Audit 的供應商 | Supplier Audit Report (Reviewed) | 淘汰 |
| **M6** | **製造路徑可行性** | Concept Route.Manufacturing.Process_Complexity | 初步評估關鍵製程 (如: 特殊成型, 高精度加工, 複雜組裝) 的可行性。 | DFM Pre-Assessment Report (Reviewed) | 淘汰 |

## 附錄 A.2: Evidence Matrix 模板

此矩陣作為 Step 3.1 的主要產出，用於追蹤每個方案的證據狀態和缺口。

| 欄位 ID | 欄位名稱 | 數據類型 | 說明 |
|---------|----------|----------|------|
| Category | 類別 | String | (e.g., KPI001, NVH002, DFM003) 連結到 Constraint 或 Risk |
| Requirement_Spec | 要求/規格 | String | 該類別的具體要求或目標數值 |
| Current_Evidence_ID | 目前證據 (Artifact ID) | String | 指向 Evidence 工件的 ID (e.g., Sim-Torque001, Exp-Motor001) |
| Evidence_Quality | 證據品質 (E0-E4) | Enum | 評估證據的可靠性等級 (E0: 推論, E1: 計算, E2: 仿真/Bench, E3: 實測, E4: 量產) |
| Evidence_Gap | 證據缺口 | String | 若證據品質不足，描述缺口為何，如：「缺乏實際馬達響應數據」 |
| Next_Min_Experiment_ID | 下一步最小實驗 (Artifact ID) | String | 指向用於補足證據缺口的最小實驗計畫 ID (e.g., Exp-Motor001) |
| Owner | Owner | String | 負責補足該證據缺口的團隊成員 |
| Due_Date | Due | Date | 補足證據的預計完成日期 |

## 附錄 A.3: Risk Register 模板

此表格用於記錄和追蹤方案級別的風險，連結到證據和緩解措施。

| 風險 ID | 描述 | 來源 (工件 ID, e.g., A001, C002) | 失效模式 | 機率 (Low/Medium/High) | 嚴重度 (Low/Medium/High) | 等級 (L/M/H/H*) | 緩解措施 (Artifact ID) | 監控指標 (Artifact ID) | Owner | Due Date |
|---------|------|--------------------------|----------|---------------------|----------------------|----------------|--------------------------|--------------------------|-------|----------|
| Risk-A001 | 新材料熱膨脹 | A001 | 結構變形導致功能失效 | Medium | High | H | Sim-Thermal001 (仿真驗證) | Sensor-Temp001 (溫升監控) | 張三 | 2026/03/15 |
| Risk-B001 | 獨家供應商 | SC-Audit-001 | 供應鏈中斷 | Medium | High | H | SC-Plan-001 (開發替代供應商) | SC-Report-001 (供應商審核報告) | 李四 | 2026/04/01 |

---

## 附錄 A.4: Pre-CAD Review Report 模板

此模板用於引導團隊在 Pre-CAD Gate (Step 2.3) 進行審查，詳情參考 `Pre_CAD_Review_Template.md` 文件。

---

**版本**: v1.6
**最後更新**: 2026-02-25
**適用範圍**: 早期概念設計階段 (從概念發散到主路線決策)
**重要更新**: Step 2.2.2 TRIZ 解矛盾升級為三路徑統一求解（`POST /triz/solve`）—— 分類(LLM) → 路由(TC/PC/SF) → 規則引擎查表 + LLM 具體化。新增 5 個 Prompt 模板 + 規則引擎 `triz_engine.py`。模組分工表更新為已實作的規則 vs LLM 分工。`UnifiedTrizResult` 取代舊的平面解法列表。
