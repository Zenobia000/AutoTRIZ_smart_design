# RD Design Copilot 整合流程狀態機與 R&R (E2E)

本文件以程式設計角度繪製 `RD Design Copilot 整合流程 (E2E)` 的狀態機圖，並說明每個階段的 Roles & Responsibilities (R&R)。
本文件核心概念為 **雙層狀態機 (Dual-Layer State Machine)**，同時管理 **流程狀態 (Process State)** 與 **工件狀態 (Artifact State)**。

> **v1.2 更新**：Step 編號已按實際執行順序重新編排，引入雙層狀態機概念，並加入 `Step 6e: 證據補齊 (Evidence Closure)` 迴圈。

## Step 編號對照

| 新編號 | 名稱 | Phase | 核心工件類型 |
|--------|------|-------|------------|
| Step 1 | 問題界定 | I | Constraint |
| Step 2 | 理解全貌（索克拉底） | I | Contradiction, Assumption |
| Step 3 | 系統建模（因果迴路+TRIZ矛盾+斷路點） | I | Contradiction, Breakpoint |
| Step 4 | 假設與驗證規劃（HDA+未知集合） | II | Assumption |
| **Step 5** | **創造與調整（TRIZ解矛盾→子系統定義→SCAMPER變形→方案集合→MUST快篩）** | **II** | Concept Route, Interface |
| **Step P** | **Pre-CAD 設計審查 (Pre-CAD Gate)** | **II** | Pre-CAD Review Report |
| **Step 6** | **設計審查 (CAD Gate - MVP CAD Review)** | **III** | Concept Route, Evidence Matrix, Risk |
| Step 6e | 證據補齊 (Evidence Closure) | III | Evidence |
| Step 7 | 決策與行動（KT Decision Analysis+最小實驗） | III | Concept Route, Decision Record, Evidence |
| Step 8 | 內化與傳達（費曼） | III | Asset |

## 核心流程狀態機 (Process State Machine)

```mermaid
stateDiagram-v2
    direction LR

    state "Phase I: 定義問題空間" as PhaseI {
        state "Step 1: 問題界定" as S1
        state "Step 2: 理解全貌" as S2
        state "Step 3: 系統建模" as S3

        S1 --> S2 : Gate 1 ✓
        S2 --> S3 : Gate 2 ✓
    }

    state "Phase II: 假設與發散" as PhaseII {
        state "Step 4: 假設與驗證規劃" as S4
        state "Step 5: 創造與調整" as S5 {
            state "5-0: Anti-Anchor Sprint" as S5_0
            state "5a: TRIZ 解矛盾" as S5a
            state "5b: 子系統定義" as S5b
            state "5c: SCAMPER 變形" as S5c
            state "5d: AI 方案生成" as S5d
            state "5e: MUST 快篩" as S5e

            S5_0 --> S5a : Anti-Anchor Gate ✓
            S5a --> S5b : 解法方向 → 指定子系統
            S5b --> S5c : 每個子系統執行 SCAMPER
            S5a --> S5d : TRIZ 解法
            S5c --> S5d : SCAMPER 變形
            S5d --> S5e : 候選方案 → Go/No-Go
        }
        state "Step P: Pre-CAD 設計審查" as S_P
        S4 --> S5 : Gate 4 ✓
        S5 --> S_P : Gate P ✓ (MVP CAD 候選集)
    }

    state "Phase III: 收斂與驗證" as PhaseIII {
        state "Step 6: 設計審查" as S6
        state "Step 6e: 證據補齊" as S6e
        state "Step 7: 決策與行動" as S7
        state "Step 8: 內化與傳達" as S8

        S6 --> S6e : 證據缺口 Found
        S6e --> S6 : 證據更新
        S6 --> S7 : Gate C ✓ (證據充足)
        S7 --> S8 : Gate 7 ✓
    }

    [*] --> S1 : DRAFT→PHASE_I (Gate 1)
    S3 --> S4 : Gate 3 ✓ (PHASE_I→PHASE_II)
    S_P --> S6 : PHASE_II→PHASE_III (Gate C)
    S8 --> [*] : Gate 8 ✓ (PHASE_III→COMPLETED)
```

## Gate 與 Phase 轉換對照 (更新)

系統有 8 個 Step-level Gate（每步一個），其中 4 個同時觸發 Phase 轉換：

| Gate | 位置 | Gate 類型 | Phase 轉換？ | 關鍵工件狀態轉換 |
|------|------|-----------|-------------|--------------------|
| Gate 1 | Step 1 → Step 2 | 內部 Gate | **DRAFT → PHASE_I** | Constraint: Draft → Reviewed |
| Gate 2 | Step 2 → Step 3 | 內部 Gate | Phase I 內部 | Contradiction, Assumption: Draft → Reviewed |
| Gate 3 | Step 3 → Step 4 | 內部 Gate | **PHASE_I → PHASE_II** | Contradiction: Reviewed → Verified; Breakpoint: Draft → Reviewed |
| Gate 4 | Step 4 → Step 5 | 內部 Gate | Phase II 內部 | Assumption: Reviewed → Verified |
| **Gate P** | Step 5 → Step P | **Pre-CAD Gate** | Phase II 內部 | Concept Route: Draft → Reviewed |
| **Gate C** | Step P → Step 6 | **CAD Gate** | **PHASE_II → PHASE_III** | Concept Route: Reviewed → Verified; Pre-CAD Review Report: Draft → Reviewed; MVP CAD Model: Draft → Reviewed |
| Gate 6 | Step 6 → Step 6e | 內部 Gate | Phase III 內部 | Evidence Matrix, Risk: Draft → Reviewed |
| Gate 7 | Step 7 → Step 8 | 內部 Gate | Phase III 內部 | Concept Route: Verified → Baslined; Decision Record: Draft → Reviewed |
| Gate 8 | Step 8 → Done | 內部 Gate | **PHASE_III → COMPLETED** | All Core Artifacts: Baslined → Released |
## 雙層狀態機概念圖 (Process State + Artifact State)

```mermaid
stateDiagram-v2
    direction LR

    state "Process: Step 6 (CAD Gate - 設計審查)" as Process6 {
        state "Artifact: EM (Evidence Matrix)" as EM_Artifact {
            state "Draft" as EM_Draft
            state "Reviewed" as EM_Reviewed
            state "Verified" as EM_Verified
            EM_Draft --> EM_Reviewed : 填寫 EM
            EM_Reviewed --> EM_Verified : 證據補齊 (S6e)
            EM_Verified --> EM_Reviewed : 發現新缺口
        }
        state "Artifact: Concept Route" as CR_Artifact {
            state "Reviewed" as CR_Reviewed
            state "Verified" as CR_Verified
            CR_Reviewed --> CR_Verified : 證據充足 (S6e Loop Completed)
        }
        state "Artifact: Risk" as Risk_Artifact {
            state "Draft" as Risk_Draft
            state "Reviewed" as Risk_Reviewed
            Risk_Draft --> Risk_Reviewed : 風險登錄
        }
        state "Artifact: MVP CAD Model" as MVP_CAD_Artifact {
            state "Draft" as MVP_CAD_Draft
            state "Reviewed" as MVP_CAD_Reviewed
            MVP_CAD_Draft --> MVP_CAD_Reviewed : 繪製 MVP CAD
        }
    }

    state "Process: Step 6e (證據補齊)" as Process6e {
        state "Artifact: Evidence" as Evid_Artifact {
            state "Draft" as Evid_Draft
            state "Verified" as Evid_Verified
            Evid_Draft --> Evid_Verified : 執行最小實驗
        }
    }

    state "Process: Step 7 (決策與行動)" as Process7 {
        state "Artifact: Decision Record" as DR_Artifact {
            state "Draft" as DR_Draft
            state "Reviewed" as DR_Reviewed
            DR_Draft --> DR_Reviewed : 完成 KT Decision
        }
    }

    Process6 --> Process6e : 發現證據缺口
    Process6e --> Process6 : 證據更新
    Process6 --> Process7 : Gate C ✓ (證據充足)
```

### 平行處理說明

在 Step 5 (創造與調整) 中，針對不同矛盾句或子系統，5a (TRIZ 解矛盾) 和 5c (SCAMPER 模組變形) 可以並行執行：

```mermaid
flowchart LR
    subgraph "Parallel TRIZ & SCAMPER"
        subgraph "TRIZ for Contradiction C-001"
            C001_Input["矛盾句 C-001"] --> TRIZ_C001["5a TRIZ 解矛盾"]
        end
        subgraph "SCAMPER for Subsystem A"
            SSA_Input["子系統 A"] --> SCAMPER_SSA["5c SCAMPER 變形"]
        end
        subgraph "SCAMPER for Subsystem B"
            SSB_Input["子系統 B"] --> SCAMPER_SSB["5c SCAMPER 變形"]
        end
    end
    TRIZ_C001 --> S5d_AI_Gen["5d AI 方案生成"]
    SCAMPER_SSA --> S5d_AI_Gen
    SCAMPER_SSB --> S5d_AI_Gen
```

所有並行產出的解法方向與變形最終匯聚到 5d (AI 方案生成) 做交叉組合，再由 5e (MUST 快篩) 統一淘汰。

## 階段與狀態說明 (R&R)

### Phase I: 定義問題空間

#### Step 1: 問題界定
- **目的**: 將模糊需求轉化為可檢查的約束句，為後續矛盾定義奠定基礎。
- **核心工件** (Artifacts): Constraint (Draft)
- **Human (RD Team) R&R**:
    - 定義 Mission, Hard Constraints, Soft Objectives, Non-Goals。
    - 明確「三個最不能失敗的指標」及其判斷方式。
- **AI (Copilot) R&R**:
    - 協助將需求改寫為約束句。
    - 生成缺口問卷。
    - 列出已知事實與未知缺口。
- **Gate 1**: 「三個最不能失敗指標」被明確說出，且每個指標有「可量測」或「可判斷」的方式。**核心工件 Constraint 狀態: Draft → Reviewed**。

#### Step 2: 理解全貌（索克拉底問答）
- **目的**: 挖掘「大家以為理所當然」的前提，為 TRIZ 矛盾識別做準備。
- **核心工件**: Contradiction (Draft), Assumption (Draft)
- **Human (RD Team) R&R**:
    - 參與索克拉底問答，提供見解和證據。
    - 初步識別潛在矛盾。
- **AI (Copilot) R&R**:
    - 固定執行索克拉底六類提問（澄清、假設、證據、觀點、後果、反思）。
    - 匯總問答結果，輸出初步的矛盾列表。
- **Gate 2**: 至少列出 10 條關鍵假設，標出 Top 3 致命假設；至少識別 3 條核心矛盾。**核心工件 Contradiction, Assumption 狀態: Draft → Reviewed**。

#### Step 3: 系統建模（因果迴路 + TRIZ 矛盾 + 斷路點）
- **目的**: 找到耦合點，將矛盾正式化為 TRIZ 句式，識別可介入的斷路點。
- **核心工件**: Contradiction (Verified), Breakpoint (Draft)
- **Human (RD Team) R&R**:
    - 輔助建立因果迴路圖。
    - 將矛盾正式化為 TRIZ 矛盾句。
    - 識別斷路點。
- **AI (Copilot) R&R**:
    - 協助繪製因果迴路圖，分析耦合關係。
    - 提供 TRIZ 矛盾句模板。
    - 根據因果迴路提示可能的斷路點。
- **Gate 3**: 至少 1 個因果迴路 + 3 個斷路點 + 每條核心矛盾有 TRIZ 正式句。**核心工件 Contradiction 狀態: Reviewed → Verified；Breakpoint 狀態: Draft → Reviewed**。

### Phase II: 假設與發散

#### Step 4: 假設與驗證規劃（HDA + 未知集合）
- **目的**: 建立假設台帳與未知集合，完整描述不確定性全貌。
- **核心工件**: Assumption (Verified)
- **Human (RD Team) R&R**:
    - 填寫假設台帳。
    - 定義未知集合 (U)。
- **AI (Copilot) R&R**:
    - 提供假設台帳模板。
    - 協助整理未知因子列表。
- **Gate 4**: Top 3 假設每個都有可在 1-2 週內完成的驗證設計。**核心工件 Assumption 狀態: Reviewed → Verified**。

#### Step 5: 創造與調整（TRIZ → 子系統 → SCAMPER → 方案 → MUST）
- **目的**: 用 TRIZ 解矛盾找方向，用 SCAMPER 做模組級變形，輸出結構化可審查的方案集合，並用 MUST 快篩淘汰不可行方案。此階段產出的候選方案將進入 **Pre-CAD Gate (Step P)** 進行首次收斂。
- **核心工件**: Concept Route (Draft), Interface (Draft)
- **Human (RD Team) R&R**:
    - 定義子系統清單。
    - 審查 AI 生成的解法方向、SCAMPER 變形及完整方案。
    - 定義 MUST 條件並執行 Go/No-Go 判定。
- **AI (Copilot) R&R**:
    - **5-0 Anti-Anchor Sprint**: 引導產生非典型架構概念。
    - **5a TRIZ 解矛盾**: 根據矛盾句生成原理+抽象策略+工程對映。
    - **5b 子系統定義**: 識別受影響子系統。
    - **5c SCAMPER 模組變形**: 對每個子系統執行 SCAMPER 動作。
    - **5d AI 方案生成**: 整合 TRIZ 解法 + SCAMPER 變形，生成完整方案規格 (含 Interface Contract)。
    - **5e MUST 快篩**: 對候選方案逐項檢查 MUST 條件，不通過者淘汰。
- **平行處理**: 不同矛盾句的 TRIZ 解法、不同子系統的 SCAMPER 變形可並行執行。
- **Gate P (Pre-CAD Gate) 前提**: 至少保留 3 條「架構級」路線，其中包含至少 1 條 Anti-Anchor 路線。每條路線都有完整的方案規格 (機制、假設、風險、最小驗證)，並產出初步的 **Interface Contract**。每條路線的 **MUST Rule** 都經過判斷，並提供對應的初步證據。**核心工件 Concept Route, Interface 狀態: Draft → Reviewed**。

#### Step P: Pre-CAD 設計審查 (Pre-CAD Gate)
- **目的**: 在投入大量 CAD 繪製和詳細模擬之前，利用「可驗證的最小資訊」篩選和縮減候選設計方案，將發想階段的 20+ 個點子收斂到 3–5 條最優架構路線。
- **核心工件**: Concept Route (Verified), Pre-CAD Review Report (Draft)
- **Human (RD Team) R&R**:
    - 依據 `Pre_CAD_Review_Template.md` 進行審查，填寫 Pre-CAD 審查表。
    - 決策保留 3-5 條架構級差異顯著的 Concept Route。
- **AI (Copilot) R&R**:
    - 提供 Pre-CAD 審查表模板。
    - 協助分析和匯總審查結果。
- **Gate C (CAD Gate) 前提**: 經 Pre-CAD 審查，候選 Concept Route 已收斂至 3–5 條。每條保留路線的 Interface Contract 已更新。每條保留路線都明確了下一步進行 MVP CAD 的最小幾何範圍。**核心工件 Concept Route 狀態: Reviewed → Verified (通過 Pre-CAD Gate)；Pre-CAD Review Report 狀態: Draft → Reviewed**。

#### Step 6: 設計審查 (CAD Gate - MVP CAD Review)
- **目的**: 針對通過 Pre-CAD Gate 的候選方案，進行 MVP CAD 的初步審查，利用有限的 CAD/模擬成果快速識別潛在的設計缺陷、製造困難或整合問題，並將「證據缺口」轉化為下一步的最小實驗。此階段即為 **CAD Gate (Gate C)**。
- **核心工件**: Concept Route (Verified), Evidence Matrix (Draft), Risk (Reviewed), MVP CAD Model (Draft)
- **Human (RD Team) R&R**:
    - 繪製 MVP CAD 模型。
    - 填寫 **Design Review Evidence Matrix (DR EM)**，並評估證據品質 (E0-E4)。
    - 進行黑帽質疑。
    - 建立風險登錄表，指派 Owner、定義緩解措施和監控指標。
- **AI (Copilot) R&R**:
    - 提供 DR EM 模板，協助追蹤證據狀態。
    - 提供 SWOT 分析框架和黑帽質疑清單。
    - 協助整理風險登錄表，並進行歷史失效案例比對 (Failure Mode Transfer)。
- **Gate C (CAD Gate) 前提**: 若北極星指標證據等級 < E2 或存在重大證據缺口，進入 Step 6e。若證據充足，則通過 Gate C。

#### Step 6e: 證據補齊 (Evidence Closure)
- **目的**: 針對 Step 6 審查中發現的證據缺口，執行快速的最小實驗、仿真或供應商確認，以將證據等級提升至 Gate 7 的要求。
- **核心工件**: Evidence (Verified)
- **Human (RD Team) R&R**:
    - 設計並執行最小實驗。
    - 收集新的數據和證據。
- **AI (Copilot) R&R**:
    - 協助設計最小實驗。
    - 歸檔新的證據工件。
- **迴圈**: 完成 Step 6e 後，返回 Step 6 重新審查 Evidence Matrix。

#### Step 7: 決策與行動（KT Decision Analysis + 最小實驗）
- **目的**: 運用 KT Decision Analysis 框架進行決策，並設計最小實驗以補足最終決策所需證據。
- **核心工件**: Concept Route (Baslined), Decision Record (Draft)
- **Human (RD Team) R&R**:
    - 執行 KT Decision Analysis (WANT 評分、Adverse Consequences)。
    - 基於證據 (Artifact ID) 為 WANT 條件打分。
    - 完成 KT 決策記錄並簽核。
- **AI (Copilot) R&R**:
    - 提供 KT 決策流程模板 (WANT/AC)。
    - 提供標準 WANT 條件及評分標準模板。
    - 協助整理風險矩陣與風險評估表。
    - 提供最小實驗規格模板。
- **Gate 7**: 所有方案經 Step 5e MUST 篩選。每個 WANT 評分都有證據支撐。所有 H 風險都有緩解措施。KT 決策記錄完整且已簽核。**核心工件 Concept Route 狀態: Verified → Baslined；Decision Record 狀態: Draft → Reviewed**。

#### Step 8: 內化與傳達（費曼）
- **目的**: 將決策結果有效傳達給不同層級的利害關係人，並促進知識內化。
- **核心工件**: Asset
- **Human (RD Team) R&R**:
    - 製作一頁式摘要。
    - 編寫 RD 團隊 FAQ。
    - 更新約束庫、失效路徑庫等知識資產。
- **AI (Copilot) R&R**:
    - 提供一頁式摘要模板和 FAQ 結構建議。
    - 協助將決策過程中的知識沉澱為可重用資產。
- **Gate 8**: 新人看得懂；老闆聽得懂；工程師願意用。**所有核心工件狀態: Baslined → Released**。
