# Page-Level Prompt: Explore -- 問題探索

## [PAGE META]
- **page_name**: Explore -- 問題探索
- **route_path**: `/projects/:id/explore`
- **page_type**: tabs (3 Tabs)
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 透過索克拉底式問答窮盡問題空間，識別技術矛盾 (TC) 與物理矛盾 (PC)，並建構因果迴路圖 (CLD) 以視覺化系統動態關係。
- **secondary_goal**: AI 自動從問答中萃取假設與矛盾，建立跨頁面的數位線索連結 (Assumption → Track, Contradiction → Create)。
- **mapped_step**: Step 1.2 理解全貌 + Step 1.3 系統建模
- **embedded_gate**: Gate 1.2 + Phase Gate 1 (= Gate 1.3)
- **phase_color**: Phase 1 藍色 (#3B82F6)

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管, 專案經理 (PM)
- **entry_point**:
  - 從 Brief 頁面通過 Gate 1.1 後點擊「通過 → 進入 Explore」導航進入 (主要入口)。
  - 從 Dashboard 的 6+1 導航區點擊「Explore」卡片進入。
  - 從 Track 頁面的 breadcrumb 點擊「Explore」返回。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (15-45 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->
- **user_mindset**: 用戶正處於質疑與發現的心態，需要被引導深入探索設計問題的本質，同時擔心遺漏關鍵面向。

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **Tab 導航列**
   - section_type: tabs
   - section_purpose: 在索克拉底問答、矛盾識別、因果迴路圖三個子步驟之間切換。

2. **Tab A: 索克拉底問答** (Step 1.2)
   - section_type: form + agent-card (list)
   - section_purpose: AI 生成 5W1H / 多角度問題，用戶逐一回答，AI 追問或摘要，窮盡問題空間並萃取假設。

3. **Tab B: 矛盾識別** (Step 1.2)
   - section_type: agent-card (list) + form
   - section_purpose: AI 從索克拉底問答中自動識別技術矛盾 (TC) 與物理矛盾 (PC)，用戶確認、修改或新增。矛盾卡片以「改善參數 vs 惡化參數」格式呈現。

4. **Tab C: 因果迴路圖 (CLD)** (Step 1.3)
   - section_type: interactive-graph + form
   - section_purpose: AI 生成因果迴路圖，用戶在 ReactFlow 互動畫布中探索節點關係，標記關鍵斷路點 (Breakpoints)。

5. **Gate 1.2 Checklist** (Display)
   - section_type: gate-indicator (inline)
   - section_purpose: 內嵌於頁面底部，以 Step Gate 樣式檢查 Step 1.2 完成條件。

6. **Phase Gate 1 Checklist** (Display)
   - section_type: gate-indicator (inline, milestone)
   - section_purpose: 內嵌於 Gate 1.2 下方，以醒目里程碑樣式 (雙線框) 檢查 Phase 1 完成條件，通過後解鎖 Phase 2: Diverge。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: Tab 導航列
- **layout**: 水平 Tab 列，固定於內容區頂部。三個 Tab 等寬排列，當前 Tab 以 Phase 1 藍色 (#3B82F6) 底線高亮。
- **elements**:
  - `Tab A`: `tab-button`, `required`, `"索克拉底問答" -- 圖示: quiz (Material Icon)。預設選中。`
  - `Tab B`: `tab-button`, `required`, `"矛盾識別" -- 圖示: compare_arrows (Material Icon)。`
  - `Tab C`: `tab-button`, `required`, `"因果迴路圖" -- 圖示: account_tree (Material Icon)。`
  - `Tab badge (x3)`: `badge (Display)`, `optional`, `每個 Tab 右上角顯示該步驟的完成度 badge。Tab A: "X/Y 已回答"。Tab B: "X TC + Y PC"。Tab C: "X 斷路點"。`
- **states**:
  - active: 當前 Tab 有 Phase 1 藍色底線 (border-bottom: 3px solid #3B82F6)，文字加粗。
  - inactive: 灰色文字 (#6c757d)，hover 時底色微亮 (#F8F9FA)。
  - badge-update: 當 Tab 內有新數據時 badge 短暫閃爍 (Framer Motion pulse, 0.3s)。
- **copy_constraints**:
  - Tab 名稱: 固定文字，不可自訂。

### Section: Tab A -- 索克拉底問答
- **layout**: 垂直卡片列表，每張卡片為一組問答對。頂部有問題計數器 + 類別篩選。底部有「AI 生成更多問題」和「完成問答」按鈕。
- **input_category**: 混合 -- 問題為 Agent 處理 (灰底 + [AI])，回答為必填 (白底 + ★)
- **elements**:
  - `Section 標題`: `h2`, `required`, `"索克拉底問答 -- AI 引導式問題探索"`
  - `問題計數器`: `badge (Display)`, `required`, `"已回答 X / Y 題" -- 即時更新。Phase 1 藍色底。`
  - `類別篩選按鈕組`: `filter-buttons (Display)`, `optional`, `水平排列六個 pill 按鈕，對應 5W1H 六類。點擊篩選顯示該類問題。全選時顯示所有。`
  - `問題卡片 (repeating)`: `question-card`, `required`, `每張卡片結構：`
    - `(1) AI 問題區 (Agent)`: 灰底 (#F8F9FA) + [AI] badge + 問題類別 badge。問題類別色彩: Who=#3B82F6 (藍), What=#8B5CF6 (紫), Where=#EC4899 (粉), When=#F59E0B (橙), Why=#10B981 (綠), How=#6366F1 (靛)。
    - `(2) 用戶回答輸入框 (★必填)`: 白底 textarea + 紅色星號 ★。placeholder: "請在此輸入您的回答..."。min-height: 60px, auto-grow。
    - `(3) AI 追問區 (Agent)`: 灰底，AI 根據用戶回答生成追問。顯示 [回答追問] / [跳過] 按鈕。
    - `(4) 追問回答框 (選填)`: 白底 textarea (無紅色星號)。僅在用戶點擊 [回答追問] 後展開。
  - `AI 生成更多問題按鈕`: `button (secondary)`, `optional`, `"AI 生成更多問題 [AI]" -- 點擊後 AI 根據已有回答生成新問題卡片。`
  - `完成問答按鈕`: `button (primary)`, `optional`, `"完成問答 → 進入矛盾識別" -- 點擊後自動切換到 Tab B 並觸發 AI 矛盾識別。`
- **states**:
  - loading: 問題卡片區域顯示 skeleton (3 張卡片骨架) + "AI 正在分析您的 Mission..."。
  - answering: 用戶正在回答某張卡片，該卡片邊框高亮 (box-shadow: 0 0 0 2px #3B82F6)。
  - answered: 卡片左側出現綠色確認邊線 (border-left: 3px solid #28a745)。
  - follow-up-pending: AI 追問區顯示 inline skeleton + "AI 正在分析您的回答..."。
  - follow-up-shown: 追問已生成，顯示追問文字 + [回答追問] / [跳過] 按鈕。
  - empty: 尚未生成任何問題，顯示空狀態插畫 + "請確認 Brief 已完成，AI 將自動生成問題" + CTA 按鈕 "生成問題"。
- **copy_constraints**:
  - AI 問題文字: 最多 300 字元。
  - 用戶回答: 最少 5 字元，最多 1000 字元。
  - AI 追問文字: 最多 200 字元。
  - 追問回答: 最多 500 字元 (選填)。

### Section: Tab B -- 矛盾識別
- **layout**: 頂部統計摘要列，中央為矛盾卡片列表，底部有「+ 手動新增矛盾」和「AI 重新識別」按鈕。
- **input_category**: 混合 -- 矛盾識別為 Agent 處理 (灰底 + [AI])，確認/修改為必填 (★)
- **elements**:
  - `Section 標題`: `h2`, `required`, `"矛盾識別 -- 技術矛盾 (TC) 與物理矛盾 (PC)"`
  - `統計摘要列`: `stat-bar (Display)`, `required`, `水平排列四個 badge: TC 數量 (藍底 #3B82F6) + PC 數量 (橙底 #F59E0B) + 總矛盾數 (灰底) + 已確認數 (綠底 #28a745)。`
  - `矛盾卡片 (repeating)`: `contradiction-card`, `required`, `每張卡片結構：`
    - `(1) 矛盾類型 badge`: "TC" 藍底圓角 或 "PC" 橙底圓角。
    - `(2) 改善參數`: 灰底區塊，顯示 TRIZ 39 參數名稱 + 編號 (如 "#14 強度")。TC 專用。
    - `(3) 惡化參數`: 灰底區塊，顯示 TRIZ 39 參數名稱 + 編號 (如 "#1 重量")。TC 專用。
    - `(4) PC 屬性對`: 灰底區塊，顯示 "需要: 屬性 A" + "同時需要: 非 A"。PC 專用。
    - `(5) 矛盾描述`: AI 生成的文字說明 (如 "增加結構強度會增加重量...")。
    - `(6) 操作按鈕組`: [確認 ★] (primary, small) / [編輯] (ghost, small) / [刪除] (ghost, danger, small)。
  - `確認按鈕 (★必填)`: `button (primary, small)`, `required`, `點擊後卡片狀態變為 "已確認"，左側邊線變綠，[AI] badge 消失，顯示 "已確認" badge。`
  - `編輯按鈕`: `button (ghost, small)`, `optional`, `點擊後卡片切換為編輯模式：改善/惡化參數切換為下拉選單 (TRIZ 39 參數)，描述切換為 textarea。出現 [儲存] / [取消] 按鈕。`
  - `刪除按鈕`: `button (ghost, danger, small)`, `optional`, `點擊後顯示確認 dialog "確定刪除此矛盾？此操作不可復原"，確認後刪除。`
  - `手動新增矛盾按鈕`: `button (ghost)`, `required`, `"+ 手動新增矛盾" -- 在列表底部插入空白矛盾卡片，用戶選擇 TC/PC 類型後填寫。`
  - `AI 重新識別按鈕`: `button (secondary)`, `optional`, `"AI 重新識別 [AI]" -- 根據最新問答重新觸發矛盾識別。已確認的矛盾不會被覆蓋。`
- **states**:
  - loading: 矛盾卡片區域顯示 skeleton (2 張卡片骨架) + "AI 正在分析問答識別矛盾..."。
  - unconfirmed: 卡片底色灰色 (#F8F9FA)，[AI] badge 可見，操作按鈕完整顯示。
  - confirmed: 卡片左側綠色邊線 (border-left: 3px solid #28a745)，[AI] badge 消失，顯示 "已確認" 綠色 badge。
  - editing: 卡片展開為編輯模式，參數欄位切換為 TRIZ 39 下拉選單。
  - empty: 無矛盾，顯示 "請先完成索克拉底問答，AI 將自動識別矛盾" + CTA 按鈕 "前往問答"。
- **copy_constraints**:
  - 矛盾描述: AI 生成，最多 500 字元，可編輯。
  - 改善/惡化參數: 必須從 TRIZ 39 參數清單中選擇 (TC 類型)。
  - PC 屬性 A / 非 A: 最少 2 字元，最多 100 字元 (PC 類型)。

### Section: Tab C -- 因果迴路圖 (CLD)
- **layout**: 上方為工具列，中央為 ReactFlow 互動式畫布 (佔頁面高度 60%)，畫布右側或下方為斷路點列表面板。
- **input_category**: 混合 -- CLD 圖為 Agent 處理 (灰底框 + [AI])，斷路點標記為必填 (★)
- **elements**:
  - `Section 標題`: `h2`, `required`, `"因果迴路圖 (Causal Loop Diagram)"`
  - `CLD 畫布 (Agent + Display)`: `ReactFlow canvas`, `required`, `互動式因果迴路圖。節點 (node): 圓角矩形 (#FFFFFF 底, 1px solid #e9ecef)，顯示變量名稱。邊 (edge): 帶箭頭連線。正回饋 (+): 藍色箭頭 (#3B82F6) + "+" label。負回饋 (-): 紅色箭頭 (#dc3545) + "-" label。畫布外框: 灰底 (#F8F9FA) + [AI] badge 表示 AI 生成。支援: 拖動節點、畫布平移、滾輪縮放。`
  - `節點資訊面板`: `side-panel (drawer)`, `optional`, `點擊節點後右側滑出面板 (Framer Motion slideIn, 0.3s)。面板內容: 變量名稱 / 相關假設列表 / 相關矛盾列表 / [設為斷路點 ★] 按鈕。`
  - `斷路點標記按鈕 (★必填)`: `button (warning)`, `required`, `在節點面板中點擊 "設為斷路點"。標記後: 節點外框變為紅色虛線 (border: 2px dashed #dc3545) + breakpoint 星號圖示 (★)。取消標記: 再次點擊切換回正常樣式。至少標記 3 個斷路點。`
  - `斷路點列表面板`: `list-panel (Display + 必填)`, `required`, `畫布下方的表格，顯示所有已標記的斷路點: 序號 / 變量名稱 / 標記理由 (★必填 textarea, min 10 chars) / 關聯矛盾 (下拉多選) / [取消標記] 按鈕。`
  - `工具列`: `toolbar (Display)`, `required`, `畫布左上角浮動工具列: 放大 (+) / 縮小 (-) / 適應螢幕 (fit) / 全螢幕 (expand)。`
  - `AI 重新生成 CLD 按鈕`: `button (secondary)`, `optional`, `"AI 重新生成 [AI]" -- 根據最新問答 + 矛盾重新生成 CLD。已有的斷路點標記會保留 (依變量名稱匹配)。`
  - `圖例`: `legend (Display)`, `required`, `畫布右下角浮動圖例: 正回饋 (+, 藍色箭頭) / 負回饋 (-, 紅色箭頭) / 斷路點 (紅色虛線 + ★)。`
- **states**:
  - loading: 畫布區域顯示大面積 skeleton + "AI 正在建構因果迴路圖..." 提示。
  - interactive: 節點可拖動、邊 hover 顯示 tooltip (回饋方向 + 連結的變量)。
  - node-selected: 選中節點有藍色外框光暈 (box-shadow: 0 0 0 3px rgba(59,130,246,0.4))，右側面板滑出。
  - breakpoint-marked: 斷路點節點有紅色虛線外框 + ★ icon，在畫布和列表中同步顯示。
  - empty: 無 CLD 數據，畫布顯示空狀態插畫 + "請先完成索克拉底問答和矛盾識別，AI 將自動生成因果迴路圖" + CTA 按鈕 "AI 生成因果迴路"。
- **copy_constraints**:
  - 節點名稱: 最多 30 字元。
  - 斷路點理由: ★必填，最少 10 字元，最多 300 字元。
  - CLD 節點數建議: ≤ 30 個節點。超過時 AI 自動摘要簡化。

### Section: Gate 1.2 Checklist (Display)
- **layout**: 頁面底部嵌入，水平分隔線上方，checklist 格式。Step Gate 樣式 (單線框 + Phase 1 藍色色帶)。
- **input_category**: 必須呈現 (Display) -- 彩色徽章 + 進度指示
- **elements**:
  - `Gate 標題`: `h3`, `required`, `"Gate 1.2 -- 問題空間探索完整性" + Phase 1 藍色色帶 (#3B82F6)。`
  - `Checklist 項目 (x3)`: `checklist-item (repeating, Display)`, `required`, `三項檢查：(1) 累計 ≥10 個假設/回答 (✅/⚠️/❌) -- 顯示 "X/10"。(2) 識別 ≥3 個已確認矛盾 (✅/⚠️/❌) -- 顯示 "X/3"。(3) 至少 3 項高風險項目已標記 (✅/⚠️/❌) -- 顯示 "X/3"。即時檢查，自動更新。⚠️ 表示部分達標 (如 2/3)。`
  - `Gate 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ → "Gate 1.2 Passed" (綠色 #28a745)；部分 ⚠️ → "Gate 1.2 待完善" (橙色 #F59E0B)；全部 ❌ → "Gate 1.2 未通過" (紅色 #dc3545)。`
- **states**:
  - all-passed: 三項皆 ✅，綠色 badge。
  - partial: 部分 ✅ 部分 ⚠️/❌，橙色 badge。
  - none: 三項皆 ❌，紅色 badge。
- **copy_constraints**:
  - Checklist 文字: 固定文字，不可自訂。

### Section: Phase Gate 1 Checklist (Display)
- **layout**: 緊接 Gate 1.2 下方，雙線框強調 (border: 2px solid #3B82F6)，里程碑標記樣式。背景微藍 (#EFF6FF)。左側有 Phase 1 藍色旗幟圖示。
- **input_category**: 必須呈現 (Display) -- 彩色徽章 + 里程碑指示
- **elements**:
  - `Phase Gate 標題`: `h3`, `required`, `"Phase Gate 1 -- Define 階段完成度檢查" + 左側旗幟圖示 (flag icon, #3B82F6)。雙線框。`
  - `Checklist 項目 (x3)`: `checklist-item (repeating, Display)`, `required`, `三項檢查：(1) 至少 1 個因果迴路圖已建立 (✅/❌)。(2) 至少 3 個斷路點已標記 (✅/❌) -- 顯示 "X/3"。(3) 所有矛盾已分類為 TC 或 PC (✅/❌) -- 顯示 "X/Y 已分類"。即時檢查。`
  - `Phase Gate 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ → "Phase Gate 1 Passed" (綠色 #28a745 + 旗幟圖示)；否則 → "Phase Gate 1 未通過" (紅色 #dc3545)。`
  - `前往 Phase 2 按鈕`: `button (primary, large)`, `required`, `"進入 Phase 2: Diverge →"。Gate 1.2 + Phase Gate 1 皆通過時啟用 (Phase 2 橙色 #F59E0B 底色)，未通過時禁用 (greyed out, opacity: 0.5) + tooltip "請完成 Phase 1 所有 Gate 條件"。`
- **states**:
  - all-passed: 三項皆 ✅ 且 Gate 1.2 也通過，綠色 badge，按鈕啟用 (橙色 Phase 2 配色)，旗幟 confetti 微動畫 (Framer Motion, 0.5s, 僅首次通過時播放)。
  - partial: 部分通過，紅色 badge，按鈕禁用。
  - none: 全部未通過，紅色 badge，按鈕禁用。
- **copy_constraints**:
  - Phase Gate 文字: 固定文字，不可自訂。
  - 按鈕文字: "進入 Phase 2: Diverge →" 固定。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶從 Brief 通過 Gate 1.1 進入 Explore 頁面，預設顯示 Tab A: 索克拉底問答。
  2. 系統自動根據 Brief 的 Mission + Constraints + KPI 觸發 AI 生成第一批問題 (5-8 題，涵蓋 5W1H 六類)。
  3. 用戶逐一回答問題 (★必填)。每回答一題，AI 可能生成 0-2 個追問。用戶可回答追問或點擊 [跳過]。
  4. 用戶可點擊「AI 生成更多問題」要求 AI 根據已有回答補充深度問題。
  5. 用戶點擊「完成問答 → 進入矛盾識別」或手動切換到 Tab B，系統自動觸發 AI 矛盾識別。
  6. Tab B: AI 從問答內容中識別矛盾 (TC/PC)，生成矛盾卡片。用戶逐一 [確認 ★] / [編輯] / [刪除]。可 [+ 手動新增矛盾]。
  7. 切換到 Tab C，系統自動根據問答 + 矛盾觸發 AI 生成因果迴路圖 (若尚未生成)。
  8. Tab C: CLD 互動式畫布載入。用戶點擊節點查看詳情面板，標記斷路點 (★必填至少 3 個) 並填寫理由。
  9. Gate 1.2 和 Phase Gate 1 Checklist 即時反映完成狀態。
  10. Gate 1.2 + Phase Gate 1 全部通過後，「進入 Phase 2: Diverge →」按鈕啟用 (橙色)。
  11. 用戶點擊按鈕，數據自動保存，導航至 `/projects/:id/track`。

- **跨 Tab 數據流**：
  - Tab A 回答 → Tab B AI 自動識別矛盾 (觸發時機: Tab 切換或手動點擊)。
  - Tab A 回答 → 自動萃取為假設 → Track 頁面 assumptions API 可見。
  - Tab B 確認的矛盾 → Tab C CLD 建模的輸入源。
  - Tab C 斷路點 → 連結到矛盾 (下拉多選關聯)。

- **Tab 切換行為**：
  - 切換 Tab 時自動保存當前 Tab 數據 (auto-save)。
  - Tab B 首次進入時，若問答數 ≥ 5 且尚無矛盾，自動觸發 AI 矛盾識別。
  - Tab C 首次進入時，若矛盾數 ≥ 1 且尚無 CLD，自動觸發 AI 生成 CLD。
  - 已生成過的 AI 產出，切換 Tab 不重新觸發 (除非用戶點擊 "AI 重新識別" / "AI 重新生成")。
  - URL hash 追蹤 Tab 狀態: `/projects/:id/explore#socratic`, `#contradictions`, `#cld`。

- **Auto-Save 策略**：
  - 問答回答: onBlur 或 debounce 3s 自動 PUT 儲存。
  - 矛盾確認/編輯: 操作後立即 PUT。
  - CLD 斷路點/理由: 操作後 debounce 2s PUT。
  - 儲存中顯示 "Saving..." 小型 indicator (右上角)。

- **表單驗證規則**：
  - 問答回答: 每題回答最少 5 字元。
  - 矛盾確認: TC 必須有 improving_parameter 和 worsening_parameter (TRIZ 39 下拉)；PC 必須填寫屬性 A 和非 A。
  - 斷路點: 至少 3 個節點被標記為斷路點，每個斷路點必須填寫理由 (≥ 10 字元)。

- **RWD 行為差異**：
  - Desktop (>1024px): Tab 水平排列，CLD 畫布佔 60% 高度，節點面板右側滑出 drawer。
  - Tablet (768px - 1023px): Tab 水平排列，CLD 畫布佔 50% 高度，節點面板底部滑出。
  - Mobile (<768px): Tab 改為水平捲動 pill 按鈕 (避免三個 Tab 擠壓)。CLD 畫布全寬且有「全螢幕」按鈕置頂。節點面板改為 bottom sheet。問答卡片全寬堆疊。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/questions` -- 取得索克拉底問題列表 (含用戶回答與追問)。
  - POST `/api/projects/:id/questions` -- AI 生成新問題 / 用戶觸發追問生成。
  - PUT `/api/projects/:id/questions/:qid` -- 更新單題回答。
  - GET `/api/projects/:id/contradictions` -- 取得矛盾列表 (含 TC/PC 分類)。
  - POST `/api/projects/:id/contradictions` -- AI 識別矛盾 / 手動新增矛盾。
  - PUT `/api/projects/:id/contradictions/:cid` -- 確認/編輯矛盾 (status: confirmed)。
  - DELETE `/api/projects/:id/contradictions/:cid` -- 刪除矛盾。
  - GET `/api/projects/:id/causal-loops` -- 取得因果迴路圖數據 (nodes + edges + breakpoints)。
  - POST `/api/projects/:id/causal-loops` -- AI 生成 CLD。
  - PUT `/api/projects/:id/causal-loops/:lid` -- 更新 CLD (斷路點標記 + 理由)。
  - GET `/api/projects/:id/gates/1.2/check` -- 檢查 Gate 1.2 通過狀態。
  - GET `/api/projects/:id/gates/1.3/check` -- 檢查 Phase Gate 1 通過狀態。
- **response shape** (GET `/api/projects/:id/questions`):
  ```json
  {
    "questions": [
      {
        "id": "uuid",
        "category": "who" | "what" | "where" | "when" | "why" | "how",
        "question_text": "string (AI generated)",
        "answer": "string | null",
        "follow_ups": [
          {
            "id": "uuid",
            "question_text": "string",
            "answer": "string | null"
          }
        ],
        "source": "ai" | "manual",
        "created_at": "YYYY-MM-DD HH:mm:ss"
      }
    ],
    "total": 10,
    "answered": 7
  }
  ```
- **response shape** (GET `/api/projects/:id/contradictions`):
  ```json
  {
    "contradictions": [
      {
        "id": "uuid",
        "type": "TC" | "PC",
        "improving_parameter": { "id": 14, "name": "強度" },
        "worsening_parameter": { "id": 1, "name": "重量" },
        "pc_attribute_a": "string | null",
        "pc_attribute_not_a": "string | null",
        "description": "string",
        "status": "draft" | "confirmed" | "rejected",
        "source": "ai" | "manual",
        "created_at": "YYYY-MM-DD HH:mm:ss"
      }
    ],
    "total": 5,
    "confirmed": 3
  }
  ```
- **response shape** (GET `/api/projects/:id/causal-loops`):
  ```json
  {
    "id": "uuid",
    "nodes": [
      {
        "id": "node-uuid",
        "label": "string",
        "position": { "x": 0, "y": 0 },
        "is_breakpoint": false,
        "breakpoint_reason": "string | null",
        "related_contradictions": ["cid-1", "cid-2"],
        "related_assumptions": ["aid-1"]
      }
    ],
    "edges": [
      {
        "id": "edge-uuid",
        "source": "node-uuid",
        "target": "node-uuid",
        "feedback_type": "positive" | "negative",
        "label": "string | null"
      }
    ],
    "breakpoints_count": 0
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/1.2/check`):
  ```json
  {
    "gate_id": "1.2",
    "passed": false,
    "checklist": [
      { "label": "累計 ≥10 個假設/回答", "current": 7, "target": 10, "passed": false },
      { "label": "識別 ≥3 個已確認矛盾", "current": 2, "target": 3, "passed": false },
      { "label": "至少 3 項高風險項目已標記", "current": 3, "target": 3, "passed": true }
    ]
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/1.3/check`):
  ```json
  {
    "gate_id": "1.3",
    "gate_type": "phase_gate",
    "passed": false,
    "checklist": [
      { "label": "至少 1 個因果迴路圖", "current": 1, "target": 1, "passed": true },
      { "label": "至少 3 個斷路點", "current": 1, "target": 3, "passed": false },
      { "label": "所有矛盾已分類", "current_classified": 2, "total": 5, "passed": false }
    ]
  }
  ```
- **error cases**:
  - 問題列表載入失敗 (500): Tab A 顯示全區錯誤提示 + 重試按鈕。
  - AI 問題生成失敗 (500): 顯示 "AI 生成失敗" toast + [重新生成] 按鈕。
  - 矛盾列表載入失敗 (500): Tab B 顯示全區錯誤提示 + 重試按鈕。
  - AI 矛盾識別失敗 (500): 顯示 "矛盾識別失敗" toast + [AI 重新識別] 按鈕。
  - CLD 載入失敗 (500): Tab C 顯示全區錯誤提示 + 重試按鈕。
  - AI CLD 生成失敗 (500): 畫布顯示 "因果迴路圖生成失敗" + [AI 重新生成] 按鈕。
  - 回答/矛盾保存失敗 (500): 右上角 "儲存失敗，3 秒後重試" + 自動 retry (max 3 次)。
  - Gate check 失敗 (500): Checklist 顯示 "無法檢查" badge (灰色)。

## [STATE DESIGN]

### Zustand Store Slice
```typescript
interface ExplorePageState {
  // Active tab
  activeTab: 'socratic' | 'contradictions' | 'cld';

  // Tab A: Socratic
  questions: Question[];
  answeredCount: number;
  totalCount: number;
  categoryFilter: QuestionCategory | 'all';

  // Tab B: Contradictions
  contradictions: Contradiction[];
  confirmedCount: number;

  // Tab C: CLD
  causalLoop: CausalLoop | null;
  selectedNodeId: string | null;
  breakpointsCount: number;

  // UI state
  saveStatus: 'idle' | 'saving' | 'saved' | 'error';
  aiGenerating: 'questions' | 'contradictions' | 'cld' | null;

  // Gate state
  gate12Result: GateCheckResult | null;
  phaseGate1Result: GateCheckResult | null;
}

type QuestionCategory = 'who' | 'what' | 'where' | 'when' | 'why' | 'how';

interface Question {
  id: string;
  category: QuestionCategory;
  question_text: string;
  answer: string | null;
  follow_ups: FollowUp[];
  source: 'ai' | 'manual';
}

interface Contradiction {
  id: string;
  type: 'TC' | 'PC';
  improving_parameter: TrizParameter | null;
  worsening_parameter: TrizParameter | null;
  pc_attribute_a: string | null;
  pc_attribute_not_a: string | null;
  description: string;
  status: 'draft' | 'confirmed' | 'rejected';
}

interface CausalLoop {
  id: string;
  nodes: CausalNode[];
  edges: CausalEdge[];
}

interface CausalNode {
  id: string;
  label: string;
  position: { x: number; y: number };
  is_breakpoint: boolean;
  breakpoint_reason: string | null;
  related_contradictions: string[];
}

interface CausalEdge {
  id: string;
  source: string;
  target: string;
  feedback_type: 'positive' | 'negative';
}
```

### React Query Keys
```typescript
const exploreQueryKeys = {
  questions: (projectId: string) => ['projects', projectId, 'questions'],
  contradictions: (projectId: string) => ['projects', projectId, 'contradictions'],
  causalLoops: (projectId: string) => ['projects', projectId, 'causal-loops'],
  gate12: (projectId: string) => ['projects', projectId, 'gates', '1.2', 'check'],
  phaseGate1: (projectId: string) => ['projects', projectId, 'gates', '1.3', 'check'],
};
```

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **雙 Gate 共存**: 此頁同時嵌入 Gate 1.2 (Step Gate) 和 Phase Gate 1 (= Gate 1.3)。Phase Gate 以雙線框和微藍背景 (#EFF6FF) 區分於普通 Step Gate。這是 6+1 架構中 Step Gate + Phase Gate 共存的標準模式 (Decide 頁面亦同)。
- **AI 自動連鎖觸發**: Tab 之間存在 AI 連鎖依賴 (問答 → 矛盾識別 → CLD)。Tab 切換時自動觸發下游 AI 生成 (若尚未生成)，無需用戶主動點擊。此為 Apple "AI as Invisible Infrastructure" 哲學的深度實踐。若 AI 已生成過，切換 Tab 不重新觸發。
- **URL Hash 追蹤 Tab**: 此頁使用 URL hash (`#socratic`, `#contradictions`, `#cld`) 追蹤 Tab 狀態，確保用戶重新整理或分享連結時能回到正確的 Tab。其他 Tab 頁面 (Track, Review, Decide) 若需要也可採用此模式。
- **ReactFlow 第三方依賴**: 因果迴路圖依賴 ReactFlow library (`@xyflow/react`)。此為 Explore 頁面專屬的重量級互動元件。需確保 code splitting 將 ReactFlow chunk 獨立載入，避免影響其他頁面 LCP。

## [ACCEPTANCE CRITERIA]
- [ ] Tab 導航列正確切換三個 Tab，當前 Tab 有 Phase 1 藍色底線高亮 (#3B82F6)。
- [ ] Tab badge 即時更新: Tab A "X/Y 已回答", Tab B "X TC + Y PC", Tab C "X 斷路點"。
- [ ] 索克拉底問答: AI 自動生成 5-8 題問題 (涵蓋 5W1H 六類)，以灰底卡片 + [AI] badge + 類別色彩 badge 顯示。
- [ ] 索克拉底問答: 用戶可回答問題 (★必填, min 5 chars)，AI 根據回答自動追問，追問可選填。
- [ ] 索克拉底問答: 已回答卡片有綠色確認邊線，計數器即時更新。
- [ ] 矛盾識別: AI 從問答中自動識別矛盾，生成 TC (藍色 badge) / PC (橙色 badge) 分類卡片。
- [ ] 矛盾識別: 用戶可 [確認 ★] / [編輯] / [刪除] 矛盾，可 [+ 手動新增矛盾]。
- [ ] 矛盾識別: TC 的改善/惡化參數使用 TRIZ 39 參數下拉選擇。
- [ ] 矛盾識別: 統計摘要列正確顯示 TC 數 / PC 數 / 總數 / 已確認數。
- [ ] 因果迴路圖: AI 生成 ReactFlow 互動式 CLD，節點可拖動/縮放/平移。
- [ ] 因果迴路圖: 正回饋 (+) 為藍色箭頭，負回饋 (-) 為紅色箭頭。
- [ ] 因果迴路圖: 用戶可點擊節點開啟右側面板，標記斷路點 (★必填至少 3 個) 並填寫理由 (min 10 chars)。
- [ ] 因果迴路圖: 斷路點節點顯示紅色虛線外框 + ★ icon。
- [ ] Gate 1.2 Checklist 即時反映三項檢查 (≥10 假設, ≥3 矛盾, ≥3 高風險)，支援 ✅/⚠️/❌ 三態。
- [ ] Phase Gate 1 Checklist 以雙線框 + 微藍底里程碑樣式顯示，即時反映三項檢查 (CLD / 斷路點 / 矛盾分類)。
- [ ] Phase Gate 1 通過後啟用「進入 Phase 2: Diverge →」按鈕 (橙色 #F59E0B 配色)。
- [ ] 所有 AI 產出卡片符合灰底 (#F8F9FA) + [AI] badge 視覺規範。
- [ ] Auto-save 機制正常運作，Tab 切換時自動保存當前 Tab 數據。
- [ ] URL hash 追蹤 Tab 狀態 (#socratic / #contradictions / #cld)，重新整理不遺失當前 Tab。
- [ ] RWD 在 Desktop / Tablet / Mobile 三個斷點下佈局正確，CLD 在 Mobile 可全螢幕展開。

## [VERSION]
- **version**: v2.0
- **last_updated**: 2026-02-25
- **changelog**:
  - v1.0 -- 初版建立 (索克拉底問答 + 矛盾識別 + CLD + Gate 1.2 + Phase Gate 1)
  - v2.0 -- 新增 AI 追問機制、問題類別色彩 badge、矛盾 TC/PC 卡片差異化、斷路點理由必填、STATE DESIGN 區塊、URL hash Tab 追蹤、RWD Mobile 全螢幕 CLD
