# Pre-CAD Review Report Template

## 說明
此模板用於 RD Design Copilot 流程中 Gate P (Pre-CAD Gate) 的審查。其目的在於發想階段利用「可驗證的最小資訊」篩選和縮減候選設計方案，並在投入大量 CAD 繪製和詳細模擬之前，淘汰不具可行性的方案。

## Pre-CAD 審查表

**方案 ID**：`CR-A001` (連結到 Concept Route 工件)

| 審查維度 | 審查項目 | 評估內容 (基於方案規格 & Interface Contract) | 證據 (Artifact ID / 描述) | 評分 (1-5, 5為最佳) | 評語/建議 |
|---|---|---|---|---|---|
| **1. MUST (硬限制)** | M1 空間約束 | 方案預估幾何包絡是否能置入目標空間？ | CR-A001.Interface.Envelope.Description | 4 | 初步判斷可行，需進一步 MVP CAD 確認 |
| | M2 成本預估 | 方案核心零組件粗估成本是否符合預期？ | CR-A001.BOM.Estimated_Cost | 3 | 成本尚可控，但有潛在風險零組件 |
| | M3 安全餘裕 | 北極星指標是否有初步安全餘裕判斷？ | CR-A001.Safety_Margin.KPI_ID (Expert Judgement) | 3 | 某關鍵指標餘裕較低，需早期實驗驗證 |
| | M4 解耦程度 | 關鍵耦合點數量是否符合要求？ | CR-A001.Coupling_Points (CLD-001) | 5 | 模組化程度高，耦合點控制良好 |
| | M5 供應可行性 | 關鍵零組件供應鏈是否可行？ | CR-A001.Key_Components.Supplier_Audit_ID | 4 | 需開發新供應商，但技術可行 |
| | M6 製造路徑可行性 | 核心製造工藝是否初步可行？ | CR-A001.Manufacturing.Process_Complexity (DFM Pre-Assessment) | 3 | 有挑戰性工藝，需早期製程驗證 |
| **2. 解耦程度 (Decoupling)** | 關鍵模組間的介面是否清晰？ | CR-A001.Interface.Description | 5 | 介面定義清晰，獨立性高 |
| | 更改一個模組是否會劇烈影響其他模組？ | CR-A001.Risk.Source_Artifact_ID (CLD-001) | 4 | 部分介面變更會影響，但可控 |
| **3. 可驗證性 (Testability)** | 核心假設能否透過 1-2 週小實驗驗證？ | CR-A001.Min_Experiment (Exp-A001) | 4 | 大部分核心假設可快速驗證 |
| | 是否有不可驗證的「黑箱」機制？ | CR-A001.Mechanism.Physical_Principle | 5 | 所有機制都有可驗證的物理原理 |
| **4. 主要風險機制 (Failure Mechanism)** | 方案最可能怎麼死？ (e.g., 熱失控, 早期磨損, 雜訊干擾) | CR-A001.Risk.Failure_Mode (Risk-A001) | 3 | 熱管理風險較高，需早期仿真 |
| | 是否有類似產品的歷史失效經驗？ | Historical Failure Database (FFMEA-001) | 4 | 有參考案例，可學習避免 |
| **5. 最小 CAD 工作量 (MVP CAD Effort)** | 需要繪製哪些最小幾何模型以進行粗仿真？ | CR-A001.Interface.Envelope.Description | 5 | 只需繪製核心結構，約 2 天工時 |
| | 是否需要製作實體原型進行概念驗證？ | CR-A001.Min_Experiment | 3 | 建議製作簡單物理模型驗證關鍵運動學 |

---

## Pre-CAD Gate 決策總結

**概念路線 ID**：`CR-A001`

**決策結果**：[通過 / 建議修改 / 淘汰]

**關鍵理由**：
*   **優勢**：在解耦程度和可驗證性方面表現優異，能有效降低早期開發風險。
*   **風險**：M3 (安全餘裕) 和 M6 (製造可行性) 存在潛在挑戰，需在後續 MVP CAD 階段重點關注。

**後續行動**：
*   進行 MVP CAD 繪製，聚焦在核心結構和關鍵介面。
*   針對 M3 和 M6 的挑戰，規劃 Step 6e 的最小實驗。

**審查人**：
*   [姓名/角色]：__________
*   [姓名/角色]：__________
*   日期：__________

---

**版本**: v1.0
**最後更新**: 2026-02-24
**適用範圍**: RD Design Copilot Gate P (Pre-CAD Gate)
