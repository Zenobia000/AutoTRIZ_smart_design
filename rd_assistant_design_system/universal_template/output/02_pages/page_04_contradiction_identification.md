# Page-Level Prompt: 矛盾識別

## [PAGE META]
- **page_name**: 矛盾識別
- **route_path**: `/projects/:id/contradiction-identification`
- **page_type**: 表單/列表
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 協助用戶將口語化的工程問題形式化為 TRIZ 矛盾句，為後續的 TRIZ 分析做準備。
- **secondary_goal**: 管理已識別的矛盾，並提供編輯功能。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管
- **entry_point**:
  - 從「假設台帳頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 中 (10-15 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **矛盾輸入區**
   - section_type: form
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 讓用戶輸入或 AI 輔助生成矛盾的自然語言描述，並將其轉化為 TRIZ 矛盾句。

2. **矛盾列表展示區**
   - section_type: table/list
   - section_purpose: 展示已識別的 TRIZ 矛盾列表。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 矛盾輸入區
- **layout**: 單欄響應式表單佈局，各輸入框垂直排列，底部為操作按鈕組。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `矛盾自然語言描述`: `textarea`, `required`, `用戶輸入原始的工程問題描述。`
  - `AI 轉化按鈕`: `button`, `optional`, `點擊後 AI 嘗試將描述轉化為 TRIZ 矛盾句。`
  - `改善參數`: `dropdown/input`, `required`, `從 TRIZ 39 參數中選擇。`
  - `惡化參數`: `dropdown/input`, `required`, `從 TRIZ 39 參數中選擇。`
  - `工程表述`: `textarea`, `required`, `當 X 改善時，Y 惡化。`
  - `物理矛盾`: `textarea`, `optional`, `同一物件需要同時具備屬性 A 和非屬性 A。`
  - `新增矛盾按鈕`: `button (primary)`, `required`, `將完成的 TRIZ 矛盾添加到列表中。`
- **states**:
  - 正常：所有輸入框為空或已填寫。
  - loading：AI 轉化中顯示 Loading Spinner，按鈕禁用。
  - error：輸入驗證失敗或 AI 轉化失敗時顯示錯誤提示。
- **copy_constraints**:
  - 矛盾自然語言描述: 最少 10 個字元，最多 500 字元。
  - 改善參數/惡化參數: 必須從預設列表中選擇。
  - 工程表述: 最少 20 個字元，最多 300 字元。

### Section: 矛盾列表展示區
- **layout**: 響應式表格佈局，支持編輯、刪除操作。
- **elements**:
  - `矛盾表格`: `table`, `required`, `顯示矛盾編號、改善參數、惡化參數、工程表述、物理矛盾、操作按鈕 (編輯/刪除)。`
- **states**:
  - 正常：矛盾列表正常顯示。
  - empty：無矛盾時顯示「沒有矛盾」提示。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 表格內容清晰顯示，支持文本截斷和懸停顯示完整內容。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入矛盾識別頁面，系統載入該專案已識別的矛盾列表。
  2. 用戶在矛盾輸入區輸入自然語言描述，可點擊「AI 轉化」按鈕獲取建議的 TRIZ 矛盾句。
  3. 用戶填寫或調整 TRIZ 矛盾句的各字段，點擊「新增矛盾」按鈕將完成的矛盾添加到列表中。
  4. 用戶可對列表中現有的矛盾進行編輯或刪除。

- **表單驗證規則**（如適用）：
  - `改善參數`: 必填，且必須從 TRIZ 39 參數列表中選擇 → 改善參數為必填項，且必須從 TRIZ 39 參數中選擇。
  - `惡化參數`: 必填，且必須從 TRIZ 39 參數列表中選擇 → 惡化參數為必填項，且必須從 TRIZ 39 參數中選擇。
  - `工程表述`: 必填，最少 20 字元 → 工程表述為必填項，且需至少 20 個字元。

- **資料更新策略**：
  - 新增、編輯或刪除矛盾後，矛盾列表數據將自動刷新。

- **RWD 行為差異**：
  - Desktop (>1024px): 矛盾輸入區和列表區可並排顯示，提供完整的操作體驗。
  - Tablet (768px - 1023px): 矛盾輸入區和列表區可能堆疊顯示，列表可能簡化為關鍵信息。
  - Mobile (<768px): 輸入區和列表區垂直堆疊，列表轉換為卡片式顯示，編輯操作可能通過 Modal 進行。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/contradictions` — 獲取指定專案的矛盾列表。
  - POST `/api/projects/:id/contradictions` — 創建新矛盾。
  - PUT `/api/projects/:id/contradictions/:contradiction_id` — 更新矛盾信息。
  - GET `/api/triz/parameters` — 獲取 TRIZ 39 參數列表供下拉選單使用。
- **error cases**:
  - API 載入或提交失敗: 頁面顯示錯誤提示訊息，提供重試按鈕。
  - TRIZ 39 參數獲取失敗: 下拉選單禁用，顯示錯誤提示。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 矛盾列表能正確顯示所有矛盾，包含 TRIZ 形式化描述。
- [x] 能順利新增、編輯、刪除矛盾，並保存其詳細信息。
- [x] 「AI 轉化」功能正常，可提供合理的 TRIZ 矛盾建議。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
