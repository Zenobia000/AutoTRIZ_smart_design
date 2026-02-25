# Assembly Prompt — 方案探索

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

本次任務：根據上方 Global Guideline，設計並實作「方案探索」。

### [PAGE SPECIFICATION]

**頁面元資料**：
- 路徑：`/projects/:id/solution-explorer`
- 類型：列表/詳情/工具
- 主要目標：協助用戶基於已識別的矛盾，生成、篩選和評估多個設計方案。
- 次要目標：記錄方案的機制、假設、風險、最小驗證，並進行 MUST 快篩。

**目標用戶**：
- 主要：RD 工程師
- 次要：RD 主管

**進入方式**：
- 從「矛盾識別頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
- 預估停留時間：長 (20-40 分鐘)

**頁面結構**（由上至下）：

1. **矛盾選擇與方案生成區**
   - 用途：選擇矛盾作為輸入，觸發 AI 生成初始方案集。
   - 佈局：頂部操作區，包含下拉選單和按鈕。
   - 元件：
     - `矛盾選擇器` (dropdown, required)：從該專案已識別的矛盾中選擇一個或多個。必須選擇至少一個矛盾。
     - `生成方案按鈕` (button primary, required)：點擊後觸發 AI 生成方案。
   - 狀態：正常（下拉選單可用，按鈕可點擊）、loading（生成方案中，按鈕禁用並顯示 Loading Spinner）、error（選擇矛盾失敗或生成方案失敗時顯示錯誤提示）

2. **方案列表與篩選區**
   - 用途：展示 AI 生成的方案集，支持查看詳情和 MUST 快篩。
   - 佈局：響應式卡片或表格佈局，支持查看詳情和篩選。
   - 元件：
     - `方案卡片/列表項` (card/list item, required)：顯示方案名稱（最長 100 字元）、簡短描述（最長 200 字元）、MUST 快篩結果 (以標籤或圖標表示)、操作按鈕 (查看詳情)。
     - `MUST 快篩標籤/篩選器` (tag/filter, optional)：顯示方案是否通過各項 MUST 快篩，支持按 MUST 條件篩選。
   - 狀態：正常、empty（無方案時顯示「沒有方案」提示）、loading（方案數據載入中顯示骨架屏）、error（數據載入失敗）

3. **方案詳情與編輯區**
   - 用途：顯示單一方案的詳細信息，並允許用戶編輯、添加更多細節。
   - 佈局：側邊抽屜 (Drawer) 或模態框 (Modal) 中的詳情佈局。
   - 元件：
     - `方案名稱` (input text, required)：顯示/編輯方案名稱。
     - `機制說明` (textarea, required)：詳細描述方案的物理原理和結構。
     - `假設清單` (list, required)：顯示方案基於的假設，可連結到假設台帳，支持編輯。
     - `風險評估` (table, required)：顯示方案引入的新風險和評估，支持編輯。
     - `最小驗證` (textarea, required)：描述驗證此方案所需的最小實驗。
     - `MUST 快篩結果` (checklist/badges, required)：顯示此方案通過/未通過的 MUST 條件，可交互。
     - `保存/取消按鈕` (button group, required)：保存編輯或取消操作。
   - 狀態：正常、loading（數據保存中顯示 Loading Spinner）、error（驗證失敗或保存失敗）

**互動要求**：
1. 用戶進入方案探索頁面，系統載入已生成的方案列表（如有）。
2. 用戶從下拉選單中選擇一個或多個矛盾，點擊「生成方案」按鈕，觸發 AI 根據選擇的矛盾和知識庫生成一系列初步設計方案。
3. AI 生成的方案顯示在列表中，用戶可點擊方案卡片/列表項查看詳細信息，並在詳情區進行編輯。
4. 方案會自動進行 MUST 快篩，篩選結果即時顯示在卡片/列表項上。用戶可根據篩選結果決定是否進一步編輯或淘汰方案。

**表單驗證規則**：
- `方案名稱`: 必填，最少 5 字元 → 方案名稱為必填項，且需至少 5 個字元。
- `機制說明`: 必填，最少 50 字元 → 機制說明為必填項，且需至少 50 個字元。

**資料更新策略**：
- AI 生成新方案後，方案列表自動刷新。
- 用戶編輯方案並保存後，該方案的詳細信息自動刷新。

**資料處理**：
- API 端點：
  - GET `/api/projects/:id/contradictions` — 獲取指定專案的矛盾列表，用於矛盾選擇器。
  - POST `/api/projects/:id/solutions/generate` — 根據選定的矛盾觸發 AI 生成方案。
  - GET `/api/projects/:id/solutions` — 獲取指定專案的方案列表。
  - PUT `/api/projects/:id/solutions/:solution_id` — 更新方案信息。
- 載入策略：漸進式載入 (Skeleton Screen)，關鍵數據優先。
- 錯誤處理：
  - AI 生成失敗：顯示 AI 處理失敗提示，建議用戶重新嘗試或調整輸入。
  - MUST 快篩服務失敗：顯示快篩失敗提示，或標記方案為「待手動審核」。
  - 方案數據載入失敗：頁面顯示錯誤提示訊息，提供重試按鈕。

**RWD 行為差異**：
- Desktop (>1024px)：矛盾選擇與生成區、方案列表可並排顯示，方案詳情以側邊抽屜形式展示。
- Tablet (768px - 1023px)：佈局調整為堆疊，方案列表可能簡化顯示，方案詳情以模態框形式展示。
- Mobile (<768px)：所有區塊垂直堆疊，方案列表卡片式顯示，方案詳情為全屏模態框。

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
