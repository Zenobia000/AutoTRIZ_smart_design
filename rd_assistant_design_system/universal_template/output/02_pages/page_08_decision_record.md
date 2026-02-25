# Page-Level Prompt: 決策記錄

## [PAGE META]
- **page_name**: 決策記錄
- **route_path**: `/projects/:id/decision-record`
- **page_type**: 詳情/表單/報告
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 完整記錄設計決策的過程、依據、結論和後續行動，確保決策可追溯和可解釋。
- **secondary_goal**: 提供決策的簽核功能，並支持決策的編輯和匯出。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 主管, 專案經理 (PM)
  - 次要：RD 工程師, QA 工程師, 高階主管
- **entry_point**:
  - 從「設計審查頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 中 (15-20 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **決策概覽區**
   - section_type: summary/card
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 顯示決策聲明、日期、決策者等基本信息，提供決策的快速總覽。

2. **KT 決策分析結果區**
   - section_type: table/report
   - section_purpose: 展示 MUST、WANT、AC 分析結果，並鏈接到相關證據，支持決策的依據。

3. **決策結論與行動區**
   - section_type: summary/form
   - section_purpose: 總結決策的主路線、備援方案和後續行動項目，並提供簽核功能，推進專案執行。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 決策概覽區
- **layout**: 單欄或雙欄佈局，信息清晰分組。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `決策聲明`: `text (h2)`, `required`, `簡潔有力的決策結論。`
  - `決策者`: `text`, `required`, `顯示決策負責人的姓名和角色。`
  - `決策日期`: `date`, `required`, `顯示決策創建日期。`
- **states**:
  - 正常：所有信息正常顯示。
  - empty：無決策數據時顯示提示。
- **copy_constraints**:
  - 決策聲明: 最長 200 個字元。

### Section: KT 決策分析結果區
- **layout**: 多個表格或列表佈局，數據可視化（如雷達圖）輔助。
- **elements**:
  - `MUST 結果表格`: `table`, `required`, `顯示通過和淘汰的方案，及其原因。`
  - `WANT 結果表格`: `table`, `required`, `顯示各方案的 WANT 評分、加權分數和證據連結。`
  - `風險評估表格`: `table`, `required`, `顯示主要風險、等級和緩解措施。`
- **states**:
  - 正常：數據正常顯示。
  - empty：無分析結果時顯示提示。
- **copy_constraints**:
  - 表格數據清晰易讀，支持排序和篩選。

### Section: 決策結論與行動區
- **layout**: 單欄佈局，行動項目列表可展開收起。
- **elements**:
  - `主路線`: `text`, `required`, `顯示最終選定的主方案。`
  - `備援方案`: `text`, `optional`, `顯示備用的方案。`
  - `行動項目列表`: `list/table`, `required`, `記錄所有後續行動，包含任務、負責人、截止日期。`
  - `簽核區`: `signature component`, `required`, `提供決策者和審核者進行電子簽核的功能。`
  - `匯出報告按鈕`: `button (secondary)`, `optional`, `點擊後匯出決策記錄為 PDF/Word 等格式。`
- **states**:
  - 正常：所有功能可用。
  - disabled：決策未完成或未簽核時按鈕禁用。
- **copy_constraints**:
  - 行動項目描述: 最長 100 個字元。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入決策記錄頁面，系統載入該專案的最新決策數據。
  2. 用戶可查看各項決策分析結果和結論，審閱主路線、備援和行動項目。
  3. 決策者和審核者進行電子簽核，標記決策為最終狀態。
  4. 用戶可點擊「匯出報告」按鈕將決策記錄匯出為指定格式。

- **表單驗證規則**（如適用）：
  - `簽核人`: 必填，且必須為有效的用戶 → 決策記錄未完成簽核。

- **資料更新策略**：
  - 決策信息更新後自動刷新。
  - 簽核狀態更新後，頁面顯示相應的簽核狀態。

- **RWD 行為差異**：
  - Desktop (>1024px): 各區塊完整顯示，布局清晰，方便審閱。
  - Tablet (768px - 1023px): 區塊可能堆疊，表格可能橫向滾動或顯示簡化視圖。
  - Mobile (<768px): 所有區塊垂直堆疊，表格轉為卡片或簡化顯示。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/decision-record` — 獲取指定專案的決策記錄。
  - PUT `/api/projects/:id/decision-record` — 更新決策記錄信息。
  - POST `/api/projects/:id/decision-record/sign` — 提交決策簽核。
- **error cases**:
  - 獲取決策記錄失敗: 頁面顯示錯誤提示，並提供返回專案儀表板的按鈕。
  - 簽核失敗: 顯示簽核失敗提示，並提供重試選項。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- 無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [x] 決策記錄能完整展示決策聲明、KT 分析結果、結論和行動項目。
- [x] 簽核功能正常，簽核狀態能正確顯示。
- [x] 匯出報告功能正常，匯出文件格式正確。
- [x] 響應式設計在不同設備上顯示良好，信息呈現合理。
