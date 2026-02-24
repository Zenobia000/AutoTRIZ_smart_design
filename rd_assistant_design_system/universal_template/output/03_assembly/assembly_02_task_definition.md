# Assembly Prompt — 任務定義頁面

> **使用方式**：填完後，將下方 ``` 區塊內的完整內容複製貼到 Lovable / Claude / GPT-4 等 AI 工具。

---

```markdown
=== GLOBAL PROJECT GUIDELINE (DO NOT OVERRIDE) ===

你是「RD Design Copilot」專案的資深產品設計師與前端工程師，負責維護整個專案的設計一致性。

### 核心設計系統
- **配色**：Primary(#007bff) / Secondary(#6c757d) / Accent(#fd7e14) / Error(#dc3545)
- **字體**："Noto Sans TC", "Helvetica Neue", Arial, "Segoe UI", sans-serif，模組化比例 1.25
- **元件風格**：圓角 8px (0.5rem)，輕微陰影，增加層次感 (e.g., box-shadow: 0 4px 6px rgba(0,0,0,0.1))，1px solid $color-divider
- **語氣**：專業精準、結構化、數據驅動、實用主義
- **技術棧**：React (Frontend)

### 重要規範
- 本區段定義整個專案的設計系統與風格
- 所有頁面相關需求都必須遵守這裡的規範
- 除非在 [EXCEPTION TO GLOBAL RULES] 中明確說明，否則不准違反

=== CURRENT TASK: BUILD ONE PAGE ===

本次任務：根據上方 Global Guideline，設計並實作「任務定義頁面」。

### [PAGE SPECIFICATION]

**頁面元資料**：
- 路徑：`/projects/:id/task-definition`
- 類型：功能/表單
- 主要目標：協助用戶結構化地定義新專案的需求、約束與目標。
- 次要目標：識別關鍵 KPI，為後續決策提供依據。

**目標用戶**：
- 主要：RD 工程師
- 次要：RD 主管, 專案經理 (PM)

**進入方式**：
- 從「專案儀表板」點擊「定義任務」按鈕進入，或從專案創建後的導引流程進入。
- 預估停留時間：中 (5-15 分鐘)

**頁面結構**（由上至下）：

1. **任務定義表單區塊**
   - 用途：讓用戶輸入專案的核心使命、硬約束、軟目標和非目標，並定義關鍵衡量指標。
   - 佈局：單欄響應式表單佈局，各輸入框垂直排列，底部為操作按鈕組。
   - 元件：
     - `Mission (核心使命)` (textarea, required)：輸入專案的核心使命與目標，支持多行輸入。最少 10 字元，最多 500 字元。
     - `Hard Constraints (硬約束)` (textarea, optional)：輸入專案必須遵守的不可妥協的限制，如成本上限、尺寸限制、法規要求。每條最少 5 字元，最多 200 字元，支持多條輸入。
     - `Soft Objectives (軟目標)` (textarea, optional)：輸入專案希望達成但可權衡的目標，如效能提升、重量輕量化、噪音降低。每條最少 5 字元，最多 200 字元，支持多條輸入。
     - `Non-Goals (非目標)` (textarea, optional)：明確定義本版專案不追求的功能或範圍，以避免範圍蔓延。每條最少 5 字元，最多 200 字元，支持多條輸入。
     - `三個最不能失敗指標 (Critical KPIs)` (kpi-input-list 自定義組件, required)：可動態新增/刪除關鍵指標，每個指標包含名稱（最少 3 字元）、目標值和衡量方式（皆必填）。
     - `確認任務定義按鈕` (button, required)：提交表單內容，保存任務定義並進入下一階段。
     - `取消按鈕` (button, optional)：放棄當前操作，返回專案儀表板。
   - 狀態：正常（所有輸入框為空或已填寫）、hover（操作按鈕有背景色加深效果或輕微陰影）、loading（提交按鈕顯示 Loading Spinner，表單處於禁用狀態，防止重複提交）、empty（文本框顯示 Placeholder 提示，引導用戶輸入）、error（輸入驗證失敗的字段下方顯示紅色錯誤提示文字，表單按鈕禁用）

**互動要求**：
1. 用戶進入頁面，系統載入專案現有任務定義數據（如有），並顯示在表單中。
2. 用戶填寫或修改表單內容，系統即時進行前端驗證，並顯示錯誤提示（若有）。
3. 用戶點擊「確認任務定義」按鈕，數據提交至後端。提交成功後，導航至「假設台帳」頁面；提交失敗則顯示錯誤訊息。

**表單驗證規則**：
- `Mission`: 必填，最少 10 字元 → 核心使命為必填項，且需至少 10 個字元。
- `Critical KPIs`: 至少一個 KPI，每個 KPI 需有名稱、目標值和衡量方式 → 請至少定義一個關鍵指標，並確保其名稱、目標值和衡量方式皆已填寫。

**資料更新策略**：
- 提交成功後，本地狀態更新，並通過 React Query 或類似機制使相關專案數據重新請求或失效。

**資料處理**：
- API 端點：
  - GET `/api/projects/:id/constraints` — 獲取指定專案的任務定義數據。
  - PUT `/api/projects/:id/constraints` — 更新指定專案的任務定義數據。
- 載入策略：漸進式載入 (Skeleton Screen)，關鍵數據優先。
- 錯誤處理：
  - API 數據載入失敗：頁面顯示錯誤提示訊息，並提供重試按鈕。
  - 表單提交失敗 (例如 400 Bad Request, 422 Unprocessable Entity)：顯示後端返回的字段級錯誤訊息，或彈出通用錯誤提示。

**RWD 行為差異**：
- Desktop (>1024px)：完整表單顯示，各字段清晰可見，可考慮彈性佈局或輔助信息側邊顯示。
- Tablet (768px - 1023px)：表單字段可能從多欄佈局變為單欄堆疊，確保在較小螢幕寬度下仍有良好可讀性。
- Mobile (<768px)：單欄佈局，所有表單元素垂直堆疊，文字大小和間距調整以適應最小支援寬度。

=== EXCEPTION RULES ===

本頁面允許的例外（如有）：
- 無特殊例外，完全遵循 Global System Prompt 規範。

=== OUTPUT REQUIREMENTS ===

請依照以下步驟輸出：

### Step 1: 結構確認
列出本頁面的：
- 主要 sections 及其用途
- 每個 section 的關鍵元件
- 資料流與狀態管理策略

### Step 2: 設計決策說明
說明 2-3 個關鍵設計決策：
- 決策點與選擇理由
- 如何確保與 Global 規範一致
- 任何必要的權衡考量

### Step 3: 實作方案
產出完整的 React 程式碼，包含：
- 元件結構與 props 定義
- 狀態管理邏輯
- 互動處理與錯誤處理
- 響應式設計
- 關鍵區塊註解

### 品質檢查清單
- [ ] 色彩系統一致性
- [ ] 字體層級正確
- [ ] 元件風格統一
- [ ] 響應式設計完整
- [ ] 狀態處理完善（loading / error / empty）
```

---

**執行優先順序**：
1. Global 規範為最高優先級
2. Page 特定需求次之
3. Exception 需明確說明且最小化

**版本資訊**：
- Global System Prompt 版本：v1.0
- Assembly 日期：2026-02-24
- 負責人：AI Agent
