# Page-Level Prompt: Create -- 方案創造

## [PAGE META]
- **page_name**: Create -- 方案創造
- **route_path**: `/projects/:id/create`
- **page_type**: accordion (7 sequential sub-steps, progressively disclosed)
  <!-- landing / form / dashboard / report / search / detail / settings / accordion / tabs -->
- **primary_goal**: 引導用戶完成 Anti-Anchor → TRIZ → 子系統 → SCAMPER → 方案生成 → MUST 快篩 → Pre-CAD 審查完整方案創造流程，將矛盾轉化為可審查的設計方案。
- **secondary_goal**: 確保方案多元性 (Anti-Anchor)、結構化發散 (TRIZ + SCAMPER)、嚴格收斂 (MUST + Pre-CAD)，為 Phase 3 決策做準備。
- **phase**: Phase 2 Diverge (#F59E0B 橙)
- **steps**: Step 2.2.1 ~ 2.2.6 + Step 2.3
- **embedded_gates**: Gate 2.2.1 (Activity Gate), Gate 2.2 (Step Gate), Phase Gate 2 = Gate 2.3 (Phase Gate)

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管
- **entry_point**:
  - 從「假設追蹤 (Track)」頁面 Gate 2.1 通過後點擊「前往 Create →」導航進入。
  - 從 Dashboard 的 6+1 導航區點擊「Create」卡片進入。
  - 從 Review 頁面的 breadcrumb 點擊「Create」返回。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (30-60 分鐘)
  <!-- 7 個子步驟逐步展開，用戶可分多次完成 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **子步驟進度條**
   - section_type: progress-bar
   - section_purpose: 顯示 7 個子步驟的完成狀態，讓用戶知道目前位於流程的哪個階段。

2. **Accordion 1 -- Anti-Anchor Sprint (Step 2.2.1)**
   - section_type: accordion / form
   - section_purpose: 打破路徑依賴，引導用戶建立至少 1 條非基準路線。

3. **Accordion 2 -- TRIZ 解矛盾 (Step 2.2.2)**
   - section_type: accordion / tabs (3 sub-tabs: TC / PC / SF)
   - section_purpose: 針對每個矛盾，透過矩陣查表 + 分離原理 + 76 標準解三條路徑產出解法建議。

4. **Accordion 3 -- 子系統定義 (Step 2.2.3)**
   - section_type: accordion / form
   - section_purpose: AI 建議受影響子系統，用戶確認後作為 SCAMPER 輸入。

5. **Accordion 4 -- SCAMPER 變形 (Step 2.2.4)**
   - section_type: accordion / card-grid
   - section_purpose: 對每個子系統執行 7 種 SCAMPER 變形，生成更多方案變體。

6. **Accordion 5 -- 方案生成 (Step 2.2.5)**
   - section_type: accordion / card-list
   - section_purpose: AI 整合 TRIZ + SCAMPER 產出方案集合 (concept routes)，用戶命名、描述機制、標記關鍵假設。

7. **Accordion 6 -- MUST 快篩 (Step 2.2.6)**
   - section_type: accordion / matrix-table
   - section_purpose: 以 Go/No-Go 矩陣 (方案 x MUST 約束) 快速淘汰不符合硬約束的方案。

8. **Accordion 7 -- Pre-CAD 審查 (Step 2.3)**
   - section_type: accordion / scoring-form + radar-chart
   - section_purpose: 對通過 MUST 的方案進行 5 維度評分 (空間/成本/安全/解耦/供應)，決定是否進入 CAD 階段。

9. **Gate 檢查指示器**
   - section_type: gate-indicator (inline, dual-layer)
   - section_purpose: 內嵌 Gate 2.2 (Step Gate) + Phase Gate 2 = Gate 2.3 (Phase Gate) checklist，顯示通過條件。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 子步驟進度條
- **layout**: 頁面頂部水平進度條，7 個節點，Phase 2 橙色主題 (#F59E0B)。
- **elements**:
  - `進度節點 x 7`: `step-indicator`, `Display`, `圖示狀態：✅ 已完成 (filled circle, 綠色) / ◉ 進行中 (outlined circle, 橙色 pulse) / ○ 未開始 (empty circle, 灰色 #D1D5DB)。`
  - `節點標籤 x 7`: `Anti-Anchor` → `TRIZ` → `子系統` → `SCAMPER` → `方案` → `MUST` → `Pre-CAD`
  - `連線`: 節點間橙色連線 (#F59E0B)，已完成段為實線，未完成段為虛線。
- **states**:
  - 根據各 Accordion 的完成狀態自動計算 (Display，不可手動編輯)。
  - 點擊節點可快速 scroll 至對應 Accordion (僅已展開或已完成的節點可點擊)。
- **copy_constraints**:
  - 每個節點標籤最多 10 個字元。

### Section: Accordion 1 -- Anti-Anchor Sprint (Step 2.2.1)
- **layout**: 可展開的 Accordion 面板，內部為黃色警告卡片 + 路線輸入表單。
- **visual_highlight**: 黃色警告卡片 -- 路徑依賴偵測提醒 (Anti-Anchor)。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"1. Anti-Anchor Sprint (Step 2.2.1)" + 狀態 badge: [✅ 完成] / [◉ 進行中] / [○ 未開始]。`
  - `路徑依賴警告`: `alert-card (yellow, #FEF3C7 底 + #F59E0B 左邊線 4px)`, `Agent`, `AI 分析當前專案可能的路徑依賴風險，顯示為黃色警告卡片。附 [AI] 標籤 + 具體風險描述。`
  - `非基準路線列表`: `dynamic-input-list`, `required (★必填)`, `用戶輸入至少 1 條非基準設計路線。每條路線包含：名稱 (text, ★必填) + 簡述 (textarea, ★必填)。`
  - `[+ 新增路線] 按鈕`: `button (secondary)`, `required`, `新增一條空白路線輸入。`
  - `[AI 生成非基準路線] 按鈕`: `button (secondary)`, `Agent`, `AI 自動生成 >=1 條非對標路線建議，以灰底卡片顯示，附 [採用] [編輯] [跳過] 按鈕。`
  - `Gate 2.2.1 行內指示`: `gate-inline (Display)`, `required`, `"Gate 2.2.1: >=1 非對標路線且通過 M1+M4" → ✅ / ❌。Activity Gate 樣式 (輕量 inline badge)。`
- **states**:
  - 正常：表單可編輯，AI 警告卡片已載入。
  - loading：AI 分析中，黃色卡片顯示 skeleton。
  - error：AI 分析失敗，顯示 fallback 提示 + [重試] 按鈕。
  - complete：>=1 路線已填寫，Gate 2.2.1 顯示 ✅，Accordion 標題顯示 [✅ 完成]。
- **copy_constraints**:
  - 路線名稱：最少 3 字元，最多 50 字元。
  - 路線簡述：最少 10 字元，最多 300 字元。
  - AI 警告描述：最多 500 字元。

### Section: Accordion 2 -- TRIZ 解矛盾 (Step 2.2.2)
- **layout**: Accordion 展開後，按矛盾分組。每個矛盾內部有 3-tab 切換：矩陣查表 (TC) / 分離原理 (PC) / 76 標準解 (SF)。
- **visual_highlight**: TRIZ 3-path tabs -- TC/PC/SF 三條路徑彩色標籤切換。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"2. TRIZ 解矛盾 (Step 2.2.2)" + 狀態 badge。`
  - `矛盾分組標題`: `heading (repeating)`, `Display`, `每個矛盾顯示：矛盾代碼 (如 "C-001") + 名稱 + 改善/惡化參數 (TC) 或屬性 A/非 A (PC)。`
  - `3-path Tab bar`:
    - `矩陣查表 Tab (TC)`: `tab-button`, `required`, `"矩陣查表" + 藍色底線。`
    - `分離原理 Tab (PC)`: `tab-button`, `required`, `"分離原理" + 橙色底線。`
    - `76 標準解 Tab (SF)`: `tab-button`, `required`, `"76 標準解" + 綠色底線。`
  - `TC Tab 內容`:
    - `矩陣查表結果`: `Display`, `Agent`, `根據改善/惡化參數自動查詢 39x39 矛盾矩陣，列出建議原理編號及名稱。`
    - `原理解法卡片 x N`: `card (grey #F8F9FA)`, `Agent`, `每張卡片：原理編號 + 名稱 + AI 針對此矛盾的具體解法建議。附 [AI] 標籤。`
    - `採用/編輯/重生成/跳過`: `button-group`, `required (★必填)`, `用戶對每張解法卡片選擇操作。[採用] 綠色 / [編輯] 灰色 / [重生成] 橙色 / [跳過] 灰色。`
  - `PC Tab 內容`:
    - `分離原則卡片 x 4`: `card (grey)`, `Agent`, `時間分離 / 空間分離 / 條件分離 / 尺度分離，每張有 AI 具體建議。附 [AI] 標籤。`
    - `採用/編輯/重生成/跳過`: `button-group`, `required (★必填)`, `同 TC Tab。`
  - `SF Tab 內容`:
    - `76 標準解法建議`: `card (grey)`, `Agent`, `AI 從 76 標準解中匹配適用解法。附 [AI] 標籤。`
    - `採用/編輯/重生成/跳過`: `button-group`, `required (★必填)`, `同 TC Tab。`
- **states**:
  - 正常：Tab 可切換，卡片已載入。
  - loading：AI 生成解法中，卡片區顯示 skeleton。
  - error：TRIZ 查詢失敗，顯示重試按鈕。
  - complete：至少一個矛盾有被採用的解法。
- **copy_constraints**:
  - AI 解法建議：最多 500 字元。
  - 用戶編輯解法：最少 10 字元，最多 500 字元。

### Section: Accordion 3 -- 子系統定義 (Step 2.2.3)
- **layout**: Accordion 展開後，AI 建議子系統卡片列表 + 用戶確認。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"3. 子系統定義 (Step 2.2.3)" + 狀態 badge。`
  - `AI 建議子系統列表`: `checklist (grey #F8F9FA)`, `Agent`, `AI 根據矛盾和採用解法，建議受影響的子系統清單。附 [AI] 標籤。每個子系統顯示名稱 + 影響原因 + 關聯矛盾代碼。`
  - `用戶確認勾選`: `checkbox-group`, `required (★必填)`, `用戶勾選確認受影響子系統，可新增/移除。至少確認 1 個。`
  - `[+ 手動新增子系統]`: `button (secondary)`, `optional`, `用戶新增 AI 未建議的子系統。`
- **states**:
  - 正常：AI 建議已載入，用戶可勾選。
  - loading：AI 分析中，顯示 skeleton 卡片列表。
  - complete：至少一個子系統被確認。
- **copy_constraints**:
  - 子系統名稱：最少 2 字元，最多 50 字元。
  - 影響原因：最多 200 字元。

### Section: Accordion 4 -- SCAMPER 變形 (Step 2.2.4)
- **layout**: 以子系統為分組，每個子系統下方展開 7 種 SCAMPER 動作 (S/C/A/M/P/E/R) 的卡片網格。
- **visual_highlight**: 7-column SCAMPER matrix -- S/C/A/M/P/E/R x 子系統。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"4. SCAMPER 變形 (Step 2.2.4)" + 狀態 badge。`
  - `子系統分組標題`: `heading (repeating)`, `Display`, `子系統名稱。`
  - `SCAMPER 變體卡片 x 7 (per subsystem)`: `card (grey #F8F9FA)`, `Agent`, `每張卡片對應一種 SCAMPER 動作 (S=Substitute, C=Combine, A=Adapt, M=Modify, P=Put to other use, E=Eliminate, R=Rearrange)。AI 生成變體描述，附 [AI] 標籤。`
  - `採用/編輯/跳過`: `button-group`, `optional`, `用戶對每張變體卡片選擇操作。標記為 "promising" 的變體會帶入方案生成。`
  - `[回饋新矛盾] 按鈕`: `button (accent, 橙底白字)`, `optional`, `若 SCAMPER 變體揭示新矛盾，可回饋至 Accordion 2 TRIZ 重新處理。`
- **states**:
  - 正常：變體卡片已載入，7 x N 網格可瀏覽。
  - loading：AI 生成變體中，卡片區顯示 skeleton 網格。
  - feedback-loop：用戶點擊 [回饋新矛盾] 後，頁面 smooth scroll 回 Accordion 2 並高亮新矛盾。
- **copy_constraints**:
  - 變體描述：最多 300 字元。
  - SCAMPER 動作名稱固定 (S/C/A/M/P/E/R)，不可修改。

### Section: Accordion 5 -- 方案生成 (Step 2.2.5)
- **layout**: 卡片列表，每張卡片展示一個完整方案 (concept route / alternative)。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"5. 方案生成 (Step 2.2.5)" + 狀態 badge。`
  - `方案卡片 x N`: `card (white, bordered)`, `Display + editable`, `每張卡片顯示：`
    - `方案名稱`: `text (★必填)`, `required`, `用戶命名或 AI 建議。`
    - `機制說明`: `textarea (★必填)`, `required`, `描述方案核心機制。`
    - `關鍵假設`: `chip-group (★必填)`, `required`, `關聯假設列表 (如 "A-001", "A-005")，從 Track 頁面假設中選擇。`
    - `來源標記`: `badge (Display)`, `required`, `標示方案來源：TRIZ#XX / SCAMPER-X / Manual / AI-Integrated。`
    - `robust_scores`: `badge-group (Display)`, `required`, `顯示 robustness 評分，系統自動計算或用戶手動填寫。`
  - `[+ 手動新增] 按鈕`: `button (secondary)`, `required`, `用戶手動新增方案。`
  - `[AI 整合生成] 按鈕`: `button (primary)`, `Agent`, `AI 整合前述步驟 (TRIZ 採用解法 + SCAMPER promising 變體) 產出方案集合，以灰底卡片列表呈現，附 [AI] 標籤 + [採用] [編輯] [重生成]。`
- **states**:
  - 正常：方案卡片正常顯示。
  - empty：無方案時顯示引導提示 "點擊 [AI 整合生成] 或 [+ 手動新增] 建立方案"。
  - loading：AI 整合生成中，顯示 skeleton 卡片列表。
- **copy_constraints**:
  - 方案名稱：最少 3 字元，最多 100 字元。
  - 機制說明：最少 20 字元，最多 500 字元。

### Section: Accordion 6 -- MUST 快篩 (Step 2.2.6)
- **layout**: 矩陣表格，行 = 方案 (alternatives)，列 = MUST 約束。
- **visual_highlight**: MUST 紅綠矩陣 -- Go/No-Go 熱力表格 (✅綠 / ❌紅 / ⚠️橙)。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"6. MUST 快篩 (Step 2.2.6)" + 狀態 badge。`
  - `MUST 矩陣表格`: `matrix-table`, `required (★必填)`, `行標題：方案名稱。列標題：M1 空間 / M2 成本 / M3 安全餘裕 / M4 解耦 / M5 供應。`
  - `矩陣儲存格`: `toggle (3-state)`, `required (★必填)`, `每格切換：✅ pass (綠底 #D1FAE5) / ❌ fail (紅底 #FEE2E2) / ⚠️ marginal (橙底 #FEF3C7)。`
  - `[AI 預填] 按鈕`: `button (secondary)`, `Agent`, `AI 根據方案機制自動預填 MUST 評估，用戶可覆蓋。結果帶 [AI] 標籤。`
  - `篩選摘要`: `summary-bar (Display)`, `required`, `顯示「X 方案通過 (全✅)，Y 方案淘汰 (任一❌)，Z 方案待定 (有⚠️)」。`
  - `淘汰行高亮`: `row-style`, `Display`, `有任一 ❌ 的方案列灰底 + 刪除線文字，標記為淘汰。`
- **states**:
  - 正常：矩陣可互動，每格可點擊切換。
  - complete：所有儲存格已填。
  - warning：有方案全部 ❌ 時，該列灰底標記淘汰。
  - ai-prefilled：AI 預填的儲存格帶虛線邊框 + [AI] 小標籤，表示可覆蓋。
- **copy_constraints**:
  - MUST 標準名稱固定 (M1~M5)，不可修改。
  - 方案名稱截斷至 30 字元。

### Section: Accordion 7 -- Pre-CAD 審查 (Step 2.3)
- **layout**: 針對每個通過 MUST 的方案，展開 5 維度評分表 + 雷達圖。
- **visual_highlight**: Pre-CAD 5 維度雷達圖 (Recharts radar chart)。
- **elements**:
  - `Accordion 標題`: `accordion-header`, `required`, `"7. Pre-CAD 審查 (Step 2.3)" + 狀態 badge。`
  - `方案選擇器`: `tab/pill (Display)`, `required`, `僅顯示通過 MUST 的方案 (無任何 ❌)，可切換。淘汰方案不出現。`
  - `5 維度評分`:
    - `space_score (空間可行性)`: `slider (1-5)`, `required (★必填)`, `空間可行性評分。分數標籤：1=不可行 / 3=可行需調整 / 5=完全可行。`
    - `cost_score (成本合理性)`: `slider (1-5)`, `required (★必填)`, `成本合理性評分。分數標籤：1=嚴重超標 / 3=可接受 / 5=有餘裕。`
    - `safety_score (安全餘裕)`: `slider (1-5)`, `required (★必填)`, `安全餘裕評分。分數標籤：1=不達標 / 3=達標 / 5=大幅超標。`
    - `decoupling_score (解耦程度)`: `slider (1-5)`, `required (★必填)`, `解耦程度評分。分數標籤：1=高耦合 / 3=適度 / 5=完全解耦。`
    - `supply_score (供應鏈可行性)`: `slider (1-5)`, `required (★必填)`, `供應鏈可行性評分。分數標籤：1=無供應商 / 3=有替代 / 5=成熟供應鏈。`
  - `維度備註`: `textarea x 5`, `optional`, `每個維度的補充說明。`
  - `overall_pass`: `badge (Display)`, `required`, `所有分數 >= 3 → ✅ "通過" (綠底) / 否則 → ❌ "不通過" (紅底)。系統自動計算，不可手動修改。`
  - `雷達圖`: `radar-chart (Recharts)`, `Display`, `5 維度分數可視化。圓心 0，外圈 5。填充色半透明橙 (#F59E0B, opacity: 0.3)，線條橙實線。通過區域 (>=3) 以綠色虛線圈標記。`
  - `[AI 分析] 按鈕`: `button (secondary)`, `Agent`, `觸發 AI 分析此方案在 5 維度的優劣勢。結果顯示為灰底卡片 (#F8F9FA) + [AI] 標籤 + [採用] [重生成] 按鈕。`
  - `AI 分析結果`: `card (grey)`, `Agent`, `AI 分析產出，含每個維度的評語與建議。`
- **states**:
  - 正常：評分滑桿可互動，雷達圖即時更新 (Framer Motion 過渡動畫)。
  - loading：AI 分析中，卡片顯示 skeleton。
  - complete：所有通過 MUST 方案皆已評分。
  - overall-pass：overall_pass = true 的方案，卡片邊框變為綠色。
  - overall-fail：overall_pass = false 的方案，卡片邊框變為紅色 + 低分維度高亮紅色。
- **copy_constraints**:
  - 維度備註：最多 200 字元。
  - AI 分析結果：最多 800 字元。

### Section: Gate 檢查指示器
- **layout**: 頁面底部，雙層 Gate checklist。Gate 2.2 (Step Gate) 在上，Phase Gate 2 (Phase Gate, 雙線框強調) 在下。
- **input_category**: 必須呈現 (Display) -- 彩色徽章 + checklist
- **elements**:
  - `Gate 2.2 標題`: `h3`, `required`, `"Gate 2.2 -- 方案創造完整性" + Phase 2 橙色色帶。`
  - `Gate 2.2 Checklist`: `checklist-item (x2, Display)`, `required`:
    - `>=2 方案通過 MUST 快篩`: `check-item`, `Display`, `✅ / ❌。`
    - `robust_scores 已填寫`: `check-item`, `Display`, `✅ / ❌。`
  - `Gate 2.2 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ → "Gate 2.2 Passed" (綠色) / 否則 → "Gate 2.2 未通過" (紅色)。`
  - `Phase Gate 2 分隔`: `divider + milestone-bar`, `required`, `雙線框強調，Phase 2 橙色底帶。標題: "Phase Gate 2 (= Gate 2.3) -- Diverge 階段完成檢查"。`
  - `Phase Gate 2 Checklist`: `checklist-item (x1, Display)`, `required`:
    - `>=1 方案 Pre-CAD overall_pass = True`: `check-item`, `Display`, `✅ / ❌。`
  - `Phase Gate 2 狀態 badge`: `badge (Display)`, `required`, `✅ → "Phase 2 Passed" (綠色 + 星號) / 否則 → "Phase 2 未通過" (紅色)。`
  - `前往下一步按鈕`: `button (primary)`, `required`, `"通過 Phase Gate 2 → 進入 Review"。Phase Gate 2 通過時啟用 (背景橙轉綠)，否則禁用。`
- **states**:
  - all-passed: 兩個 Gate 皆通過，綠色 badge，按鈕啟用，Phase Gate 2 雙線框綠色高亮。
  - gate-2.2-passed-only: Gate 2.2 通過但 Phase Gate 2 未通過，按鈕禁用。
  - none-passed: 皆未通過，按鈕禁用。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入頁面，系統載入該專案已有的方案創造數據，自動展開第一個未完成的 Accordion。
  2. **Accordion 1 (Anti-Anchor)**：用戶閱讀 AI 路徑依賴警告，輸入 >=1 條非基準路線或採用 AI 建議。Gate 2.2.1 通過後自動展開 Accordion 2。
  3. **Accordion 2 (TRIZ)**：系統載入專案矛盾列表。針對每個矛盾，用戶切換 TC/PC/SF 三個 Tab，瀏覽 AI 建議解法，對每張卡片選擇採用/編輯/重生成/跳過。
  4. **Accordion 3 (子系統)**：AI 根據步驟 2 的採用解法建議受影響子系統，用戶確認勾選。
  5. **Accordion 4 (SCAMPER)**：系統為每個確認的子系統生成 7 種 SCAMPER 變體。用戶可採用變體或回饋新矛盾至 Accordion 2。
  6. **Accordion 5 (方案生成)**：系統彙整所有採用的解法/變體為方案卡片。用戶可手動新增或觸發 AI 整合生成。用戶必須填寫名稱、機制、關鍵假設 (★必填)。
  7. **Accordion 6 (MUST)**：用戶在 MUST 矩陣中標記每個方案的通過/失敗/邊際狀態。可選擇 AI 預填。
  8. **Accordion 7 (Pre-CAD)**：對通過 MUST 的方案進行 5 維度評分 (★必填 1-5 分)，雷達圖即時更新。可觸發 AI 分析。
  9. 頁面底部 Gate 2.2 + Phase Gate 2 checklist 自動更新。Phase Gate 2 通過後可導航至 Review 頁。

- **Progressive Disclosure 行為**：
  - Accordion 預設收合，依完成順序自動展開下一個 (Gate 2.2.1 通過 → 展開 Accordion 2)。
  - 已完成的 Accordion 標題右側顯示 [✅ 完成] badge，卡片內容預覽摘要。
  - 用戶可隨時手動展開/收合任何 Accordion (不限制順序，但首次建議依序)。

- **SCAMPER → TRIZ 回饋迴路**：
  - Accordion 4 的 [回饋新矛盾] 按鈕觸發：建立新矛盾 → 頁面 smooth scroll 至 Accordion 2 → 新矛盾高亮 (橙色脈衝動畫 2s) → AI 自動觸發 TRIZ 分析。

- **表單驗證規則**：
  - Accordion 1：`非基準路線` >= 1 條，每條名稱 + 簡述必填。
  - Accordion 2：每個矛盾至少有 1 個被採用的解法。
  - Accordion 3：至少 1 個子系統被確認。
  - Accordion 5：方案名稱 ★必填、機制 ★必填、關鍵假設 ★必填。
  - Accordion 6：所有方案 x 所有 MUST 標準的儲存格必須填寫。
  - Accordion 7：每個通過 MUST 方案的 5 個維度分數必填 (1-5)。

- **資料更新策略**：
  - 每個 Accordion 內的操作即時 auto-save (debounce 1s)。
  - Gate checklist 透過 React Query 輪詢 Gate API，每次 Accordion 操作後 invalidate + refetch。
  - SCAMPER 回饋新矛盾時，Accordion 2 矛盾列表自動刷新 (invalidate contradictions query)。

- **RWD 行為差異**：
  - Desktop (>1024px): Accordion 全寬展開。TRIZ 三路徑 Tab 水平排列。SCAMPER 7 欄網格。MUST 矩陣完整表格。雷達圖 300px。
  - Tablet (768px - 1023px): Accordion 全寬。TRIZ Tab 水平排列 (略窄)。SCAMPER 改為 4+3 兩行。MUST 矩陣可水平滾動。雷達圖 250px。
  - Mobile (<768px): Accordion 全寬。TRIZ Tab 改為下拉選單切換。SCAMPER 改為垂直卡片列表。MUST 矩陣轉為卡片式 (每方案一張卡片)。雷達圖 200px 居中。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - POST `/api/projects/:id/triz` — 觸發 TRIZ 矛盾分析 (body: `{ contradiction_id }`)，回傳 TC/PC/SF 解法建議。
  - POST `/api/projects/:id/scamper` — 觸發 SCAMPER 變形生成 (body: `{ subsystem_ids }`)。
  - GET `/api/projects/:id/alternatives` — 獲取方案集合列表。
  - POST `/api/projects/:id/alternatives` — 新增方案 (body: `{ name, mechanism, key_assumptions, source }`)。
  - PUT `/api/projects/:id/alternatives/:alt_id` — 更新方案資訊。
  - GET `/api/projects/:id/must` — 獲取 MUST 快篩結果。
  - POST `/api/projects/:id/must` — 提交 MUST 快篩評估 (body: `{ alternative_id, must_scores }`)。
  - GET `/api/projects/:id/pre-cad-reviews` — 獲取 Pre-CAD 審查列表。
  - POST `/api/projects/:id/pre-cad-reviews` — 新增 Pre-CAD 審查記錄 (body: `{ alternative_id, scores: { space, cost, safety, decoupling, supply } }`)。
  - PUT `/api/projects/:id/pre-cad-reviews/:review_id` — 更新 Pre-CAD 審查。
  - POST `/api/projects/:id/pre-cad-reviews/:review_id/ai-analyze` — 觸發 AI 分析 Pre-CAD 方案。
  - POST `/api/projects/:id/alternatives/ai-integrate` — 觸發 AI 整合生成方案集合。
  - GET `/api/projects/:id/gates/2.2/check` — 檢查 Gate 2.2 狀態。
  - GET `/api/projects/:id/gates/2.3/check` — 檢查 Phase Gate 2 (gate_id "2.3") 狀態。
- **response shape** (GET `/api/projects/:id/alternatives`):
  ```json
  {
    "alternatives": [
      {
        "id": "uuid",
        "name": "string",
        "mechanism": "string",
        "source": "triz_tc" | "triz_pc" | "triz_sf" | "scamper" | "manual" | "ai_integrated",
        "key_assumption_ids": ["uuid"],
        "robust_scores": { "score": 0.0, "filled": false },
        "must_result": "pass" | "fail" | "marginal" | null,
        "pre_cad_review": {
          "space_score": null,
          "cost_score": null,
          "safety_score": null,
          "decoupling_score": null,
          "supply_score": null,
          "overall_pass": null
        }
      }
    ]
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/2.3/check`):
  ```json
  {
    "gate_id": "2.3",
    "gate_type": "phase_gate",
    "passed": false,
    "checklist": [
      { "label": ">=1 方案 Pre-CAD overall_pass = True", "passed": false, "current": 0, "required": 1 }
    ]
  }
  ```
- **error cases**:
  - TRIZ / SCAMPER AI 生成失敗 (500): 顯示灰底錯誤卡片 + [重試] 按鈕，不阻塞流程。
  - AI 整合方案生成失敗 (500): toast "AI 整合失敗" + [重試]。用戶可手動新增。
  - Pre-CAD AI 分析失敗 (500): Toast 提示，用戶可手動填寫評分。
  - Gate API 查詢失敗 (500): Gate 指示器顯示 ⚠️ 載入失敗，提供重試。
  - 方案數據載入失敗 (500): Accordion 5 顯示錯誤提示 + 重試按鈕。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **Accordion 自動展開邏輯**: 本頁使用 Progressive Disclosure 自動展開下一個 Accordion，覆蓋 Global 預設的「所有 Accordion 手動操作」規則。原因：7 步驟流程需要引導用戶循序前進，降低認知負荷。
- **SCAMPER → TRIZ 回饋迴路**: 本頁允許 Accordion 4 回饋新矛盾至 Accordion 2，形成非線性流程。原因：SCAMPER 變形可能揭示新的技術矛盾，需要回到 TRIZ 重新分析。這是唯一允許 Accordion 間反向跳轉的互動模式。
- **MUST 矩陣行動端轉為卡片式**: 覆蓋 Global 的表格預設 RWD 行為 (水平滾動)，改用卡片式。原因：MUST 矩陣列數多，水平滾動體驗差，卡片式在行動端可讀性更佳。
- **三個 Gate 共存於同一頁**: 本頁同時包含 Gate 2.2.1 (Activity Gate, 行內)、Gate 2.2 (Step Gate)、Phase Gate 2 (Phase Gate)，為所有頁面中 Gate 數量最多者。Gate 2.2.1 以行內 badge 形式顯示在 Accordion 1 內部，Gate 2.2 和 Phase Gate 2 在頁面底部分層顯示。

## [ACCEPTANCE CRITERIA]
- [ ] 子步驟進度條正確反映 7 個 Accordion 的完成狀態 (✅/◉/○)，點擊節點可 scroll 至對應 Accordion。
- [ ] Accordion 1：AI 路徑依賴警告正常載入 (黃色 [AI] 卡片)。用戶可建立 >=1 非基準路線。Gate 2.2.1 行內指示器正常。
- [ ] Accordion 2：每個矛盾可切換 TC/PC/SF 三個 Tab。AI 解法卡片正常顯示 (灰底 + [AI] 標籤)。用戶可採用/編輯/重生成/跳過。
- [ ] Accordion 3：AI 建議子系統列表正常載入，用戶可勾選確認 (>=1 個)。
- [ ] Accordion 4：SCAMPER 變體卡片正常生成 (7 x N 網格)。[回饋新矛盾] 功能可 scroll 回 Accordion 2 並新增矛盾。
- [ ] Accordion 5：方案卡片正確顯示名稱、機制、來源 badge、關聯假設 chips、robust_scores。[手動新增] 和 [AI 整合生成] 功能正常。
- [ ] Accordion 6：MUST 矩陣可互動 (✅/❌/⚠️ 三態切換)，篩選摘要正確顯示通過/淘汰/待定數。[AI 預填] 功能正常。淘汰行灰底+刪除線。
- [ ] Accordion 7：5 維度評分滑桿可操作 (1-5)，雷達圖即時更新。overall_pass 自動計算 (all >= 3)。AI 分析功能正常。
- [ ] Gate 2.2 + Phase Gate 2 checklist 正確反映條件。Phase Gate 2 通過後「進入 Review」按鈕啟用。
- [ ] Progressive Disclosure：Accordion 依序自動展開，已完成標示 [✅ 完成] badge。
- [ ] RWD 在 Desktop / Tablet / Mobile 三種視口正確呈現 (TRIZ Tab→下拉、SCAMPER 7欄→垂直、MUST 表格→卡片)。

## [VERSION]
- **version**: v2.0
- **last_updated**: 2026-02-25
- **changelog**:
  - v1.0 — 初版建立
  - v2.0 — 對齊 6+1 架構 v2.0、Apple 設計哲學、命名規範 v1.1；新增 Gate 2.2.1 Activity Gate；新增 AI 預填 MUST、AI 整合生成方案、AI 生成非基準路線功能；TRIZ 3-path sub-tab 詳細規格化；Pre-CAD 雷達圖規格細化 (通過區域綠色虛線)；Phase Gate 2 雙線框強調樣式；API 端點新增 ai-integrate、ai-analyze；新增 response shape 範例
