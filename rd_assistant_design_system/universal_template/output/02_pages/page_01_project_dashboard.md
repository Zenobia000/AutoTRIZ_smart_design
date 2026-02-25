# Page-Level Prompt: 專案儀表板

## [PAGE META]
- **page_name**: 專案儀表板
- **route_path**: `/projects/:id`
- **page_type**: 儀表板/詳情頁
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 總覽單一專案的進度、關鍵數據、決策記錄，並提供導航到各階段任務的入口。
- **secondary_goal**: 讓用戶快速了解專案狀態，並方便進行下一步操作。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師, 專案經理 (PM), RD 主管
  - 次要：N/A
- **entry_point**:
  - 從「專案列表」頁面點擊特定專案進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 中 (3-10 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **專案概覽區**
   - section_type: summary/card
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 顯示專案名稱、狀態、創建日期、負責人等基本信息，以及核心 KPI 概覽。

2. **專案進度與決策歷程區**
   - section_type: timeline/list
   - section_purpose: 以時間線或列表形式展示專案各階段任務的完成情況和關鍵決策點。

3. **階段任務導航區**
   - section_type: navigation/menu
   - section_purpose: 提供快速導航到專案各階段（任務定義、假設台帳等）的入口。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 專案概覽區
- **layout**: 頂部多欄佈局，響應式調整。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `專案名稱`: `text (h1)`, `required`, `顯示專案全名。`
  - `專案狀態標籤`: `badge`, `required`, `顯示專案當前狀態 (如進行中、已完成)。`
  - `核心KPI卡片`: `card`, `required`, `顯示 Mission、Hard Constraints 摘要，以及 Critical KPIs 的進度。`
- **states**:
  - 正常：所有信息正常顯示。
  - loading：顯示骨架屏。
  - empty：無專案數據時顯示提示。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 專案名稱: 最長 100 個字元。

### Section: 專案進度與決策歷程區
- **layout**: 時間線或列表佈局。
- **elements**:
  - `歷程項`: `list item`, `required`, `顯示每個決策點或任務完成的日期、摘要、負責人。`
  - `查看詳情按鈕`: `button (secondary)`, `optional`, `點擊後導航至該決策的詳細記錄頁。`
- **states**:
  - 正常：歷程信息正常顯示。
  - empty：無歷程記錄時顯示提示。
- **copy_constraints**:
  - 摘要: 最長 150 個字元。

### Section: 階段任務導航區
- **layout**: 側邊欄或底部導航，列表形式。
- **elements**:
  - `任務連結`: `link`, `required`, `點擊後導航至對應的專案階段頁面 (任務定義、假設台帳等)。`
- **states**:
  - 正常：連結正常顯示。
  - active：當前頁面連結高亮。
- **copy_constraints**:
  - 任務名稱: 清晰明了。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入專案儀表板，系統載入並顯示專案詳細數據和進度。
  2. 用戶點擊「階段任務導航」中的連結，導航至對應的專案階段頁面。
  3. 用戶點擊進度歷程中的「查看詳情」按鈕，導航至決策記錄詳情頁。

- **表單驗證規則**（如適用）：
  - `專案ID`: 必須為有效的 GUID/UUID 格式 → 專案ID無效，請檢查URL。

- **資料更新策略**：
  - 頁面載入時獲取最新數據，專案數據更新後自動刷新。
  - 透過 WebSocket 或 Polling 實現數據的即時更新（如適用）。

- **RWD 行為差異**：
  - Desktop (>1024px): 完整顯示所有區塊，布局寬敞，導航固定於側邊。
  - Tablet (768px - 1023px): 概覽區塊佈局調整為堆疊，進度歷程區可能簡化為卡片，導航區可能轉換為抽屜式導航。
  - Mobile (<768px): 所有區塊垂直堆疊，導航區轉換為底部導航或抽屜式導航，確保最小寬度下的可用性。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id` — 獲取單一專案的詳細信息。
  - GET `/api/projects/:id/progress` — 獲取專案進度概覽數據。
  - GET `/api/projects/:id/history` — 獲取專案的決策和任務歷程數據。
- **error cases**:
  - API 載入失敗: 頁面顯示錯誤提示，並提供返回專案列表的按鈕。
  - 專案 ID 不存在: 顯示「專案不存在」提示，並引導返回專案列表。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 專案概覽信息（名稱、狀態、KPI）正確顯示。
- [x] 專案進度與決策歷程能清晰展示，且每個歷程項可查看詳情。
- [x] 各階段任務導航連結功能正常，可正確跳轉至對應階段頁面。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
