# Page-Level Prompt: 方案探索

## [PAGE META]
- **page_name**: 方案探索
- **route_path**: `/projects/:id/solution-explorer`
- **page_type**: 列表/詳情/工具
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 協助用戶基於已識別的矛盾，生成、篩選和評估多個設計方案。
- **secondary_goal**: 記錄方案的機制、假設、風險、最小驗證，並進行 MUST 快篩。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管
- **entry_point**:
  - 從「矛盾識別頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (20-40 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **矛盾選擇與方案生成區**
   - section_type: form/action
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 選擇矛盾作為輸入，觸發 AI 生成初始方案集。

2. **方案列表與篩選區**
   - section_type: list/filter
   - section_purpose: 展示 AI 生成的方案集，支持查看詳情和 MUST 快篩。

3. **方案詳情與編輯區**
   - section_type: detail/form
   - section_purpose: 顯示單一方案的詳細信息，並允許用戶編輯、添加更多細節。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 矛盾選擇與方案生成區
- **layout**: 頂部操作區，包含下拉選單和按鈕。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `矛盾選擇器`: `dropdown`, `required`, `從該專案已識別的矛盾中選擇一個或多個。`
  - `生成方案按鈕`: `button (primary)`, `required`, `點擊後觸發 AI 生成方案。`
- **states**:
  - 正常：下拉選單可用，按鈕可點擊。
  - loading：生成方案中，按鈕禁用並顯示 Loading Spinner。
  - error：選擇矛盾失敗或生成方案失敗時顯示錯誤提示。
- **copy_constraints**:
  - 矛盾選擇器: 必須選擇至少一個矛盾。

### Section: 方案列表與篩選區
- **layout**: 響應式卡片或表格佈局，支持查看詳情和篩選。
- **elements**:
  - `方案卡片/列表項`: `card/list item`, `required`, `顯示方案名稱、簡短描述、MUST 快篩結果 (以標籤或圖標表示)、操作按鈕 (查看詳情)。`
  - `MUST 快篩標籤/篩選器`: `tag/filter`, `optional`, `顯示方案是否通過各項 MUST 快篩，支持按 MUST 條件篩選。`
- **states**:
  - 正常：方案列表正常顯示。
  - empty：無方案時顯示「沒有方案」提示。
  - loading：方案數據載入中顯示骨架屏。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 方案名稱: 最長 100 個字元。
  - 簡短描述: 最長 200 個字元。

### Section: 方案詳情與編輯區
- **layout**: 側邊抽屜 (Drawer) 或模態框 (Modal) 中的詳情佈局。
- **elements**:
  - `方案名稱`: `input (text)`, `required`, `顯示/編輯方案名稱。`
  - `機制說明`: `textarea`, `required`, `詳細描述方案的物理原理和結構。`
  - `假設清單`: `list`, `required`, `顯示方案基於的假設，可連結到假設台帳，支持編輯。`
  - `風險評估`: `table`, `required`, `顯示方案引入的新風險和評估，支持編輯。`
  - `最小驗證`: `textarea`, `required`, `描述驗證此方案所需的最小實驗。`
  - `MUST 快篩結果`: `checklist/badges`, `required`, `顯示此方案通過/未通過的 MUST 條件，可交互。`
  - `保存/取消按鈕`: `button group`, `required`, `保存編輯或取消操作。`
- **states**:
  - 正常：詳情信息正常顯示。
  - loading：數據保存中顯示 Loading Spinner。
  - error：驗證失敗或保存失敗時顯示錯誤提示。
- **copy_constraints**:
  - 各字段有相應長度限制，假設清單、風險評估、最小驗證支持多項輸入。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入方案探索頁面，系統載入已生成的方案列表（如有）。
  2. 用戶從下拉選單中選擇一個或多個矛盾，點擊「生成方案」按鈕，觸發 AI 根據選擇的矛盾和知識庫生成一系列初步設計方案。
  3. AI 生成的方案顯示在列表中，用戶可點擊方案卡片/列表項查看詳細信息，並在詳情區進行編輯。
  4. 方案會自動進行 MUST 快篩，篩選結果即時顯示在卡片/列表項上。用戶可根據篩選結果決定是否進一步編輯或淘汰方案。

- **表單驗證規則**（如適用）：
  - `方案名稱`: 必填，最少 5 字元 → 方案名稱為必填項，且需至少 5 個字元。
  - `機制說明`: 必填，最少 50 字元 → 機制說明為必填項，且需至少 50 個字元。

- **資料更新策略**：
  - AI 生成新方案後，方案列表自動刷新。
  - 用戶編輯方案並保存後，該方案的詳細信息自動刷新。

- **RWD 行為差異**：
  - Desktop (>1024px): 矛盾選擇與生成區、方案列表可並排顯示，方案詳情以側邊抽屜形式展示。
  - Tablet (768px - 1023px): 佈局調整為堆疊，方案列表可能簡化顯示，方案詳情以模態框形式展示。
  - Mobile (<768px): 所有區塊垂直堆疊，方案列表卡片式顯示，方案詳情為全屏模態框。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/contradictions` — 獲取指定專案的矛盾列表，用於矛盾選擇器。
  - POST `/api/projects/:id/solutions/generate` — 根據選定的矛盾觸發 AI 生成方案。
  - GET `/api/projects/:id/solutions` — 獲取指定專案的方案列表。
  - PUT `/api/projects/:id/solutions/:solution_id` — 更新方案信息。
- **error cases**:
  - AI 生成失敗: 顯示 AI 處理失敗提示，建議用戶重新嘗試或調整輸入。
  - MUST 快篩服務失敗: 顯示快篩失敗提示，或標記方案為「待手動審核」。
  - 方案數據載入失敗: 頁面顯示錯誤提示訊息，提供重試按鈕。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 能夠選擇矛盾並成功觸發 AI 生成方案，並將結果顯示在列表中。
- [x] 方案列表能清晰展示方案名稱、MUST 快篩結果等關鍵信息，並支持查看詳情。
- [x] 方案詳情能完整記錄所有必要信息（機制、假設、風險、最小驗證），並支持編輯和保存。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
