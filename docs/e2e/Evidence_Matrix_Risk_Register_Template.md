# Evidence Matrix & Risk Register Template

## 說明
此文件提供 RD Design Copilot 流程中 Step 3.1 (設計審查) 所需的 Evidence Matrix 和 Risk Register 模板。這些模板旨在結構化證據追蹤、風險管理，並連結至數位線索中的核心工件。

---

## 1. Evidence Matrix Template (工件: Evidence Matrix)

**Purpose**: To track the evidence status and gaps for each concept route, ensuring decisions are evidence-driven. This matrix is the primary output of Step 3.1.

| 欄位 ID | 欄位名稱 | 數據類型 | 說明 | 範例內容 |
|---|---|---|---|---|
| `CR_ID` | **概念路線 ID** | String | 連結到 `Concept Route` 工件 | `CR-A001` |
| `Category` | **類別** | String | 該行證據所屬的領域或要求 (e.g., KPI, NVH, DFM, Reliability) | `KPI001` (騎乘體驗), `NVH002` (噪音表現), `DFM003` (可製造性), `Risk-A001` (熱衰退風險) |
| `Requirement_Spec` | **要求/規格** | String | 該類別的具體要求、目標數值或需驗證的假設 | `起步扭矩建立時間 ≤ 200ms`, `低速爬坡噪音 ≤ 60dB`, `關鍵件裝配時間 ≤ 5min`, `新材料熱膨脹` |
| `Current_Evidence_ID` | **目前證據 (Artifact ID)** | String | 指向 `Evidence` 工件的 ID (e.g., `Sim-Torque001`, `Exp-Motor001`, `DFM-Review001`)。若有多個證據，可列出主要或最新 ID。 | `Sim-Torque001` |
| `Evidence_Quality` | **證據品質 (E0-E4)** | Enum | 評估證據的可靠性等級。 <br> **E0**: 只有推論 <br> **E1**: 有計算/估算 <br> **E2**: 有仿真或 Bench Test <br> **E3**: 有實測 (接近真實情境) <br> **E4**: 量產條件下證據 | `E1` |
| `Evidence_Gap` | **證據缺口** | String | 若證據品質不足 (e.g., E0/E1)，簡潔描述缺口為何。 | `實際馬達響應數據不足` |
| `Next_Min_Experiment_ID` | **下一步最小實驗 (Artifact ID)** | String | 指向用於補足證據缺口的 `Evidence` 工件 ID (e.g., `Exp-Motor001`)。此即 Step 3.1.loop 的行動計畫。 | `Exp-Motor001` |
| `Owner` | **Owner** | String | 負責補足該證據缺口的團隊成員 | `張三` |
| `Due_Date` | **Due** | Date | 補足證據的預計完成日期 | `2026-03-15` |
| `Status` | **狀態** | Enum | (Pending, In Progress, Completed, Blocked) | `Pending` |

---

## 2. Risk Register Template (工件: Risk)

**Purpose**: To systematically identify, assess, and manage risks associated with each concept route, linking them to evidence and mitigation actions. This is integrated with the Evidence Matrix.

| 欄位 ID | 欄位名稱 | 數據類型 | 說明 | 範例內容 |
|---|---|---|---|---|
| `Risk_ID` | **風險 ID** | String | 唯一識別碼 | `Risk-A001` |
| `CR_ID` | **概念路線 ID** | String | 連結到 `Concept Route` 工件 | `CR-A001` |
| `Description` | **風險描述** | String | 風險的簡潔描述 (e.g., 新材料熱膨脹導致結構變形) | `新材料熱膨脹導致結構變形` |
| `Source_Artifact_ID` | **來源 (工件 ID)** | String | 連結到觸發此風險的工件 (e.g., `Assumption A001`, `Contradiction C002`, `Interface I001`) | `Assumption A001` |
| `Failure_Mode` | **失效模式** | String | 具體的失效方式 (e.g., 早期疲勞失效, 過熱) | `結構變形導致功能失效` |
| `Probability` | **機率** | Enum (Low, Medium, High) | 評估風險發生的可能性 | `Medium` |
| `Severity` | **嚴重度** | Enum (Low, Medium, High) | 評估風險一旦發生造成的影響 | `High` |
| `Level` | **風險等級** | Enum (L, M, H, H*) | 綜合機率與嚴重度評定 (H* = 極高風險) | `H` |
| `Mitigation_Action` | **緩解措施** | String | 針對此風險計畫採取的行動 (e.g., `Sim-Thermal001 (仿真驗證)`, `SC-Plan-001 (開發替代供應商)`) | `Sim-Thermal001 (仿真驗證)` |
| `Monitoring_Metric` | **監控指標 (Artifact ID)** | String | 用於監控風險狀態的指標或數據 (e.g., `Sensor-Temp001 (溫升監控)`) | `Sensor-Temp001 (溫升監控)` |
| `Owner` | **Owner** | String | 負責管理此風險的團隊成員 | `張三` |
| `Due_Date` | **Due Date** | Date | 緩解措施的預計完成日期 | `2026-03-15` |
| `Status` | **狀態** | Enum (Open, In Progress, Closed) | `Open` |

---

**版本**: v1.0
**最後更新**: 2026-02-24
**適用範圍**: RD Design Copilot Step 3.1 (設計審查)
