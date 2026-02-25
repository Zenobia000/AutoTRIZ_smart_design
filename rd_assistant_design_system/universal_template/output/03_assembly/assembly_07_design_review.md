# Assembly Prompt — 設計審查

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

本次任務：根據上方 Global Guideline，設計並實作「設計審查」。

### [PAGE SPECIFICATION]

**頁面元資料**：
- 路徑：`/projects/:id/design-review`
- 類型：列表/詳情/審查表單
- 主要目標：針對通過 Pre-CAD Gate 的候選方案，進行 MVP CAD 的初步審查，利用有限的 CAD/模擬成果快速識別潛在的設計缺陷、製造困難或整合問題。
- 次要目標：將「證據缺口」轉化為下一步的最小實驗，並記錄審查過程與結果。

**目標用戶**：
- 主要：RD 主管, RD 工程師, QA 工程師
- 次要：專案經理 (PM), 製造工程師

**進入方式**：
- 從「Pre-CAD 審查頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
- 預估停留時間：長 (20-40 分鐘)

**頁面結構**（由上至下）：

1. **審查方案列表區**
   - 用途：展示通過 Pre-CAD 審查的候選設計方案概覽，供審查團隊選擇。
   - 佈局：響應式列表或卡片佈局，支持查看詳情。
   - 元件：
     - `方案卡片/列表項` (card/list item, required)：顯示方案名稱（最長 100 字元）、簡短描述、操作按鈕 (查看詳情、編輯 DR EM)。
   - 狀態：正常、empty（無審查方案時顯示「沒有審查方案」提示）、loading（方案載入中顯示骨架屏）、error（數據載入失敗）

2. **Design Review Evidence Matrix (DR EM) 編輯區**
   - 用途：供審查團隊填寫和評估每個方案的證據狀態和缺口。
   - 佈局：模態框 (Modal) 或側邊抽屜 (Drawer) 中的表格佈局。
   - 元件：
     - `DR EM 表格` (table, required)：包含類別、要求/規格、目前證據、證據品質、證據缺口、下一步最小實驗、Owner、Due Date 等字段。各字段有相應長度限制。
     - `證據上傳` (file upload, optional)：支持用戶上傳證據文件。
   - 狀態：正常、error（評估項未完成或輸入不符合要求）

3. **風險登錄表編輯區**
   - 用途：記錄與方案相關的風險，包括失效模式、機率、嚴重度、緩解措施。
   - 佈局：模態框 (Modal) 或側邊抽屜 (Drawer) 中的表格佈局。
   - 元件：
     - `風險表格` (table, required)：包含風險 ID、描述、失效模式、機率、嚴重度、等級、緩解措施、監控指標等字段。各字段有相應長度限制。
   - 狀態：正常、error（字段驗證失敗）

4. **審查結論與決策區**
   - 用途：總結審查結果，決定方案去向，並記錄結論。
   - 佈局：底部固定操作欄或獨立區塊。
   - 元件：
     - `方案去向選擇器` (radio button/dropdown, required)：選擇方案的最終去向 (如：批准、修訂、淘汰)。
     - `審查結論備註` (textarea, optional)：記錄審查會議的關鍵討論和決策原因。最長 500 字元。
     - `批准審查按鈕` (button primary, required)：點擊後保存審查結果並推進專案階段。
   - 狀態：正常、disabled（未完成所有評估或未選擇方案去向時按鈕禁用）、loading（提交中顯示 Loading Spinner）

**互動要求**：
1. 用戶進入設計審查頁面，系統載入通過 Pre-CAD 審查的候選方案列表。
2. 用戶點擊某方案，打開 DR EM 和風險登錄表進行詳細評估和記錄。
3. 審查團隊填寫 DR EM 和風險登錄表，識別證據缺口和風險，並規劃最小實驗。
4. 完成所有評估後，選擇方案去向（如：批准、修訂、淘汰），並點擊「批准審查」按鈕，保存審查結果並推進專案階段。

**表單驗證規則**：
- `DR EM`: 所有 DR EM 字段必須填寫 → 所有審查維度必須填寫。
- `風險表格`: 所有風險評估字段必須填寫 → 所有風險評估項為必填。
- `方案去向選擇器`: 必選 → 請選擇一個方案去向。

**資料更新策略**：
- 保存審查結果後，方案列表數據將自動刷新，專案狀態推進。
- DR EM 和風險登錄表數據更新後自動刷新。

**資料處理**：
- API 端點：
  - GET `/api/projects/:id/solutions/reviewed` — 獲取通過 Pre-CAD 審查的方案。
  - POST `/api/projects/:id/design-reviews` — 提交設計審查結果。
  - GET `/api/projects/:id/evidence-matrix` — 獲取 DR EM 數據。
  - GET `/api/projects/:id/risk-register` — 獲取風險登錄表數據。
- 載入策略：漸進式載入 (Skeleton Screen)，關鍵數據優先。
- 錯誤處理：
  - 獲取方案或審查數據失敗：頁面顯示錯誤提示訊息，提供重試按鈕。
  - 提交審查結果失敗：顯示提交失敗提示，並提供重新提交選項。

**RWD 行為差異**：
- Desktop (>1024px)：審查方案列表和 DR EM/風險登錄表可並排顯示，提升審查效率。
- Tablet (768px - 1023px)：佈局堆疊，DR EM 和風險登錄表可能以全屏顯示。
- Mobile (<768px)：列表卡片化，DR EM 和風險登錄表以全屏模態框顯示。

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
