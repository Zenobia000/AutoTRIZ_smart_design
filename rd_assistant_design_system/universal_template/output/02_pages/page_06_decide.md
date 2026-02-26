# Page-Level Prompt: Decide -- 最終決策

## [PAGE META]
- **page_name**: Decide -- 最終決策
- **route_path**: `/projects/:id/decide`
- **page_type**: tabs (3 Tabs)
  <!-- landing / form / dashboard / report / search / detail / settings / accordion / tabs -->
- **primary_goal**: 透過 WANT 加權評分矩陣、KT 決策記錄和匯出功能，完成方案選擇、決策簽核與知識沉澱。
- **secondary_goal**: 產生完整的決策紀錄文件 (PDF/JSON/全流程報告)，使決策可審查、可追溯、可複用。
- **phase**: Phase 3 Converge (#10B981 綠)
- **mapped_steps**: Step 3.2 決策與行動 + Step 3.3 內化與傳達
- **embedded_gates**: Gate 3.2 + Phase Gate 3 (= Gate 3.3)

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師、RD 主管
  - 次要：專案經理 (PM)、高階主管
- **entry_point**:
  - 從「設計審查 (Review)」頁面 Gate 3.1 通過後導航進入。
  - 從 Dashboard / Sidebar 直接點擊「Decide」卡片進入。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 中 (10-20 分鐘)
  <!-- WANT 評分需團隊共識，KT 決策記錄為最終確認 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **Phase Header**
   - section_type: header
   - section_purpose: 顯示 "Phase 3: Converge > Step 3.2-3.3 最終決策" breadcrumb 及 Phase 3 綠色色帶。

2. **Tab A -- WANT 評分**
   - section_type: tab / scoring-matrix
   - section_purpose: 以 WANT 加權評分矩陣比較各方案，輸出加權總分排行，提供數據驅動的方案選擇依據。

3. **Tab B -- KT 決策記錄**
   - section_type: tab / form
   - section_purpose: 記錄最終決策的選擇、理由和行動項目，建立可追溯的 KT (Kepner-Tregoe) 決策文件。

4. **Tab C -- 匯出**
   - section_type: tab / export
   - section_purpose: 匯出 PDF / JSON / 全流程報告，審查人簽核，完成專案知識沉澱 (Step 3.3)。

5. **Gate 3.2 Checklist**
   - section_type: gate-indicator (inline)
   - section_purpose: 內嵌 Gate 3.2，檢查 DecisionRecord 是否已建立。

6. **Phase Gate 3 (= Gate 3.3) Checklist**
   - section_type: gate-indicator (inline, milestone)
   - section_purpose: 醒目里程碑標記 (雙線框強調)，檢查決策簽核與知識沉澱完整性。Phase Gate 3 通過即代表專案完成。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: Phase Header
- **layout**: 頂部橫幅，Phase 3 綠色色帶 (#10B981)，breadcrumb 路徑。
- **elements**:
  - `Phase 色帶`: `div (4px height)`, `Display`, `背景色 #10B981，頁面頂部。`
  - `Breadcrumb`: `text`, `Display`, `"Phase 3: Converge > Step 3.2-3.3 最終決策"。`
- **states**:
  - 正常：色帶 + breadcrumb 靜態顯示。

### Section: Tab A -- WANT 評分
- **layout**: 上方為 WANT 加權評分表格 (行=條件, 列=方案)，下方為 Recharts 橫條圖排行。
- **input_category**: 必填 (Human Input) -- weights 和 scores 為用戶/團隊必填判斷。
- **visual_highlight**: WANT 分數排行橫條圖 (Recharts Horizontal Bar Chart)
- **elements**:
  - `[載入標準模板 (W1-W6)] 按鈕`: `button (secondary)`, `optional`, `一鍵建立 6 個標準 WANT 條件：W1 性能餘裕 / W2 製造性 / W3 成本 / W4 可靠性 / W5 時程 / W6 擴展性。每個條件預設包含 10分/6分/2分 描述錨點。已有條件時顯示確認提示 "將覆蓋現有條件，確定？"。`
  - `標準模板預設值`:
    - W1 性能餘裕: weight=10, score_10="完全滿足+20%餘裕", score_6="剛好滿足", score_2="不足需妥協"
    - W2 製造可行: weight=8, score_10="現有製程可做", score_6="需小幅改造", score_2="需全新製程"
    - W3 成本競爭: weight=7, score_10="低於目標成本", score_6="接近目標", score_2="超出30%+"
    - W4 可靠性: weight=8, score_10="MTBF>10萬小時", score_6="MTBF 5-10萬小時", score_2="MTBF<5萬小時"
    - W5 開發時程: weight=6, score_10="提前完成", score_6="準時", score_2="延遲>2個月"
    - W6 擴展性: weight=5, score_10="完全獨立模組化", score_6="部分耦合", score_2="高度耦合"
  - `WANT 條件表格`: `editable-table (React Table)`, `required`, `行標題：條件名稱 (W1, W2...)。列標題：條件名稱 / 權重 (1-10) / 方案 A 分數 / 方案 B 分數 / 方案 C 分數... (動態列，依方案數量)。`
  - `條件名稱`: `text (inline-edit)`, `required ★`, `WANT 條件名稱。可自訂。白底 + 紅色星號。`
  - `權重 (weight)`: `number-input (1-10)`, `required ★`, `條件權重，1=最低 10=最高。白底 + 紅色星號。`
  - `10分/6分/2分 描述`: `tooltip / expandable-row`, `optional`, `每個條件可展開查看 10分 (極佳)、6分 (及格)、2分 (不及格) 的描述錨點，幫助評分校準。`
  - `方案原始評分 (raw_score)`: `number-input (1-10)`, `required ★`, `每個方案在每個條件上的原始評分 1-10。白底 + 紅色星號。`
  - `加權分數 (weighted_score)`: `text (auto)`, `Display`, `自動計算 weight x raw_score，顯示於括號內。如 "8 (80)"。`
  - `加權總分列`: `text (auto, bold)`, `Display`, `表格最後一行，自動加總各條件的 weighted_score。最高分方案加 ★ 標記。`
  - `[+ 新增條件] 按鈕`: `button (ghost)`, `required`, `在表格底部新增空白條件行。`
  - `WANT 排行橫條圖`: `horizontal-bar-chart (Recharts)`, `Display`, `X 軸=加權總分，Y 軸=方案名稱。條形長度按比例，最高分以 Phase 3 綠色 (#10B981) 標記，其餘為灰色 (#D1D5DB)。`
  - `AI 評分建議卡片`: `agent-card`, `Agent`, `灰底卡片 (#F8F9FA) + [AI] 標籤。AI 根據 Review 頁的證據矩陣和實驗結果建議各方案評分。附 [採用] [編輯] [重生成] [跳過] 按鈕。`
- **states**:
  - 正常：表格有條件和方案，評分完整，橫條圖顯示排名。
  - empty-criteria：無條件時顯示 "尚無評分條件，點擊「載入標準模板」快速開始" + CTA 按鈕。
  - empty-alternatives：無方案時顯示 "尚無方案，請先在 Create 頁建立方案" + 導航至 Create。
  - partial：部分評分未填，表格中空格以淡黃底色標記。
  - loading：AI 建議中，顯示 skeleton 卡片。
  - complete：所有評分已填，排名圖表完整。
- **copy_constraints**:
  - 條件名稱：最少 2 字元，最多 80 字元。
  - 權重：整數 1-10。
  - 原始評分：整數 1-10。
  - 方案名稱：從方案集合自動帶入，不可在此修改。

### Section: Tab B -- KT 決策記錄
- **layout**: 三段式卡片佈局 (選擇 / 理由 / 行動)，垂直堆疊。
- **input_category**: 必填 (Human Input) -- decision_title、selected_alternative、rationale、action_items、risk_acceptance 為用戶必填。
- **visual_highlight**: 決策三段摘要卡片
- **elements**:
  - `選擇卡片`: `card`, `required`, `標題："選擇"。卡片頂部 4px Phase 3 綠色邊條。`
    - `decision_title`: `text-input`, `required ★`, `決策標題。白底 + 紅色星號。`
    - `selected_alternative`: `dropdown`, `required ★`, `選定方案，從 WANT 評分中的方案列表帶入。白底 + 紅色星號。預設為 WANT 最高分方案，可修改。`
  - `理由卡片`: `card`, `required`, `標題："理由"。卡片頂部 4px Phase 3 綠色邊條。`
    - `rationale`: `textarea`, `required ★`, `選擇理由，用戶填寫。白底 + 紅色星號。min-height: 100px, auto-grow。`
    - `AI 決策摘要`: `agent-card (inline)`, `Agent`, `灰底 + [AI] 標籤。AI 生成決策摘要，綜合 WANT 評分、MUST 篩選結果、風險評估。格式："基於 WANT 加權評分，方案 B 以 188 分排名第一；MUST 篩選全部通過；風險 R1 已有 mitigation..."。附 [採用] [編輯] 按鈕。點擊 [採用] 將 AI 摘要寫入 rationale 欄位。`
  - `行動卡片`: `card`, `required`, `標題："行動"。卡片頂部 4px Phase 3 綠色邊條。`
    - `action_items 列表`: `dynamic-list`, `required ★`, `每項包含：行動描述 (text-input ★) + 負責人 (text-input ★) + 到期日 (date-picker, optional)。至少 1 項。白底 + 紅色星號。`
    - `[+ 新增行動] 按鈕`: `button (ghost)`, `required`, `在列表底部新增空白行。`
    - `risk_acceptance`: `textarea`, `required ★`, `風險接受聲明。系統自動列出已識別的 H/H* 風險及其 mitigation，用戶確認接受。白底 + 紅色星號。`
- **states**:
  - 正常：三張卡片垂直堆疊，所有必填項已填寫。
  - empty：初次進入，卡片內欄位為空，引導 "請填寫決策記錄以完成 Gate 3.2"。
  - partial：部分必填項未填，對應卡片邊框顯示橙色提醒。
  - ai-loading：AI 決策摘要生成中，顯示 skeleton。
  - saved：保存成功，右上角顯示 "Saved ✓" 2 秒。
- **copy_constraints**:
  - decision_title：最少 5 字元，最多 200 字元。
  - rationale：最少 20 字元，最多 2000 字元。
  - action_items 描述：最少 5 字元，最多 300 字元。
  - action_items 負責人：最少 2 字元，最多 50 字元。
  - risk_acceptance：最少 10 字元，最多 1000 字元。

### Section: Tab C -- 匯出
- **layout**: 匯出選項列表 + 審查人簽核區 + 預覽區。
- **input_category**: 必填 (Human Input) -- 審查人簽核為必填。
- **elements**:
  - `匯出按鈕組`: `button-group`, `required`, `三個按鈕：[匯出 PDF] / [匯出 JSON] / [匯出全流程報告]。`
  - `匯出 PDF`: `button (primary)`, `required`, `匯出 KT 決策記錄為 PDF 文件，包含選擇/理由/行動/風險接受。`
  - `匯出 JSON`: `button (secondary)`, `required`, `匯出結構化 JSON 數據，包含完整專案工件 (definitions, assumptions, alternatives, decisions)。`
  - `匯出全流程報告`: `button (primary)`, `required`, `匯出從 Brief 到 Decide 的完整專案報告，涵蓋所有 Phase/Step/Gate 數據。`
  - `匯出預覽區`: `preview-panel`, `Display`, `點擊任一匯出按鈕前，顯示該格式的內容預覽 (摘要)。PDF 預覽為前 2 頁縮圖；JSON 預覽為結構摘要；全流程預覽為目錄大綱。`
  - `審查人簽核`: `signature-form`, `required ★`, `三個必填欄位：姓名 (text-input ★) / 角色 (dropdown: RD 工程師/RD 主管/PM/品質工程師/其他 ★) / 簽核日期 (date-picker, 預設今天 ★)。白底 + 紅色星號。`
  - `[新增簽核人] 按鈕`: `button (ghost)`, `optional`, `允許多人簽核 (如需要 RD 主管 + PM 雙簽)。`
- **states**:
  - 正常：三個匯出按鈕可用，簽核區已填寫。
  - incomplete：DecisionRecord 未建立 (Tab B 未完成)，匯出按鈕禁用 + tooltip "請先完成 KT 決策記錄"。
  - exporting：匯出中，按鈕顯示 spinner + "匯出中..."。
  - exported：匯出成功，Toast "匯出成功" + 下載自動觸發。
  - error：匯出失敗，Toast "匯出失敗，請重試"。
- **copy_constraints**:
  - 簽核姓名：最少 2 字元，最多 50 字元。
  - 簽核日期：格式 YYYY-MM-DD。

### Section: Gate 3.2 Checklist
- **layout**: 頁面底部嵌入，水平分隔線上方，checklist 格式。Step Gate 樣式 (單線框) + Phase 3 綠色色帶。
- **input_category**: 必須呈現 (Display)
- **elements**:
  - `Gate 標題`: `h3`, `required`, `"Gate 3.2 -- 決策記錄完整性檢查" + Phase 3 綠色色帶 (#10B981)。`
  - `Checklist 項目 (x3)`: `checklist-item (repeating, Display)`, `required`, `三項即時檢查：(1) DecisionRecord 已建立 (✅/❌)、(2) selected_alternative 已選擇 (✅/❌)、(3) action_items 非空 (至少 1 項) (✅/❌)。`
  - `Gate 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ 時顯示 "Gate 3.2 Passed" (綠色 badge #28a745)。`
- **states**:
  - all-passed：三項皆 ✅，綠色 badge。
  - partial/none：部分或全部 ❌，紅色 badge #dc3545。

### Section: Phase Gate 3 (= Gate 3.3) Checklist
- **layout**: Gate 3.2 下方，雙線框強調 (border: 2px double #10B981)，Phase Gate 里程碑樣式。
- **input_category**: 必須呈現 (Display) -- 醒目里程碑標記
- **elements**:
  - `Phase Gate 標題`: `h3 (emphasized)`, `required`, `"Phase Gate 3 (= Gate 3.3) -- 最終里程碑" + Phase 3 綠色色帶 (#10B981) + 雙線框。`
  - `Checklist 項目 (x3)`: `checklist-item (repeating, Display)`, `required`, `三項即時檢查：(1) DecisionRecord 已簽核 (至少 1 人簽核) (✅/❌)、(2) 所有 H/H* Risk 有 mitigation (✅/❌)、(3) action_items 非空 (至少 1 項) (✅/❌)。`
  - `Phase Gate 狀態 badge`: `badge (Display, large)`, `required`, `全部 ✅ 時顯示 "Phase Gate 3 Passed" (綠色 badge, 放大)。`
  - `完成按鈕`: `button (primary, large)`, `required`, `"Phase Gate 3 通過 → 專案完成"。Phase Gate 通過時啟用 (#10B981 green, 放大按鈕)，未通過時禁用。通過後導航至 Dashboard 並顯示成功慶祝畫面 (confetti animation)。`
- **states**:
  - all-passed：三項皆 ✅，綠色 badge (放大)，按鈕啟用。
  - partial/none：紅色 badge，按鈕禁用 + tooltip "請完成所有條件"。

## [WIREFRAME]

```
┌─ Header: Phase 3: Converge > Step 3.2-3.3 最終決策 ──────────┐
│                                                                │
│ [WANT 評分] [KT 決策記錄] [匯出]             ← 3 Tabs         │
│ ─────────────────────────────────                              │
│                                                                │
│ Tab A: WANT 評分                                               │
│ [載入標準模板 (W1-W6)]                                          │
│ ┌──────────┬──────┬────────┬────────┬────────┐                │
│ │ 條件      │ 權重 │ 方案 A  │ 方案 B  │ 方案 C │                │
│ ├──────────┼──────┼────────┼────────┼────────┤                │
│ │W1 性能餘裕│ 10   │ 8 (80) │ 6 (60) │ 7 (70) │                │
│ │W2 製造性  │ 8    │ 7 (56) │ 9 (72) │ 6 (48) │                │
│ │W3 成本    │ 7    │ 6 (42) │ 8 (56) │ 7 (49) │                │
│ ├──────────┼──────┼────────┼────────┼────────┤                │
│ │ 加權總分  │      │ 178    │ 188 ★  │ 167    │                │
│ └──────────┴──────┴────────┴────────┴────────┘                │
│                                                                │
│ [Recharts 橫條圖: 方案排名]                                     │
│ 方案 B ████████████████████ 188                                │
│ 方案 A ███████████████████  178                                │
│ 方案 C █████████████████    167                                │
│                                                                │
│ Tab B: KT 決策記錄                                             │
│ ┌─ 選擇 ──────────────────────────────────────────────┐       │
│ │ ★ 決策標題: [________________]                        │       │
│ │ ★ 選定方案: [方案 B ▼]                                │       │
│ └──────────────────────────────────────────────────────┘       │
│ ┌─ 理由 ──────────────────────────────────────────────┐       │
│ │ ★ 選擇理由: [________________________________]        │       │
│ │ [AI] 決策摘要: "基於 WANT 加權評分..."                 │       │
│ │ [採用] [編輯]                                          │       │
│ └──────────────────────────────────────────────────────┘       │
│ ┌─ 行動 ──────────────────────────────────────────────┐       │
│ │ ★ 行動項目:                                           │       │
│ │   1. [________________________________] 負責人: [___] │       │
│ │   2. [________________________________] 負責人: [___] │       │
│ │ [+ 新增行動]                                           │       │
│ │ ★ 風險接受: [已識別風險的接受聲明]                      │       │
│ └──────────────────────────────────────────────────────┘       │
│                                                                │
│ Tab C: 匯出                                                    │
│ [匯出 PDF]  [匯出 JSON]  [匯出全流程報告]                       │
│ ★ 審查人簽核: [姓名] [角色] [日期]                               │
│                                                                │
│ ── Gate 3.2 ──────────────────────────────────                 │
│ ✅ Decision Record 已建立  ✅ 方案已選定  ✅ 行動項目非空        │
│                                                                │
│ ══ Phase Gate 3 (= Gate 3.3) ═══════════════                   │
│ ✅ 已簽核  ✅ H/H* Risk 有 mitigation  ✅ 行動項目非空          │
│ [🏁 Phase Gate 3 通過 → 專案完成]                              │
└────────────────────────────────────────────────────────────────┘
```

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入頁面，系統載入方案列表 (alternatives)、WANT 條件、風險數據，預設顯示 Tab A WANT 評分。
  2. Tab A：用戶可點擊 [載入標準模板 (W1-W6)] 快速建立 6 個標準條件，或手動新增條件。填寫 weight ★ 和每個方案的 raw_score ★。系統即時計算 weighted_score 和加權總分。橫條圖即時更新排名。
  3. Tab A：AI 建議卡片提供評分參考 (基於 Review 頁的證據和實驗)。用戶可採用或忽略。
  4. 用戶切換至 Tab B KT 決策記錄。填寫 decision_title ★、selected_alternative ★ (預設為 WANT 最高分方案)、rationale ★。
  5. Tab B：AI 自動生成決策摘要，綜合 WANT/MUST/Risk 數據。用戶可 [採用] 將摘要寫入 rationale，或 [編輯] 修改。
  6. Tab B：填寫 action_items ★ (至少 1 項) 和 risk_acceptance ★。系統自動列出 H/H* 風險作為參考。
  7. 用戶切換至 Tab C 匯出。填寫審查人簽核 ★ (姓名/角色/日期)。選擇匯出格式並下載。
  8. 頁面底部 Gate 3.2 和 Phase Gate 3 checklist 自動更新。Gate 3.2 先通過，Phase Gate 3 在簽核完成後通過。
  9. Phase Gate 3 通過後，點擊 "專案完成" 按鈕，導航至 Dashboard 並顯示慶祝畫面。

- **Tab 間聯動**：
  - Tab A 最高分方案 → Tab B selected_alternative 預設值。
  - Tab B 完成填寫 → Tab C 匯出按鈕啟用。
  - Tab C 簽核完成 → Phase Gate 3 checklist 更新。
  - Tab A/B 數據變化 → Gate 3.2 checklist 自動 re-evaluate。
  - Tab C 簽核 → Phase Gate 3 checklist 自動 re-evaluate。

- **Auto-Save 策略**：
  - Tab A 評分表：每次 score/weight 變更 debounce 1s 自動保存 (PUT)。
  - Tab B 決策記錄：onBlur 或 debounce 5s 自動保存 (PUT)。
  - 儲存中顯示 "Saving..." 右上角 indicator，成功後顯示 "Saved ✓" 2 秒。

- **表單驗證規則**：
  - Tab A `weight`：必填，整數 1-10 → "請輸入 1-10 之間的權重"。
  - Tab A `raw_score`：必填，整數 1-10 → "請輸入 1-10 之間的評分"。
  - Tab B `decision_title`：必填，最少 5 字元 → "請輸入決策標題"。
  - Tab B `selected_alternative`：必填 → "請選擇方案"。
  - Tab B `rationale`：必填，最少 20 字元 → "請填寫選擇理由"。
  - Tab B `action_items`：至少 1 項，每項描述最少 5 字元 → "請填寫至少一項行動"。
  - Tab B `risk_acceptance`：必填，最少 10 字元 → "請填寫風險接受聲明"。
  - Tab C `signature name`：必填，最少 2 字元 → "請填寫審查人姓名"。
  - Tab C `signature role`：必填 → "請選擇審查人角色"。
  - Tab C `signature date`：必填 → "請選擇簽核日期"。

- **資料更新策略**：
  - Tab A WANT 條件+評分：GET/PUT want 端點，React Query 管理，staleTime: 30s。
  - Tab B 決策記錄：GET/POST/PUT decisions 端點。
  - Tab C 匯出：GET export 端點 (觸發下載)。
  - Gate check：每次 Tab 切換或數據變更時自動 GET gates check。

- **RWD 行為差異**：
  - Desktop (>1024px): Tab 水平排列。WANT 表格完整顯示所有方案列。橫條圖完整。KT 決策三卡片垂直堆疊。
  - Tablet (768px - 1023px): Tab 水平排列。WANT 表格可水平滾動 (方案多時)。橫條圖完整。三卡片垂直堆疊。
  - Mobile (<768px): Tab 改為下拉選單切換。WANT 表格轉為方案卡片式 (每張卡片顯示一個方案在所有條件上的評分)。橫條圖保留但縮窄。三卡片全寬堆疊。

## [STATE DESIGN]

### Zustand Store Slice: `decideStore`
```typescript
interface DecideState {
  activeTab: 'want' | 'decision' | 'export';
  topAlternativeId: string | null;
  decisionRecordCreated: boolean;
  signedOff: boolean;
  setActiveTab: (tab: DecideState['activeTab']) => void;
}
```

### React Query Keys
```typescript
const decideQueryKeys = {
  want: (projectId: string) => ['projects', projectId, 'want'],
  alternatives: (projectId: string) => ['projects', projectId, 'alternatives'],
  decisions: (projectId: string) => ['projects', projectId, 'decisions'],
  risks: (projectId: string) => ['projects', projectId, 'risks'],
  gate32: (projectId: string) => ['projects', projectId, 'gates', '3.2'],
  gate33: (projectId: string) => ['projects', projectId, 'gates', '3.3'],
  export: (projectId: string) => ['projects', projectId, 'export'],
};
```

### Cross-Tab Invalidation Flow
```
Tab A: mutation (update want scores)
  → invalidateQueries(['projects', projectId, 'gates', '3.2'])

Tab B: mutation (create/update decision)
  → invalidateQueries(['projects', projectId, 'gates', '3.2'])
  → invalidateQueries(['projects', projectId, 'gates', '3.3'])

Tab C: mutation (sign off)
  → invalidateQueries(['projects', projectId, 'gates', '3.3'])
```

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/want` -- 獲取 WANT 條件及評分數據。
  - POST `/api/projects/:id/want` -- 建立/更新 WANT 條件。
  - PUT `/api/projects/:id/want/:want_id` -- 更新單項 WANT 條件/評分。
  - POST `/api/projects/:id/want/load-template` -- 載入 W1-W6 標準模板。
  - GET `/api/projects/:id/alternatives` -- 獲取方案列表 (供 WANT 評分和決策選擇)。
  - GET `/api/projects/:id/decisions` -- 獲取決策記錄。
  - POST `/api/projects/:id/decisions` -- 建立決策記錄。
  - PUT `/api/projects/:id/decisions/:dec_id` -- 更新決策記錄。
  - POST `/api/projects/:id/decisions/ai-summary` -- AI 生成決策摘要。
  - GET `/api/projects/:id/export?format=pdf|json|full` -- 觸發匯出並下載。
  - POST `/api/projects/:id/decisions/:dec_id/sign-off` -- 審查人簽核。
  - GET `/api/projects/:id/gates/3.2/check` -- 檢查 Gate 3.2 狀態。
  - GET `/api/projects/:id/gates/3.3/check` -- 檢查 Phase Gate 3 狀態。
- **response shape** (GET `/api/projects/:id/want`):
  ```json
  {
    "criteria": [
      {
        "id": "uuid",
        "name": "W1 性能餘裕",
        "weight": 10,
        "description_10": "所有指標超過目標 20%+",
        "description_6": "所有指標達到目標",
        "description_2": "部分指標未達目標",
        "scores": {
          "alt-uuid-A": { "raw": 8, "weighted": 80 },
          "alt-uuid-B": { "raw": 6, "weighted": 60 }
        }
      }
    ],
    "totals": {
      "alt-uuid-A": 178,
      "alt-uuid-B": 188
    },
    "top_alternative_id": "alt-uuid-B"
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/3.2/check`):
  ```json
  {
    "gate_id": "3.2",
    "passed": true,
    "checklist": [
      { "label": "DecisionRecord 已建立", "passed": true },
      { "label": "selected_alternative 已選擇", "passed": true },
      { "label": "action_items 非空", "passed": true }
    ]
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/3.3/check`):
  ```json
  {
    "gate_id": "3.3",
    "passed": false,
    "checklist": [
      { "label": "DecisionRecord 已簽核", "passed": false },
      { "label": "所有 H/H* Risk 有 mitigation", "passed": true },
      { "label": "action_items 非空", "passed": true }
    ]
  }
  ```
- **error cases**:
  - WANT 數據載入失敗 (500): Tab A 顯示錯誤提示 + 重試按鈕。
  - 方案列表為空 (404/empty): Tab A 顯示引導至 Create 頁建立方案。
  - 決策記錄保存失敗 (500): Toast 提示 "保存失敗"，資料保留 local state。
  - AI 決策摘要失敗 (500): Toast 提示 "AI 暫時不可用"，不阻塞流程。
  - 匯出失敗 (500): Toast 提示 "匯出失敗，請重試"。
  - 簽核保存失敗 (500): Toast 提示，提供重試。
  - Gate API 查詢失敗 (500): Gate 指示器顯示 ⚠️ + "無法檢查" badge (灰色)，提供重試。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **WANT 表格行動端轉為方案卡片式**：覆蓋 Global 預設的表格 RWD 行為 (水平滾動)，改用方案卡片 (每張卡片列出該方案在所有條件上的評分)。原因：動態列數的評分表格在窄螢幕完全失去可讀性。
- **雙 Gate 同頁**：此頁同時包含 Gate 3.2 (Step Gate) 和 Phase Gate 3 (Gate 3.3)，是唯一一頁包含 2 個 Gate 的功能頁。Phase Gate 3 使用雙線框強調，與 Gate 3.2 單線框區分。原因：Step 3.2 和 3.3 邏輯上連續 (決策→簽核→匯出)，分頁會破壞流程連貫性。
- **專案完成慶祝動畫**：Phase Gate 3 通過後觸發 confetti 動畫。覆蓋 Global 的輕量 Toast 回饋規範。原因：Phase Gate 3 是整個專案的最終里程碑，值得更強的正面回饋，符合 Apple "Delight" 設計哲學。

## [HANDOFF CHECKLIST]
- [ ] 設計稿 (Figma) 已完成 Tab A/B/C 三個 Tab 視圖及 Desktop/Tablet/Mobile 斷點。
- [ ] WANT 評分表格支援動態列 (方案數量不固定)，已確認表格元件彈性。
- [ ] 橫條圖色彩 (最高分綠/其餘灰) 對比度已通過 WCAG AA 檢測。
- [ ] KT 決策記錄三段卡片 (選擇/理由/行動) 佈局已確認 RWD 表現。
- [ ] API 契約已與後端確認 (want, decisions, alternatives, export, gates/3.2, gates/3.3)。
- [ ] React Query invalidation flow 已確認跨 Tab 聯動邏輯。
- [ ] Recharts 橫條圖元件已確認可接受動態方案數量。
- [ ] AI Agent 卡片 (評分建議 / 決策摘要) 遵循 Global [AI] 標籤 + 灰底規範。
- [ ] Gate 3.2 三項 + Phase Gate 3 三項 checklist 條件與後端 API 一致。
- [ ] 匯出功能三種格式 (PDF/JSON/Full Report) 已確認後端支援。
- [ ] 簽核流程已確認 (多人簽核 / 角色選擇 / 日期記錄)。
- [ ] Confetti 動畫套件已選定 (如 canvas-confetti)，效能衝擊可接受。
- [ ] Skeleton 骨架屏已設計 Tab A/B/C 各自的 loading 態。
- [ ] E2E 測試腳本覆蓋：WANT 評分→KT 決策→簽核→匯出→Phase Gate 3 通過→專案完成。

## [ACCEPTANCE CRITERIA]
- [ ] Tab A [載入標準模板 (W1-W6)] 按鈕正確建立 6 個標準條件，含 10分/6分/2分 描述。
- [ ] Tab A WANT 條件表格可新增/編輯/刪除條件，支援動態方案列。
- [ ] Tab A weight 和 raw_score 為必填 (1-10)，weighted_score 和加權總分自動計算。
- [ ] Tab A 最高分方案以 ★ 標記。
- [ ] Tab A Recharts 橫條圖正確顯示方案排名，最高分以綠色標記。
- [ ] Tab A AI 評分建議卡片正確顯示灰底 + [AI] 標籤。
- [ ] Tab B 三段卡片 (選擇/理由/行動) 正確渲染，所有必填項驗證正常。
- [ ] Tab B selected_alternative 預設為 WANT 最高分方案，可修改。
- [ ] Tab B AI 決策摘要生成正常，[採用] 可將摘要寫入 rationale。
- [ ] Tab B action_items 支援新增/刪除，至少 1 項必填。
- [ ] Tab B risk_acceptance 自動列出 H/H* 風險作為參考。
- [ ] Tab C 三種匯出格式按鈕功能正常，DecisionRecord 未完成時禁用。
- [ ] Tab C 審查人簽核表單必填驗證正常，支援多人簽核。
- [ ] Tab C 匯出預覽區正確顯示預覽內容。
- [ ] Gate 3.2 三項 checklist 正確反映條件。
- [ ] Phase Gate 3 三項 checklist 正確反映條件，雙線框醒目顯示。
- [ ] Phase Gate 3 通過後完成按鈕啟用，點擊導航至 Dashboard。
- [ ] Auto-save 機制正常運作，有視覺回饋。
- [ ] 響應式設計在 Desktop / Tablet / Mobile 三種視口正確呈現。

## [VERSION]
- **current_version**: v2.0
- **last_updated**: 2026-02-25
- **changelog**:
  - v1.0 -- 初版建立 (基於 Blueprint 14.6 規格)
  - v2.0 -- 完整重寫：新增 wireframe、STATE DESIGN、HANDOFF CHECKLIST；拆分 Gate 3.2 和 Phase Gate 3；細化 Tab A/B/C 元件規格；新增 AI Agent 互動模式；補充 API response shape；新增匯出預覽和多人簽核
