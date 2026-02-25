# MUST Rulebook Template (可機器執行)

## 說明
此模板用於定義可機器執行的 MUST 條件，作為 RD Design Copilot 流程中 Step 2.2.6 (MUST 快篩) 的依據。每條 MUST 規則都應詳細定義其輸入、判定邏輯、所需證據類型及不通過時的處理方式。

## MUST 規則定義

| 欄位名稱 | 說明 | 範例數據類型 / 結構 | 連結工件 / 欄位 (Schema Path) | 判定邏輯 / 公式 | 證據類型 (Required Artifact) | Fail 處置 |
|---|---|---|---|---|---|---|
| **MUST ID** | 唯一識別碼 | String | N/A | N/A | N/A | N/A |
| **條件描述** | MUST 條件的簡潔描述 | String | N/A | N/A | N/A | N/A |
| **Input 欄位** | 判定所需數據的來源。可引用其他工件的特定欄位。 | String / Array of Strings | `Concept Route.Interface.Envelope.CAD_ID` | `Concept Route.BOM.Estimated_Cost` | `Constraint.Hard_Constraints.Volume` | `Risk.Level` | N/A |
| **判定邏輯 / 公式** | 用於判斷 MUST 條件是否通過的具體邏輯或計算公式。應盡量量化。 | String (e.g., Python-like expression) | N/A | `CAD_Model.Interference_Check(Envelope.CAD_ID, Constraint.Hard_Constraints.Volume)` | `BOM.Estimated_Cost <= Constraint.Hard_Constraints.Cost_Upper_Limit` | `Risk.Level = 'H*' or 'H'` | N/A |
| **證據類型** | 支援判定所需的證據檔案或數據類型。 | Enum (CAD Model, Spreadsheet, Report, Sim Data, Test Log, Expert Judgement, SC Response) | N/A | `CAD Model (Verified)` | `Spreadsheet (Reviewed)` | `Simulation Report (Verified)` | N/A |
| **Fail 處置** | 若 MUST 條件不通過，系統應採取的動作。 | Enum (淘汰, 降級, 列為風險) | N/A | `淘汰` | `降級` | `列為風險` | N/A |

---

## MUST 規則範例

| MUST ID | 條件描述 | Input 欄位 (Schema Path) | 判定邏輯 / 公式 | 證據類型 (Required Artifact) | Fail 處置 |
|---|---|---|---|---|---|---|
| **M1** | **空間約束**：方案概念必須能置入目標空間包絡內 | `Concept Route.Interface.Envelope.CAD_ID`, `Constraint.Hard_Constraints.Volume` | `CAD_Model.Interference_Check(Concept Route.Interface.Envelope.CAD_ID, Constraint.Hard_Constraints.Volume)` | `CAD Model (Verified)` | `淘汰` |
| **M2** | **成本預估**：方案概念的預估 BOM 成本不得超過目標上限 | `Concept Route.BOM.Estimated_Cost`, `Constraint.Hard_Constraints.Cost_Upper_Limit` | `Concept Route.BOM.Estimated_Cost <= Constraint.Hard_Constraints.Cost_Upper_Limit` | `Spreadsheet (Reviewed)` | `淘汰` |
| **M3** | **安全餘裕**：核心北極星指標必須具備合理的設計安全餘裕 | `Concept Route.Safety_Margin.KPI_ID`, `Constraint.Soft_Objectives.Min_Safety_Margin_Factor` | `Concept Route.Safety_Margin.KPI_ID >= Constraint.Soft_Objectives.Min_Safety_Margin_Factor` | `Calculation (Verified)` / `Simulation Report (Verified)` | `淘汰` |
| **M4** | **解耦程度**：方案概念不應引入過多的關鍵耦合點，避免系統複雜性失控 | `Concept Route.Coupling_Points`, `Breakpoint.CLD_ID`, `Constraint.Hard_Constraints.Max_Coupling_Points` | `COUNT(Concept Route.Coupling_Points WHERE Concept Route.Coupling_Points.Is_Critical = TRUE) <= Constraint.Hard_Constraints.Max_Coupling_Points` | `CLD (Verified)` / `Expert Judgement` | `淘汰` |
| **M5** | **供應可行性**：方案概念的關鍵零組件必須具備基本的供應韌性 | `Concept Route.Key_Components.Supplier_Audit_ID` | `Concept Route.Key_Components.Supplier_Audit_ID.Approved_Suppliers.Count >= 2` | `Supplier Audit Report (Reviewed)` / `SC Response (Verified)` | `淘汰` |
| **M6** | **製造路徑可行性**：方案概念的關鍵製造工藝必須具備初步的可行性 | `Concept Route.Manufacturing.Process_Complexity`, `Constraint.Hard_Constraints.Mfg_Capability` | `Concept Route.Manufacturing.Process_Complexity` 與 `Constraint.Hard_Constraints.Mfg_Capability` 匹配度評估 | `DFM Pre-Assessment Report (Reviewed)` / `Mfg Expert Judgement` | `淘汰` |

---

**版本**: v1.0
**最後更新**: 2026-02-24
**適用範圍**: RD Design Copilot Step 2.2.6 (MUST 快篩)
