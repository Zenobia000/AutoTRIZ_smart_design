# Page-Level Prompt: 專案列表

## [PAGE META]
- **page_name**: 專案列表
- **route_path**: `/projects`
- **page_type**: 列表/儀表板
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 讓用戶快速瀏覽、篩選、管理現有專案，並創建新專案。
- **secondary_goal**: 提供專案概覽信息，支持快速導航至各專案詳情。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師, 專案經理 (PM)
  - 次要：RD 主管
- **entry_point**:
  - 應用啟動後的首頁，或從左側導航菜單點擊「專案」進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 短 (1-3 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **專案篩選與操作區**
   - section_type: filter/action
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 提供搜尋、篩選功能及創建新專案的入口。

2. **專案列表展示區**
   - section_type: list/table
   - section_purpose: 以卡片或列表形式展示專案概覽。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 專案篩選與操作區
- **layout**: 頂部水平佈局，包含搜尋框、篩選器、按鈕。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `搜尋框`: `input (text)`, `optional`, `根據專案名稱、關鍵字進行模糊搜尋。`
  - `篩選器`: `dropdown/checkbox group`, `optional`, `根據專案狀態 (進行中、已完成)、創建者進行篩選。`
  - `新增專案按鈕`: `button (primary)`, `required`, `點擊後導航至創建新專案頁面。`
- **states**:
  - 正常：所有功能可用。
  - hover：按鈕有背景色加深效果。
  - active：篩選器選中狀態。
  - disabled：權限不足時按鈕禁用。
  - empty：無搜尋結果時顯示提示。
  - error：篩選條件無效時顯示錯誤提示。
- **copy_constraints**:
  - 搜尋框: 最少 1 個字元，最多 50 個字元。

### Section: 專案列表展示區
- **layout**: 響應式網格佈局 (卡片) 或表格佈局 (列表)。
- **elements**:
  - `專案卡片/列表項`: `card/list item`, `required`, `顯示專案名稱、簡短描述、進度條、狀態標籤、最後更新時間。`
  - `分頁器/載入更多按鈕`: `pagination/button`, `optional`, `當專案數量較多時提供分頁或無限滾動。`
- **states**:
  - 正常：專案正常顯示。
  - hover：專案卡片陰影抬升，顯示更多操作。
  - empty：列表為空時顯示「沒有專案」的提示。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 專案名稱: 最長 100 個字元。
  - 描述: 最長 200 個字元。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入專案列表頁面，系統載入並顯示現有專案列表。
  2. 用戶可使用搜尋框或篩選器查找特定專案，列表將即時更新。
  3. 用戶點擊專案卡片或列表項，導航至該專案的儀表板。
  4. 用戶點擊「新增專案」按鈕，導航至創建新專案頁面。

- **表單驗證規則**（如適用）：
  - `搜尋關鍵字`: 必填，最少 1 個字元 → 搜尋關鍵字不能為空。

- **資料更新策略**：
  - 搜尋或篩選後，列表數據將自動刷新。
  - 創建、更新或刪除專案後，專案列表將自動刷新以反映最新狀態。

- **RWD 行為差異**：
  - Desktop (>1024px): 完整顯示篩選器和卡片網格，提供寬敞的視覺空間。
  - Tablet (768px - 1023px): 篩選器可能折疊或簡化為一行，卡片網格佈局調整為 2 欄。
  - Mobile (<768px): 篩選器折疊為 Modal 或 Drawer，卡片垂直堆疊顯示，確保最小寬度下的可用性。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects` — 獲取專案列表，支持篩選、排序參數。
  - POST `/api/projects` — 創建新專案 (從創建新專案頁面提交)。
- **error cases**:
  - API 載入失敗: 頁面顯示錯誤提示，提供重試按鈕。
  - 專案列表為空: 顯示「沒有專案」的提示，並引導創建新專案。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 專案列表能正確顯示所有專案信息，包含名稱、狀態、進度等概覽。
- [x] 搜尋和篩選功能正常工作，列表能即時更新顯示符合條件的專案。
- [x] 點擊專案卡片或列表項，可正確導航至該專案的儀表板。
- [x] 「新增專案」按鈕可正確導航至創建新專案頁面。
