# Page-Level Prompt: 假設台帳

## [PAGE META]
- **page_name**: 假設台帳
- **route_path**: `/projects/:id/assumption-ledger`
- **page_type**: 列表/表單
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 管理專案設計過程中的所有假設，追蹤其驗證狀態和潛在影響。
- **secondary_goal**: 提供假設的詳細信息，並支持假設的編輯、驗證規劃。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師, RD 主管
  - 次要：專案經理 (PM)
- **entry_point**:
  - 從「任務定義頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (10-20 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **假設列表展示區**
   - section_type: table/list
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 以表格形式展示所有假設，包含編號、內容、依據來源、驗證狀態等。

2. **假設詳情編輯區**
   - section_type: form/detail
   - section_purpose: 顯示單一假設的詳細信息，並提供編輯、規劃驗證的表單。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 假設列表展示區
- **layout**: 響應式表格佈局，支持排序和分頁。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `假設表格`: `table`, `required`, `每列顯示假設編號、內容、依據來源、若錯了最壞後果、最小驗證方法、驗證成本/週期、狀態、操作按鈕。`
  - `新增假設按鈕`: `button (primary)`, `required`, `點擊後打開假設詳情編輯區以新增假設。`
- **states**:
  - 正常：假設列表正常顯示。
  - loading：顯示骨架屏。
  - empty：無假設時顯示「沒有假設」提示。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 假設內容: 最長 300 個字元。

### Section: 假設詳情編輯區
- **layout**: 模態框 (Modal) 或側邊抽屜 (Drawer) 中的表單佈局。
- **elements**:
  - `假設內容`: `textarea`, `required`, `輸入/顯示假設的詳細描述。`
  - `依據來源`: `input (text)`, `required`, `輸入假設的依據文獻或來源 ID。`
  - `若錯了最壞後果`: `textarea`, `required`, `輸入若假設錯誤可能導致的最壞結果。`
  - `最小驗證方法`: `textarea`, `required`, `描述驗證該假設所需的最小實驗方法。`
  - `驗證成本/週期`: `input (text)`, `required`, `輸入預估的驗證成本和週期。`
  - `保存/取消按鈕`: `button group`, `required`, `保存編輯或取消操作。`
- **states**:
  - 正常：表單可用。
  - loading：提交中顯示 Loading Spinner。
  - error：驗證失敗時顯示錯誤提示。
- **copy_constraints**:
  - 所有字段皆為必填，且有相應的長度限制。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入假設台帳頁面，系統載入並顯示該專案的所有假設列表。
  2. 用戶可點擊「新增假設」按鈕或表格中的「編輯」按鈕，打開假設詳情編輯區。
  3. 用戶在編輯區填寫/修改假設信息，點擊「保存」提交。提交成功後關閉編輯區並刷新列表。
  4. 用戶可更新假設的驗證狀態 (例如：待驗證、驗證中、已驗證、已推翻)。

- **表單驗證規則**（如適用）：
  - `假設內容`: 必填，最少 10 字元 → 假設內容為必填項，且需至少 10 個字元。
  - `依據來源`: 必填 → 依據來源為必填項。
  - `驗證成本/週期`: 必填，且需為有效數值或描述 → 驗證成本/週期格式不正確。

- **資料更新策略**：
  - 新增/編輯假設後，列表數據將自動刷新。
  - 假設狀態更新後，列表數據將自動刷新。

- **RWD 行為差異**：
  - Desktop (>1024px): 表格和詳情編輯區可並排顯示，或編輯區以模態框形式展示。
  - Tablet (768px - 1023px): 表格列可能壓縮，詳情編輯區以全屏模態框或側邊抽屜形式顯示。
  - Mobile (<768px): 表格轉換為列表卡片式顯示，詳情編輯區為全屏模態框。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/assumptions` — 獲取指定專案的假設列表。
  - POST `/api/projects/:id/assumptions` — 創建新假設。
  - PUT `/api/projects/:id/assumptions/:assumption_id` — 更新假設信息。
- **error cases**:
  - API 載入或提交失敗: 頁面顯示錯誤提示訊息，提供重試按鈕。
  - 假設列表為空: 顯示「沒有假設」提示，並引導新增假設。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 假設列表能正確顯示所有假設，包含詳細屬性（內容、依據來源、最壞後果、最小驗證方法、驗證成本/週期、狀態）。
- [x] 能順利新增、編輯假設，並保存其詳細信息。
- [x] 假設的驗證狀態可更新，並反映在列表中。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
