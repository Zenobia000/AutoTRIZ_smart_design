# Assembly Prompt — 矛盾識別

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

本次任務：根據上方 Global Guideline，設計並實作「矛盾識別」。

### [PAGE SPECIFICATION]

**頁面元資料**：
- 路徑：`/projects/:id/contradiction-identification`
- 類型：表單/列表
- 主要目標：協助用戶將口語化的工程問題形式化為 TRIZ 矛盾句，為後續的 TRIZ 分析做準備。
- 次要目標：管理已識別的矛盾，並提供編輯功能。

**目標用戶**：
- 主要：RD 工程師
- 次要：RD 主管

**進入方式**：
- 從「假設台帳頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
- 預估停留時間：中 (10-15 分鐘)

**頁面結構**（由上至下）：

1. **矛盾輸入區**
   - 用途：讓用戶輸入或 AI 輔助生成矛盾的自然語言描述，並將其轉化為 TRIZ 矛盾句。
   - 佈局：單欄響應式表單佈局，各輸入框垂直排列，底部為操作按鈕組。
   - 元件：
     - `矛盾自然語言描述` (textarea, required)：用戶輸入原始的工程問題描述。最少 10 字元，最多 500 字元。
     - `AI 轉化按鈕` (button, optional)：點擊後 AI 嘗試將描述轉化為 TRIZ 矛盾句。
     - `改善參數` (dropdown/input, required)：從 TRIZ 39 參數中選擇。必須從預設列表中選擇。
     - `惡化參數` (dropdown/input, required)：從 TRIZ 39 參數中選擇。必須從預設列表中選擇。
     - `工程表述` (textarea, required)：當 X 改善時，Y 惡化。最少 20 字元，最多 300 字元。
     - `物理矛盾` (textarea, optional)：同一物件需要同時具備屬性 A 和非屬性 A。
     - `新增矛盾按鈕` (button primary, required)：將完成的 TRIZ 矛盾添加到列表中。
   - 狀態：正常（所有輸入框為空或已填寫）、loading（AI 轉化中顯示 Loading Spinner，按鈕禁用）、error（輸入驗證失敗或 AI 轉化失敗時顯示錯誤提示）

2. **矛盾列表展示區**
   - 用途：展示已識別的 TRIZ 矛盾列表。
   - 佈局：響應式表格佈局，支持編輯、刪除操作。
   - 元件：
     - `矛盾表格` (table, required)：顯示矛盾編號、改善參數、惡化參數、工程表述、物理矛盾、操作按鈕 (編輯/刪除)。支持文本截斷和懸停顯示完整內容。
   - 狀態：正常、empty（無矛盾時顯示「沒有矛盾」提示）、error（數據載入失敗）

**互動要求**：
1. 用戶進入矛盾識別頁面，系統載入該專案已識別的矛盾列表。
2. 用戶在矛盾輸入區輸入自然語言描述，可點擊「AI 轉化」按鈕獲取建議的 TRIZ 矛盾句。
3. 用戶填寫或調整 TRIZ 矛盾句的各字段，點擊「新增矛盾」按鈕將完成的矛盾添加到列表中。
4. 用戶可對列表中現有的矛盾進行編輯或刪除。

**表單驗證規則**：
- `改善參數`: 必填，且必須從 TRIZ 39 參數列表中選擇 → 改善參數為必填項，且必須從 TRIZ 39 參數中選擇。
- `惡化參數`: 必填，且必須從 TRIZ 39 參數列表中選擇 → 惡化參數為必填項，且必須從 TRIZ 39 參數中選擇。
- `工程表述`: 必填，最少 20 字元 → 工程表述為必填項，且需至少 20 個字元。

**資料更新策略**：
- 新增、編輯或刪除矛盾後，矛盾列表數據將自動刷新。

**資料處理**：
- API 端點：
  - GET `/api/projects/:id/contradictions` — 獲取指定專案的矛盾列表。
  - POST `/api/projects/:id/contradictions` — 創建新矛盾。
  - PUT `/api/projects/:id/contradictions/:contradiction_id` — 更新矛盾信息。
  - GET `/api/triz/parameters` — 獲取 TRIZ 39 參數列表供下拉選單使用。
- 載入策略：漸進式載入 (Skeleton Screen)，關鍵數據優先。
- 錯誤處理：
  - API 載入或提交失敗：頁面顯示錯誤提示訊息，提供重試按鈕。
  - TRIZ 39 參數獲取失敗：下拉選單禁用，顯示錯誤提示。

**RWD 行為差異**：
- Desktop (>1024px)：矛盾輸入區和列表區可並排顯示，提供完整的操作體驗。
- Tablet (768px - 1023px)：矛盾輸入區和列表區可能堆疊顯示，列表可能簡化為關鍵信息。
- Mobile (<768px)：輸入區和列表區垂直堆疊，列表轉換為卡片式顯示，編輯操作可能通過 Modal 進行。

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
