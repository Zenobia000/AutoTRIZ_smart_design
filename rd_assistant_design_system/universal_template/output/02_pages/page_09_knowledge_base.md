# Page-Level Prompt: 知識庫

## [PAGE META]
- **page_name**: 知識庫
- **route_path**: `/knowledge-base`
- **page_type**: 列表/詳情
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 讓用戶瀏覽、搜尋和學習專案相關的知識資產（例如 Playbook、歷史案例、決策模板）。
- **secondary_goal**: 促進知識沉澱和復用，提升團隊協作效率。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師, RD 主管, 專案經理 (PM)
  - 次要：QA 工程師, 製造工程師
- **entry_point**:
  - 從導航菜單或專案儀表板中的相關連結進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (5-30 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **知識庫搜尋與分類區**
   - section_type: form/filter
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 提供知識內容的搜尋、篩選和分類功能。

2. **知識列表展示區**
   - section_type: list/grid
   - section_purpose: 展示知識文章、模板或案例的列表。

3. **知識詳情展示區**
   - section_type: detail/content
   - section_purpose: 顯示單一知識條目的詳細內容。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 知識庫搜尋與分類區
- **layout**: 頂部操作區，包含搜尋框、分類篩選器。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `搜尋框`: `input (text)`, `optional`, `根據關鍵字搜尋知識內容。`
  - `分類篩選器`: `dropdown/checkbox group`, `optional`, `按知識類型 (Playbook, 案例, 模板) 或標籤進行篩選。`
- **states**:
  - 正常：搜尋框和篩選器可用。
  - loading：搜尋中顯示 Loading Spinner。
  - error：搜尋失敗時顯示錯誤提示。
- **copy_constraints**:
  - 搜尋框: 最少 1 個字元，最多 100 個字元。

### Section: 知識列表展示區
- **layout**: 響應式列表或網格佈局，支持分頁。
- **elements**:
  - `知識卡片/列表項`: `card/list item`, `required`, `顯示知識標題、簡短描述、所屬類別、發布日期。`
  - `分頁器/載入更多按鈕`: `pagination/button`, `optional`, `當知識數量較多時提供分頁功能。`
- **states**:
  - 正常：知識列表正常顯示。
  - empty：無知識時顯示「沒有知識」提示。
  - loading：知識載入中顯示骨架屏。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 標題: 最長 100 個字元。
  - 描述: 最長 200 個字元。

### Section: 知識詳情展示區
- **layout**: 單欄內容佈局，支持 Markdown 渲染。
- **elements**:
  - `文章標題`: `text (h1)`, `required`, `顯示知識文章的完整標題。`
  - `文章內容`: `richtext/markdown-viewer`, `required`, `顯示知識文章的詳細內容。`
  - `相關文檔連結`: `list of links`, `optional`, `鏈接到相關的決策記錄、假設台帳等。`
- **states**:
  - 正常：內容正常顯示。
  - loading：內容載入中顯示骨架屏。
  - error：內容載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 內容渲染清晰，支持代碼高亮、圖片顯示。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入知識庫頁面，系統載入並顯示知識列表。
  2. 用戶可使用搜尋框或分類篩選器查找特定知識，知識列表將即時更新。
  3. 用戶點擊知識卡片/列表項，導航至該知識的詳情頁面。
  4. 在詳情頁面，用戶可瀏覽知識內容，並點擊相關文檔連結，返回列表頁面可保留搜尋/篩選狀態。

- **表單驗證規則**（如適用）：
  - `搜尋關鍵字`: 必填，最少 1 字元 → 搜尋關鍵字不能為空。

- **資料更新策略**：
  - 搜尋或篩選後，知識列表數據將自動刷新。
  - 知識內容更新後，詳情頁面數據將自動刷新。

- **RWD 行為差異**：
  - Desktop (>1024px): 搜尋與分類區、知識列表可並排顯示，知識詳情頁面為獨立頁面。
  - Tablet (768px - 1023px): 佈局調整為堆疊，知識列表可能簡化顯示，詳情頁面全屏顯示。
  - Mobile (<768px): 所有區塊垂直堆疊，知識列表卡片式顯示，詳情頁面全屏。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/knowledge-base` — 獲取知識庫列表，支持搜尋、篩選參數。
  - GET `/api/knowledge-base/:category/:slug` — 獲取單一知識詳情。
- **error cases**:
  - API 載入失敗: 頁面顯示錯誤提示訊息，提供重試按鈕。
  - 知識條目不存在: 顯示「知識不存在」提示，並引導返回知識列表。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 知識列表能正確顯示，支持搜尋和分類篩選功能。
- [x] 知識詳情頁面能完整展示內容，並支持 Markdown 渲染。
- [x] 相關文檔連結功能正常，可跳轉至鏈接資源。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
