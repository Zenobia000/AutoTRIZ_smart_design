# Page-Level Prompt: 設計審查

## [PAGE META]
- **page_name**: 設計審查
- **route_path**: `/projects/:id/design-review`
- **page_type**: 列表/詳情/審查表單
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 針對通過 Pre-CAD Gate 的候選方案，進行 MVP CAD 的初步審查，利用有限的 CAD/模擬成果快速識別潛在的設計缺陷、製造困難或整合問題。
- **secondary_goal**: 將「證據缺口」轉化為下一步的最小實驗，並記錄審查過程與結果。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 主管, RD 工程師, QA 工程師
  - 次要：專案經理 (PM), 製造工程師
- **entry_point**:
  - 從「Pre-CAD 審查頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (20-40 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **審查方案列表區**
   - section_type: list/table
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 展示通過 Pre-CAD 審查的候選設計方案概覽，供審查團隊選擇。

2. **Design Review Evidence Matrix (DR EM) 編輯區**
   - section_type: form/table
   - section_purpose: 供審查團隊填寫和評估每個方案的證據狀態和缺口。

3. **風險登錄表編輯區**
   - section_type: form/table
   - section_purpose: 記錄與方案相關的風險，包括失效模式、機率、嚴重度、緩解措施。

4. **審查結論與決策區**
   - section_type: summary/action
   - section_purpose: 總結審查結果，決定方案去向，並記錄結論。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 審查方案列表區
- **layout**: 響應式列表或卡片佈局，支持查看詳情。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `方案卡片/列表項`: `card/list item`, `required`, `顯示方案名稱、簡短描述、操作按鈕 (查看詳情、編輯 DR EM)。`
- **states**:
  - 正常：方案列表正常顯示。
  - empty：無審查方案時顯示「沒有審查方案」提示。
  - loading：方案載入中顯示骨架屏。
  - error：數據載入失敗時顯示錯誤提示。
- **copy_constraints**:
  - 方案名稱: 最長 100 個字元。

### Section: Design Review Evidence Matrix (DR EM) 編輯區
- **layout**: 模態框 (Modal) 或側邊抽屜 (Drawer) 中的表格佈局。
- **elements**:
  - `DR EM 表格`: `table`, `required`, `包含類別、要求/規格、目前證據、證據品質、證據缺口、下一步最小實驗、Owner、Due Date 等字段。`
  - `證據上傳`: `file upload`, `optional`, `支持用戶上傳證據文件。`
- **states**:
  - 正常：表單可用。
  - error：評估項未完成或輸入不符合要求時顯示錯誤提示。
- **copy_constraints**:
  - 各字段有相應長度限制。

### Section: 風險登錄表編輯區
- **layout**: 模態框 (Modal) 或側邊抽屜 (Drawer) 中的表格佈局。
- **elements**:
  - `風險表格`: `table`, `required`, `包含風險 ID、描述、失效模式、機率、嚴重度、等級、緩解措施、監控指標等字段。`
- **states**:
  - 正常：表格正常顯示。
  - error：字段驗證失敗時顯示錯誤提示。
- **copy_constraints**:
  - 各字段有相應長度限制。

### Section: 審查結論與決策區
- **layout**: 底部固定操作欄或獨立區塊。
- **elements**:
  - `方案去向選擇器`: `radio button/dropdown`, `required`, `選擇方案的最終去向 (如：批准、修訂、淘汰)。`
  - `審查結論備註`: `textarea`, `optional`, `記錄審查會議的關鍵討論和決策原因。`
  - `批准審查按鈕`: `button (primary)`, `required`, `點擊後保存審查結果並推進專案階段。`
- **states**:
  - 正常：按鈕可用。
  - disabled：未完成所有評估或未選擇方案去向時按鈕禁用。
  - loading：提交中顯示 Loading Spinner。
- **copy_constraints**:
  - 備註: 最長 500 個字元。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入設計審查頁面，系統載入通過 Pre-CAD 審查的候選方案列表。
  2. 用戶點擊某方案，打開 DR EM 和風險登錄表進行詳細評估和記錄。
  3. 審查團隊填寫 DR EM 和風險登錄表，識別證據缺口和風險，並規劃最小實驗。
  4. 完成所有評估後，選擇方案去向（如：批准、修訂、淘汰），並點擊「批准審查」按鈕，保存審查結果並推進專案階段。

- **表單驗證規則**（如適用）：
  - `DR EM`: 所有 DR EM 字段必須填寫 → 所有審查維度必須填寫。
  - `風險表格`: 所有風險評估字段必須填寫 → 所有風險評估項為必填。
  - `方案去向選擇器`: 必選 → 請選擇一個方案去向。

- **資料更新策略**：
  - 保存審查結果後，方案列表數據將自動刷新，專案狀態推進。
  - DR EM 和風險登錄表數據更新後自動刷新。

- **RWD 行為差異**：
  - Desktop (>1024px): 審查方案列表和 DR EM/風險登錄表可並排顯示，提升審查效率。
  - Tablet (768px - 1023px): 佈局堆疊，DR EM 和風險登錄表可能以全屏顯示。
  - Mobile (<768px): 列表卡片化，DR EM 和風險登錄表以全屏模態框顯示。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/solutions/reviewed` — 獲取通過 Pre-CAD 審查的方案。
  - POST `/api/projects/:id/design-reviews` — 提交設計審查結果。
  - GET `/api/projects/:id/evidence-matrix` — 獲取 DR EM 數據。
  - GET `/api/projects/:id/risk-register` — 獲取風險登錄表數據。
- **error cases**:
  - 獲取方案或審查數據失敗: 頁面顯示錯誤提示訊息，提供重試按鈕。
  - 提交審查結果失敗: 顯示提交失敗提示，並提供重新提交選項。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 審查方案列表能正確顯示，且能選擇方案進行審查。
- [x] DR EM 和風險登錄表能完整記錄評估結果、證據缺口、緩解措施。
- [x] 能選擇方案去向並成功提交審查結果，專案狀態正確推進。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
