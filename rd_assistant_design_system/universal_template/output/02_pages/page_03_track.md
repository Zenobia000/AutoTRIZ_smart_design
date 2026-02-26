# Page-Level Prompt: Track -- 假設追蹤

## [PAGE META]
- **page_name**: Track -- 假設追蹤
- **route_path**: `/projects/:id/track`
- **page_type**: tabs (2 tabs)
  <!-- landing / form / dashboard / report / search / detail / settings / accordion / tabs -->
- **primary_goal**: 以 Kanban 拖拉板管理假設生命週期 (未驗證→驗證中→已驗證→已否定)，並維護未知集合 U，確保所有高風險假設在進入方案創造前有對應驗證規劃。
- **secondary_goal**: 透過 AI 自動提取假設與發現未知因素，降低認知盲區，建立假設→實驗的數位線索。
- **phase**: Phase 2 Diverge (#F59E0B 橙)
- **steps**: Step 2.1
- **embedded_gates**: Gate 2.1 (Step Gate)

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管
- **entry_point**:
  - 從「問題探索 (Explore)」頁面 Phase Gate 1 通過後點擊「前往 Track →」導航進入。
  - 從 Dashboard 的 6+1 導航區點擊「Track」卡片進入。
  - 從 Create 頁面的 breadcrumb 點擊「Track」返回。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (15-30 分鐘)
  <!-- 假設管理需要反覆回顧、拖拉排序、AI 質疑，用戶會在此頁停留較長時間 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **Tab 導航列**
   - section_type: tabs
   - section_purpose: 切換兩個子功能 — 假設台帳 (Kanban) / 未知集合 U。

2. **Tab A: 假設台帳 (Assumption Kanban)** (Step 2.1)
   - section_type: kanban-board (dnd-kit)
   - section_purpose: 以四欄拖拉板管理所有假設的驗證生命週期，視覺化風險分佈，連結實驗計畫。

3. **Tab B: 未知集合 U** (Step 2.1)
   - section_type: list + form
   - section_purpose: 記錄尚未被假設化的未知因素，追蹤其發現階段與潛在影響，連結相關假設。

4. **Gate 區** (Display)
   - section_type: gate-indicator (inline)
   - section_purpose: Gate 2.1 checklist 內嵌於頁面底部，顯示通過條件。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: Tab 導航列
- **layout**: 水平 Tab bar，兩個 Tab，底部線條指示當前 Tab。Phase 2 橙色主題 (#F59E0B)。
- **elements**:
  - `Tab A`: `tab-button`, `required`, `"假設台帳" + 假設總數 badge (如 "12")。`
  - `Tab B`: `tab-button`, `required`, `"未知集合 U" + 未知因素數量 badge (如 "4")。`
- **states**:
  - active: 選中 Tab 有底部橙色條 (#F59E0B, 3px)，文字加粗。
  - inactive: 灰色文字 (#6c757d)。
  - badge-highlight: 當 Tab 內有新數據 (如 AI 新增假設/未知) 時 badge 顯示圓點通知。

### Section: Tab A -- 假設台帳 (Assumption Kanban)
- **layout**: 上方為操作工具列 (篩選 + 新增 + AI 按鈕)，中央為四欄 Kanban 拖拉板 (dnd-kit)，每欄等寬水平排列。
- **visual_highlight**: Kanban 四欄拖拉板 -- 假設生命週期視覺化 (dnd-kit drag & drop)。
- **elements**:
  - `風險等級篩選`: `filter-pills`, `optional`, `三個切換按鈕：全部 / High (紅) / Medium (橙) / Low (綠)。預設選中 "全部"。`
  - `搜尋框`: `input[type=search]`, `optional`, `即時篩選假設卡片。placeholder: "搜尋假設..."。`
  - `[+ 新增假設] 按鈕`: `button (secondary)`, `required`, `點擊彈出 Modal，填入假設內容 ★必填 + 風險等級 ★必填 + 來源說明 (optional)。新假設預設放入「未驗證」欄。`
  - `[AI 質疑假設] 按鈕`: `button (secondary)`, `Agent`, `觸發 AI 針對每個假設生成挑戰性問題，結果顯示為假設卡片上的灰底子卡片。附 [AI] 標籤。`
  - `Kanban 欄位 x 4`:
    - `未驗證 (Draft)`: `kanban-column`, `required`, `標題: "未驗證" + 卡片數量 badge。頂部橙色色帶 (#F59E0B, 4px)。`
    - `驗證中 (Testing)`: `kanban-column`, `required`, `標題: "驗證中" + 卡片數量 badge。頂部藍色色帶 (#3B82F6, 4px)。`
    - `已驗證 (Verified)`: `kanban-column`, `required`, `標題: "已驗證" + 卡片數量 badge。頂部綠色色帶 (#10B981, 4px)。`
    - `已否定 (Killed)`: `kanban-column`, `required`, `標題: "已否定" + 卡片數量 badge。頂部紅色色帶 (#dc3545, 4px)。`
  - `假設卡片 (repeating)`: `kanban-card (draggable)`, `required`, `每張卡片包含：`
    - `assumption_code`: `badge (Display)`, `required`, `自動生成編號 (如 "A-001")，不可修改。`
    - `content`: `text`, `required`, `假設內容描述，最多 2 行截斷 + 展開。`
    - `risk_level badge`: `badge (★必填)`, `required`, `H = 紅底白字 (#dc3545) / M = 橙底白字 (#F59E0B) / L = 綠底白字 (#10B981)。`
    - `linked_experiments count`: `chip (Display)`, `required`, `"Exp: N" 顯示關聯實驗數。N=0 且 risk_level=H 時紅色警告態。`
    - `AI 質疑子卡片`: `sub-card (grey, collapsible)`, `Agent`, `灰底 (#F8F9FA) + [AI] 標籤，顯示 AI 針對此假設的挑戰性問題。預設收合，點擊展開。`
  - `卡片點擊展開面板`: `slide-over-panel`, `optional`, `卡片點擊後從右側滑入詳情面板 (Desktop: Drawer 400px / Mobile: bottom sheet 60vh)，顯示完整假設內容、歷史變更、關聯實驗列表、AI 質疑詳情。`
- **states**:
  - 正常：四欄 Kanban 正常顯示，卡片可拖拉。
  - dragging：被拖動的卡片半透明 (opacity: 0.7) + 陰影加深，目標欄位高亮 (橙色虛線框 2px)。
  - drop-success：卡片落入新欄位後，輕微彈跳動畫 (Framer Motion spring)，同時自動 PUT 更新狀態。
  - loading：Kanban 區域顯示 Skeleton 佔位 (4 欄骨架)。
  - empty：無假設時顯示引導文字 "尚無假設。從 Explore 頁面的問答中標記，或點擊 [+ 新增假設] 開始" + CTA 按鈕。
  - ai-loading：[AI 質疑假設] 按鈕 loading 態，卡片上的 AI 子卡片逐一顯示 skeleton。
  - filter-active：篩選啟用時，不符合條件的卡片淡出 (opacity: 0.3)。
  - empty-column：個別欄位無卡片時顯示虛線框 + "拖拉假設至此" 提示。
- **copy_constraints**:
  - 假設內容：最少 5 字元，最多 300 字元。
  - 卡片上截斷：2 行 (約 80 字元)，超出顯示 "..."。
  - AI 質疑問題：最多 500 字元。
  - assumption_code：自動生成 "A-XXX" 格式，不可修改。

### Section: Tab B -- 未知集合 U
- **layout**: 上方為操作工具列 (新增 + AI 按鈕)，下方為表格式列表 (React Table)。
- **elements**:
  - `[+ 新增未知] 按鈕`: `button (secondary)`, `required`, `點擊展開行內新增表單，填入：名稱 ★必填 + potential_impact ★必填 (High/Medium/Low 下拉) + 描述 (optional)。`
  - `[AI 發現未知] 按鈕`: `button (secondary)`, `Agent`, `觸發 AI 根據現有矛盾與假設分析潛在未知因素。結果以灰底卡片列表顯示，每張卡片附 [AI] 標籤 + [採用] [跳過] 按鈕。`
  - `未知因素表格`: `data-table (React Table)`, `required`, `欄位：`
    - `unknown_code`: `text (Display)`, `required`, `自動生成 "U-XX" 編號。`
    - `name`: `text`, `required`, `未知因素名稱。`
    - `description`: `text (expandable)`, `optional`, `詳細描述，預設截斷 1 行。`
    - `discovery_phase`: `badge (Display)`, `required`, `發現階段：Phase 1 (藍 #3B82F6) / Phase 2 (橙 #F59E0B) / Phase 3 (綠 #10B981)，系統根據建立時間自動判斷。`
    - `potential_impact`: `badge (★必填)`, `required`, `High = 紅 badge (#dc3545) / Medium = 橙 badge (#F59E0B) / Low = 綠 badge (#10B981)。`
    - `assumption_refs`: `chip-group (Display)`, `optional`, `關聯的假設編號 (如 "A-001", "A-003")，可點擊跳轉至 Tab A 對應卡片。`
    - `actions`: `button-group`, `required`, `[編輯] (ghost) / [刪除] (ghost, red) / [轉為假設] (accent, 橙底白字)。`
  - `AI 建議卡片列表 (Agent)`: `agent-card-list`, `Agent`, `灰底 (#F8F9FA) + [AI] 標籤。每張卡片包含：建議的未知因素名稱 + 分析理由 + 潛在影響等級。[採用] 按鈕將其加入未知集合表格，[跳過] 按鈕移除卡片。`
- **states**:
  - 正常：表格正常顯示，操作按鈕可用。
  - loading：表格顯示 Skeleton 佔位列。
  - empty：無未知因素時顯示 "尚未記錄未知因素。點擊 [AI 發現未知] 讓 AI 分析潛在盲區" + CTA。
  - ai-loading：AI 分析中，建議區顯示 skeleton 卡片。
  - editing-row：編輯中的列高亮 (淡橙色底 #FEF3C7)，其餘列半透明。
- **copy_constraints**:
  - 未知因素名稱：最少 2 字元，最多 100 字元。
  - 描述：最多 500 字元。
  - unknown_code：自動生成 "U-XX" 格式，不可修改。
  - AI 建議理由：最多 300 字元。

### Section: Gate 區 (Display)
- **layout**: 頁面底部嵌入，水平分隔線下方。Gate 2.1 (Step Gate) 以橙色 (#F59E0B) 色帶標示。
- **input_category**: 必須呈現 (Display) -- 彩色徽章 + checklist
- **elements**:
  - `Gate 2.1 標題`: `h3`, `required`, `"Gate 2.1 -- 假設驗證規劃完整性" + Phase 2 橙色色帶。`
  - `Gate 2.1 Checklist`: `checklist-item (x2, Display)`, `required`, `(1) >=3 高風險假設已識別 (✅/❌) / (2) 每個高風險假設有 >=1 對應 Experiment (✅/⚠️/❌)。`
  - `Gate 2.1 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ → "Gate 2.1 Passed" (綠色 #28a745) / 否則 → "Gate 2.1 未通過" (紅色 #dc3545)。`
  - `前往下一步按鈕`: `button (primary)`, `required`, `"前往 Create →"。Gate 2.1 通過時啟用，否則禁用 (opacity: 0.5, cursor: not-allowed) + tooltip "請完成上方所有檢查項目"。`
- **states**:
  - passed: Gate 通過，綠色 badge，按鈕啟用，色帶上方顯示 ✅ 圖示。
  - not-passed: Gate 未通過，紅色 badge，按鈕禁用，checklist 項目顯示 ❌ 或 ⚠️。
  - partial: 部分條件通過，⚠️ 橙色 badge，按鈕禁用。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入 Track 頁面，預設顯示 Tab A (假設台帳)。
  2. 系統載入專案已有假設 (從 Explore 頁面標記 + 手動新增)，按 verification_status 分佈到四欄 Kanban。
  3. 用戶可拖拉假設卡片在四欄間移動，代表驗證狀態變更 (Direct Manipulation)。
  4. 用戶對每張假設卡片設定風險等級 ★必填 (H/M/L)。
  5. 用戶點擊 [AI 質疑假設] 按鈕，AI 對每個假設生成挑戰性問題，結果以子卡片形式附著在假設卡片上。
  6. 用戶可點擊假設卡片展開右側詳情面板，查看完整資訊、關聯實驗、歷史記錄。
  7. 切換至 Tab B (未知集合 U)，查看/新增/管理未知因素。
  8. 用戶點擊 [AI 發現未知]，AI 分析潛在未知因素，用戶選擇採用或跳過。
  9. 未知因素可透過 [轉為假設] 按鈕轉換為假設，自動出現在 Tab A 的「未驗證」欄。
  10. 頁面底部 Gate 2.1 即時更新檢查狀態，通過後可導航至 Create 頁。

- **Kanban 拖拉行為** (dnd-kit):
  - 拖動開始：卡片抬起 (scale: 1.05, shadow 加深)，原位留下半透明佔位 (opacity: 0.3)。
  - 拖動中：卡片跟隨游標/手指，經過目標欄時欄位邊框高亮 (橙色虛線 2px)。
  - 拖放完成：卡片落入新欄位，彈跳動畫 (Framer Motion spring)，自動 PUT 更新 verification_status (optimistic update)。
  - 拖放取消 (ESC / 拖到欄外)：卡片回到原位，無 API 請求。
  - 同欄內拖拉：支援卡片排序 (改變 sort_order)。
  - Mobile：觸控長按啟動拖拉，或改為點擊卡片→選擇目標狀態下拉。

- **跨 Tab 數據流**：
  - Tab B [轉為假設] → POST 建立新 assumption → Tab A「未驗證」欄自動出現新卡片。
  - Tab A 假設的 assumption_refs → Tab B 表格 `assumption_refs` 列自動更新。

- **Auto-Save 策略**：
  - Kanban 拖拉：drop 完成後立即 PUT (optimistic update，失敗則 rollback)。
  - 風險等級變更：onSelect 後立即 PUT。
  - 詳情面板編輯：onBlur debounce 1.5s PUT。
  - 未知因素編輯：onBlur debounce 1.5s PUT。
  - 新增假設/未知：Modal/行內表單提交後 POST。

- **表單驗證規則**：
  - 新增假設 Modal：`content` 必填 (最少 5 字元)，`risk_level` 必填 (H/M/L 選擇)。
  - 新增未知因素：`name` 必填 (最少 2 字元)，`potential_impact` 必填 (H/M/L 選擇)。
  - 風險等級：卡片上紅色星號 ★ 標示，未選擇時卡片邊框紅色警告。

- **資料更新策略**：
  - 假設列表：進入頁面時 fetch，Kanban 操作後 optimistic update + PUT。staleTime: 30s。
  - 未知因素列表：切換至 Tab B 時 fetch。staleTime: 30s。
  - Gate checklist：每次 Kanban 操作或 Tab 切換時 refetch Gate API (GET /api/projects/:id/gates/2.1/check)。
  - AI 質疑結果：觸發後 fetch，結果附著在對應假設上，存入 React Query cache。

- **RWD 行為差異**：
  - Desktop (>1024px): Kanban 四欄水平排列，每欄等寬 (~25%)。詳情為右側 Drawer (400px)。未知因素為完整表格。
  - Tablet (768px - 1023px): Kanban 四欄略窄，卡片內容截斷更短。詳情為底部 Sheet (60vh)。表格可水平滾動。
  - Mobile (<768px): Kanban 轉為水平可捲動的單列模式 (每欄佔 80% 寬度，左右滑動切換)，或改為狀態篩選 Tab + 垂直卡片列表。拖拉改為點擊+下拉選單。詳情為全螢幕 Sheet。未知因素表格轉為卡片列表。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/assumptions` — 取得假設列表 (含 verification_status, risk_level, linked_experiments)。
  - POST `/api/projects/:id/assumptions` — 新增假設 (body: `{ content, risk_level, source }`)。
  - PUT `/api/projects/:id/assumptions/:assumption_id` — 更新假設 (驗證狀態拖拉、風險等級、內容編輯)。
  - DELETE `/api/projects/:id/assumptions/:assumption_id` — 刪除假設。
  - POST `/api/projects/:id/assumptions/ai-challenge` — 觸發 AI 質疑假設，回傳每個假設的挑戰性問題。
  - GET `/api/projects/:id/unknown-factors` — 取得未知因素列表。
  - POST `/api/projects/:id/unknown-factors` — 新增未知因素 (body: `{ name, potential_impact, description }`)。
  - PUT `/api/projects/:id/unknown-factors/:factor_id` — 更新未知因素。
  - DELETE `/api/projects/:id/unknown-factors/:factor_id` — 刪除未知因素。
  - POST `/api/projects/:id/unknown-factors/ai-discover` — 觸發 AI 發現未知因素。
  - POST `/api/projects/:id/unknown-factors/:factor_id/convert-to-assumption` — 將未知因素轉為假設。
  - GET `/api/projects/:id/gates/2.1/check` — 檢查 Gate 2.1 通過狀態。
- **response shape** (GET `/api/projects/:id/assumptions`):
  ```json
  {
    "assumptions": [
      {
        "id": "uuid",
        "assumption_code": "A-001",
        "content": "string",
        "risk_level": "H" | "M" | "L" | null,
        "verification_status": "draft" | "testing" | "verified" | "killed",
        "sort_order": 0,
        "source": "socratic_qa" | "manual" | "unknown_factor_conversion",
        "linked_experiments_count": 0,
        "linked_experiment_ids": ["uuid"],
        "created_at": "2026-02-25T10:00:00Z",
        "updated_at": "2026-02-25T10:00:00Z"
      }
    ],
    "stats": {
      "total": 12,
      "high_risk_count": 3,
      "high_risk_with_experiment": 1,
      "by_status": { "draft": 5, "testing": 3, "verified": 3, "killed": 1 }
    }
  }
  ```
- **response shape** (GET `/api/projects/:id/unknown-factors`):
  ```json
  {
    "unknown_factors": [
      {
        "id": "uuid",
        "unknown_code": "U-01",
        "name": "string",
        "description": "string | null",
        "discovery_phase": "Phase 1" | "Phase 2" | "Phase 3",
        "potential_impact": "H" | "M" | "L",
        "assumption_refs": ["A-001", "A-003"],
        "created_at": "2026-02-25T10:00:00Z"
      }
    ]
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/2.1/check`):
  ```json
  {
    "gate_id": "2.1",
    "passed": false,
    "checklist": [
      { "label": ">=3 高風險假設已識別", "passed": true, "current": 4, "required": 3 },
      { "label": "每個高風險假設有對應 Experiment", "passed": false, "current": 1, "required": 4 }
    ]
  }
  ```
- **error cases**:
  - 假設列表載入失敗 (500): Kanban 顯示全區錯誤提示 + [重試] 按鈕。
  - 假設拖拉 PUT 失敗 (500): 卡片自動回到原欄位 (optimistic rollback) + toast "狀態更新失敗，請重試"。
  - AI 質疑失敗 (500): toast "AI 質疑生成失敗" + [重試] 按鈕，不阻塞流程。
  - AI 發現未知失敗 (500): 建議區顯示 "AI 分析失敗" + [重試] 按鈕。
  - 未知因素轉假設失敗 (500): toast "轉換失敗，請重試"。
  - Gate API 查詢失敗 (500): Gate 指示器顯示 ⚠️ 載入失敗，提供重試。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **Kanban 拖拉使用 dnd-kit**: 此頁為唯一使用 dnd-kit 拖拉排序的頁面，需額外安裝 `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities`。其他頁面不使用 Kanban 模式。
- **Mobile Kanban 轉為水平捲動/下拉選單**: 在 Mobile 斷點下，四欄 Kanban 轉為水平可捲動的單列模式或狀態篩選+垂直列表，偏離 Global 的「Mobile-first 垂直堆疊」原則。原因：四欄並排在小螢幕下不可讀，但完全垂直堆疊會失去 Kanban 的欄位對比語意。
- **Optimistic Update 拖拉操作**: Kanban 拖拉使用 optimistic update (先更新 UI 再發 PUT)，偏離 Global 的「API 成功後才更新 UI」策略。原因：拖拉操作需要即時反饋，等待 API 回應會造成明顯延遲感。失敗時自動 rollback。

## [ACCEPTANCE CRITERIA]
- [ ] Kanban 四欄 (未驗證/驗證中/已驗證/已否定) 正確顯示，假設卡片按 verification_status 分佈。
- [ ] 假設卡片可拖拉至不同欄位，拖放後自動更新 verification_status (PUT API)。
- [ ] 假設卡片正確顯示 assumption_code、content、risk_level badge (H紅/M橙/L綠)、linked_experiments count。
- [ ] 風險等級為 ★必填，未設定時卡片邊框紅色警告。
- [ ] [AI 質疑假設] 觸發 AI 生成挑戰性問題，結果以灰底 [AI] 子卡片附著在假設卡片上。
- [ ] [+ 新增假設] Modal 驗證正常 (content ★必填, risk_level ★必填)。
- [ ] 未知集合 U 表格正確顯示 unknown_code、name、discovery_phase badge、potential_impact badge、assumption_refs chips。
- [ ] [AI 發現未知] 觸發 AI 分析，結果以灰底 [AI] 卡片顯示，用戶可 [採用] / [跳過]。
- [ ] [轉為假設] 按鈕可將未知因素轉換為假設，自動出現在 Tab A「未驗證」欄。
- [ ] Gate 2.1 checklist 即時反映：(1) >=3 高風險假設 (2) 每個高風險假設有 >=1 Experiment。
- [ ] Gate 2.1 通過後「前往 Create →」按鈕啟用。
- [ ] RWD 在 Desktop 四欄 Kanban / Tablet 窄欄可捲動 / Mobile 水平捲動或下拉模式正確呈現。
- [ ] 拖拉失敗時卡片自動回到原欄位 (optimistic update rollback)。

## [VERSION]
- **version**: v2.0
- **last_updated**: 2026-02-25
- **changelog**:
  - v1.0 — 初版建立
  - v2.0 — 對齊 6+1 架構 v2.0、Apple 設計哲學、命名規範 v1.1；重寫 Kanban 欄位命名 (未驗證/驗證中/已驗證/已否定)；新增 AI 質疑假設 Agent 功能；新增未知集合 U 的 [轉為假設] 功能；Gate 2.1 條件精簡為 2 項；API 新增 ai-challenge、ai-discover、convert-to-assumption 端點
