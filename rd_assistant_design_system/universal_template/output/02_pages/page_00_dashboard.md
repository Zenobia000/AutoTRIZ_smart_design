# Page-Level Prompt: Dashboard

## [PAGE META]
- **page_name**: Dashboard
- **route_path**: `/projects` (專案列表) 及 `/projects/:id` (專案總覽)
- **page_type**: dashboard
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 提供專案總覽、Phase 進度追蹤、Quick Stats 統計，以及建立/選擇專案的統一入口。
- **secondary_goal**: 以 6+1 導航引導用戶快速進入對應功能頁面。

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管, 專案經理 (PM), 高階主管
- **entry_point**:
  - 登入後預設首頁 (`/projects`)。
  - 側邊導航欄點擊 Logo 或「Dashboard」圖示回到此頁。
  - 從任何功能頁的 breadcrumb 點擊專案名稱回到 `/projects/:id`。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 短 (1-3 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **專案列表區**
   - section_type: list + search
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: 提供搜尋、篩選、建立專案的入口，以卡片形式展示所有專案及其進度概覽。

2. **專案總覽區** (當選擇特定專案後顯示)
   - section_type: summary + stats
   - section_purpose: 展示選定專案的 Phase 進度條、8-Gate 通過狀態、Quick Stats 六維統計。

3. **6+1 導航區**
   - section_type: navigation
   - section_purpose: 以六個功能卡片 (Brief / Explore / Track / Create / Review / Decide) 引導用戶進入對應頁面，顯示各頁完成度。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: 專案列表區
- **layout**: 頂部搜尋列 + 篩選按鈕 + 新增按鈕，下方為響應式卡片網格 (Desktop: 3 欄, Tablet: 2 欄, Mobile: 1 欄)。
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - `搜尋框`: `input[type=search]`, `optional`, `輸入專案名稱或關鍵字即時篩選。placeholder: "搜尋專案..."。`
  - `篩選下拉`: `select`, `optional`, `依 Phase 狀態篩選: 全部 / Phase 1 / Phase 2 / Phase 3 / 已完成。`
  - `新增專案按鈕`: `button (primary)`, `required`, `點擊彈出 Modal，輸入專案名稱 ★必填 + 需求描述 ★必填 建立新專案。`
  - `專案卡片`: `card (repeating)`, `required`, `每張卡片顯示：專案名稱、建立日期、Phase 進度條 (三段色帶: 藍/橙/綠)、Gate 通過數 (如 "3/8 Gates")、點擊進入 /projects/:id。`
- **states**:
  - 正常：卡片列表正常顯示。
  - hover：卡片浮起 (box-shadow 加深, translateY(-2px))。
  - loading：卡片區域顯示 Skeleton 佔位。
  - empty：無專案時顯示空狀態插畫 + "建立你的第一個專案" CTA 按鈕。
  - error：API 載入失敗顯示錯誤提示 + 重試按鈕。
- **copy_constraints**:
  - 專案名稱: 卡片上最多顯示 40 字元，超出截斷加 `...`。
  - 搜尋框: placeholder 文字不超過 20 字元。

### Section: 專案總覽區
- **layout**: 上方為 Phase 進度條 (水平三段)，下方為 Quick Stats 六宮格。
- **elements**:
  - `Phase 進度條`: `custom-progress-bar (Display)`, `required`, `三段水平條，每段代表一個 Phase。Phase 1 藍 (#3B82F6)、Phase 2 橙 (#F59E0B)、Phase 3 綠 (#10B981)。每個 Step 以圖示表示狀態：✅ 已通過 (filled circle, phase color) / ◉ 進行中 (outlined circle, phase color, pulse animation) / ○ 未開始 (empty circle, #D1D5DB)。Step 標籤: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.2, 3.3。`
  - `Quick Stats 六宮格`: `stat-card-grid (Display)`, `required`, `六張 mini 統計卡片，每張包含：圖示 + 數值 + 標籤。六維度：矛盾數 (contradictions_count)、假設數 (assumptions_count)、方案數 (alternatives_count)、風險數 (risks_count)、實驗數 (experiments_count)、證據數 (evidence_items_count)。`
  - `Gate 通過摘要`: `badge-group (Display)`, `required`, `顯示 "X/8 Gates Passed" 搭配環形進度指示器 (Donut Chart)。`
- **states**:
  - 正常：進度條與統計卡片皆有數據。
  - loading：Skeleton 佔位替代進度條與統計卡片。
  - zero-data：新建專案，所有 Step 為 ○，所有統計為 0，顯示引導文字 "從 Brief 開始你的設計旅程"。
- **copy_constraints**:
  - Quick Stats 數值: 整數，最大顯示 9999+。
  - Step 標籤: 固定文字 "1.1" ~ "3.3"，不可自訂。

### Section: 6+1 導航區
- **layout**: 六張等寬導航卡片，水平排列 (Desktop: 6 欄, Tablet: 3x2, Mobile: 2x3 或 1x6 捲動)。
- **elements**:
  - `導航卡片 (x6)`: `nav-card (repeating)`, `required`, `每張卡片包含：頁面圖示 (Material Icon)、頁面英文名 (Brief / Explore / Track / Create / Review / Decide)、頁面中文名 (定義簡報 / 問題探索 / 假設追蹤 / 方案創造 / 設計審查 / 最終決策)、Phase 色帶 (卡片頂部 4px 色條)、完成度 badge (如 "2/3 done")。點擊導航至對應路由。未解鎖頁面 (前置 Gate 未通過) 顯示為半透明 + 鎖頭圖示 + tooltip 說明原因。`
- **states**:
  - 正常：可點擊，顯示完成度。
  - disabled：前置 Gate 未通過，半透明 (opacity: 0.5)，cursor: not-allowed。
  - hover：卡片底色加亮，色帶加粗。
  - active：當前所在頁面的卡片有選中態 (底框 + 色帶加粗)。
- **copy_constraints**:
  - 頁面名稱: 固定文字，不可自訂。
  - 完成度: 格式為 "X/Y done"，Y 為該頁包含的子步驟數。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶登入後進入 `/projects`，系統載入專案列表。
  2. 用戶可搜尋、篩選專案，或點擊「+ 新增專案」按鈕。
  3. 新增專案：彈出 Modal，填入專案名稱 ★必填 和需求描述 ★必填，確認後建立專案並自動導航至 `/projects/:id`。
  4. 點擊現有專案卡片，導航至 `/projects/:id`，載入專案總覽區和 6+1 導航區。
  5. 在專案總覽區查看 Phase 進度和 Quick Stats。
  6. 點擊 6+1 導航卡片進入對應功能頁面。

- **新增專案 Modal 驗證規則**：
  - `專案名稱`: 必填，最少 2 字元，最多 100 字元 → 紅色星號 ★ 標示。
  - `需求描述`: 必填，最少 10 字元，最多 1000 字元 → 紅色星號 ★ 標示。

- **資料更新策略**：
  - 專案列表: 進入頁面時 fetch，建立新專案後 invalidate query cache。
  - 專案總覽: 進入 `/projects/:id` 時 fetch，切換頁面回來時 refetch (staleTime: 30s)。
  - Quick Stats: 隨專案總覽一起載入，不另外請求。

- **RWD 行為差異**：
  - Desktop (>1024px): 專案卡片 3 欄網格，導航卡片 6 欄橫排，Phase 進度條完整顯示所有 Step 標籤。
  - Tablet (768px - 1023px): 專案卡片 2 欄，導航卡片 3x2，Phase 進度條縮為數字標籤。
  - Mobile (<768px): 專案卡片 1 欄，導航卡片水平捲動或 2x3 網格，Phase 進度條改為垂直堆疊。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects` — 取得專案列表 (支援 `?search=keyword` 和 `?phase=1|2|3` 查詢參數)。
  - POST `/api/projects` — 建立新專案 (body: `{ name: string, description: string }`)。
  - GET `/api/projects/:id` — 取得指定專案詳情，包含 phase_progress、gate_statuses、quick_stats。
- **response shape** (GET `/api/projects/:id`):
  ```json
  {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "phase_progress": {
      "1.1": "passed" | "in_progress" | "not_started",
      "1.2": "passed" | "in_progress" | "not_started",
      "1.3": "passed" | "in_progress" | "not_started",
      "2.1": "passed" | "in_progress" | "not_started",
      "2.2": "passed" | "in_progress" | "not_started",
      "2.3": "passed" | "in_progress" | "not_started",
      "3.2": "passed" | "in_progress" | "not_started",
      "3.3": "passed" | "in_progress" | "not_started"
    },
    "quick_stats": {
      "contradictions_count": 0,
      "assumptions_count": 0,
      "alternatives_count": 0,
      "risks_count": 0,
      "experiments_count": 0,
      "evidence_items_count": 0
    },
    "gates_passed": 0,
    "gates_total": 8
  }
  ```
- **error cases**:
  - 專案列表載入失敗 (500): 顯示全頁錯誤提示 + 重試按鈕。
  - 專案詳情載入失敗 (404): 導航回 `/projects`，顯示 toast "專案不存在"。
  - 建立專案失敗 (422): Modal 內顯示欄位級錯誤訊息。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **無內嵌 Gate**: Dashboard 為總覽頁，不對應任何 Step，因此不內嵌 Gate checklist。這是唯一一頁不包含 Gate 區塊的頁面。
- **雙路由共用頁面**: `/projects` 和 `/projects/:id` 共用同一頁面元件，以條件渲染切換列表模式與總覽模式，避免不必要的頁面跳轉。

## [ACCEPTANCE CRITERIA]
- [ ] 專案列表正確顯示所有專案，支援搜尋和篩選。
- [ ] 新增專案 Modal 的必填驗證正常運作，建立後自動導航至專案總覽。
- [ ] Phase 進度條正確顯示 8 個 Step 的三態圖示 (✅/◉/○) 及 Phase 色帶 (藍/橙/綠)。
- [ ] Quick Stats 六維統計數據正確顯示，新專案時全部為 0。
- [ ] 6+1 導航卡片正確渲染，未解鎖頁面顯示 disabled 態並提示原因。
- [ ] RWD 在 Desktop / Tablet / Mobile 三個斷點下佈局正確。
- [ ] 空專案狀態有引導性空狀態設計。
