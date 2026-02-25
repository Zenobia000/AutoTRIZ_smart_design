# Page-Level Prompt: 任務定義頁面

## [PAGE META]
- **page_name**: 任務定義頁面
- **route_path**: `/projects/:id/task-definition`
- **page_type**: 功能/表單
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 協助用戶結構化地定義新專案的需求、約束與目標。
- **secondary_goal**: 識別關鍵 KPI，為後續決策提供依據。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管, 專案經理 (PM)
- **entry_point**:
  - 從「專案儀表板」點擊「定義任務」按鈕進入，或從專案創建後的導引流程進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 中 (5-15 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **任務定義表單區塊**
   - section_type: form
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 讓用戶輸入專案的核心使命、硬約束、軟目標和非目標，並定義關鍵衡量指標。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 任務定義表單區塊
- **layout**: 單欄響應式表單佈局，各輸入框垂直排列，底部為操作按鈕組。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `Mission (核心使命)`: `textarea`, `required`, `輸入專案的核心使命與目標，支持多行輸入。`
  - `Hard Constraints (硬約束)`: `textarea`, `optional`, `輸入專案必須遵守的不可妥協的限制，如成本上限、尺寸限制、法規要求。`
  - `Soft Objectives (軟目標)`: `textarea`, `optional`, `輸入專案希望達成但可權衡的目標，如效能提升、重量輕量化、噪音降低。`
  - `Non-Goals (非目標)`: `textarea`, `optional`, `明確定義本版專案不追求的功能或範圍，以避免範圍蔓延。`
  - `三個最不能失敗指標 (Critical KPIs)`: `kpi-input-list (自定義組件)`, `required`, `可動態新增/刪除關鍵指標，每個指標包含名稱、目標值和衡量方式。`
  - `確認任務定義按鈕`: `button`, `required`, `提交表單內容，保存任務定義並進入下一階段。`
  - `取消按鈕`: `button`, `optional`, `放棄當前操作，返回專案儀表板。`
- **states**:
  - 正常：所有輸入框為空或已填寫。
  - hover：操作按鈕有背景色加深效果或輕微陰影。
  - loading：提交按鈕顯示 Loading Spinner，表單處於禁用狀態，防止重複提交。
  - empty：文本框顯示 Placeholder 提示，引導用戶輸入。
  - error：輸入驗證失敗的字段下方顯示紅色錯誤提示文字，表單按鈕禁用。
- **copy_constraints**:
  - Mission: 最少 10 個字元，最多 500 字元。
  - Hard Constraints / Soft Objectives / Non-Goals: 每條限制最少 5 個字元，最多 200 字元，支持多條輸入。
  - Critical KPIs: 每個指標名稱最少 3 個字元，目標值和衡量方式必填。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入頁面，系統載入專案現有任務定義數據（如有），並顯示在表單中。
  2. 用戶填寫或修改表單內容，系統即時進行前端驗證，並顯示錯誤提示（若有）。
  3. 用戶點擊「確認任務定義」按鈕，數據提交至後端。提交成功後，導航至「假設台帳」頁面；提交失敗則顯示錯誤訊息。

- **表單驗證規則**（如適用）：
  - `Mission`: 必填，最少 10 字元 → 核心使命為必填項，且需至少 10 個字元。
  - `Critical KPIs`: 至少一個 KPI，每個 KPI 需有名稱、目標值和衡量方式 → 請至少定義一個關鍵指標，並確保其名稱、目標值和衡量方式皆已填寫。

- **資料更新策略**：
  - 提交成功後，本地狀態更新，並通過 React Query 或類似機制使相關專案數據重新請求或失效。

- **RWD 行為差異**：
  - Desktop (>1024px): 完整表單顯示，各字段清晰可見，可考慮彈性佈局或輔助信息側邊顯示。
  - Tablet (768px - 1023px): 表單字段可能從多欄佈局變為單欄堆疊，確保在較小螢幕寬度下仍有良好可讀性。
  - Mobile (<768px): 單欄佈局，所有表單元素垂直堆疊，文字大小和間距調整以適應最小支援寬度。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/constraints` — 獲取指定專案的任務定義數據。
  - PUT `/api/projects/:id/constraints` — 更新指定專案的任務定義數據。
- **error cases**:
  - API 數據載入失敗: 頁面顯示錯誤提示訊息，並提供重試按鈕。
  - 表單提交失敗 (例如 400 Bad Request, 422 Unprocessable Entity): 顯示後端返回的字段級錯誤訊息，或彈出通用錯誤提示。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 任務定義表單所有必填欄位可正常填寫與提交。
- [x] 「三個最不能失敗指標」可新增、編輯、刪除，並能設定其判斷方式。
- [x] 提交後數據能正確保存並更新專案狀態，並正確導航至假設台帳頁面。
