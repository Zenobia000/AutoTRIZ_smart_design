# Page-Level Prompt: Brief -- 定義簡報

## [PAGE META]
- **page_name**: Brief -- 定義簡報
- **route_path**: `/projects/:id/brief`
- **page_type**: form
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: 結構化定義 Mission Statement、Hard Constraints (硬約束)、Top 3 KPI，建立專案的核心設計命題與不可妥協的邊界。
- **secondary_goal**: AI 自動生成 5W1H 任務定義表與改寫建議，供用戶審閱及修改，降低定義遺漏風險。
- **mapped_step**: Step 1.1 問題界定
- **embedded_gate**: Gate 1.1
- **phase_color**: Phase 1 藍色 (#3B82F6)

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管, 專案經理 (PM)
- **entry_point**:
  - 從 Dashboard 的 6+1 導航區點擊「Brief」卡片進入。
  - 新建專案後自動導航至此頁 (首次使用主要入口)。
  - 從 Explore 頁面的 breadcrumb 點擊「Brief」返回。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 中 (5-15 分鐘)
  <!-- 粗估停留時間，幫助決定資訊密度 -->
- **user_mindset**: 用戶正在尋求方向，需要一個結構化的框架來界定設計任務的邊界。

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **Mission 輸入區**
   - section_type: form
   - section_purpose: 讓用戶以一句話描述核心設計任務 (Mission Statement)，AI 提供改寫建議。

2. **硬約束區 (MUST)**
   - section_type: form (editable table)
   - section_purpose: 定義專案不可妥協的硬約束清單 (constraint_code, description, source)，可新增/刪除行，AI 建議補充約束。

3. **KPI 區**
   - section_type: form (dynamic list)
   - section_purpose: 定義關鍵績效指標及其目標值 (kpi_name, target_value, unit, measurement_method)，AI 建議 KPI。

4. **AI 任務定義表** (Agent)
   - section_type: agent-card (collapsible)
   - section_purpose: AI 根據 Mission + Constraints + KPI 自動生成 5W1H 任務定義，供用戶審閱。

5. **Gate 1.1 Checklist** (Display)
   - section_type: gate-indicator (inline)
   - section_purpose: 內嵌於頁面底部，即時檢查 Gate 1.1 通過條件，通過後解鎖 Explore 頁面。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: Mission 輸入區
- **layout**: 單欄表單，標題 + 模板提示 + textarea + AI 改寫建議卡片。
- **input_category**: 必填 (Human Input) -- 白底輸入框 + 紅色星號 ★
- **elements**:
  - `Mission 標題`: `h2`, `required`, `"核心使命 (Mission Statement) ★"`
  - `模板提示`: `helper-text`, `required`, `"在 [情境] 下，系統必須 [行為]，且 [指標] 不得超標" -- 顯示於 textarea 上方作為結構化填寫引導。灰色斜體。`
  - `Mission 輸入框`: `textarea`, `required`, `白底，紅色星號 ★ 標示。placeholder: "請用一句話描述您的設計任務..."。自動展開高度 (min-height: 100px, auto-grow)。`
  - `AI 改寫建議卡片 (Agent)`: `agent-card`, `optional`, `灰底卡片 (#F8F9FA) + [AI] badge。Mission 填寫完成後 AI 自動生成改寫建議 (如 "設計一款在 80°C 環境下運行的散熱模組...")。包含三個操作按鈕: [採用] (替換 Mission 內容) / [編輯] (進入編輯模式) / [跳過] (收合卡片)。`
- **states**:
  - empty: placeholder 顯示模板格式。
  - filled: 白底，左側出現綠色確認邊線 (border-left: 3px solid #28a745)。
  - error: 紅色邊框 + 下方紅色提示 "Mission 為必填欄位，至少 10 個字元"。
  - ai-suggestion: Mission 有值時，下方顯示 AI 改寫建議灰底卡片。
  - ai-loading: 改寫建議區域顯示 inline skeleton。
- **copy_constraints**:
  - Mission: 最少 10 字元，最多 500 字元。
  - AI 改寫建議: 最多 500 字元。

### Section: 硬約束區 (MUST)
- **layout**: 可編輯表格，四欄 (constraint_code / description / source / 操作)，底部 "+ 新增約束" 按鈕 + "AI 建議補充" 按鈕。
- **input_category**: 必填 (Human Input) -- 白底輸入框 + 紅色星號 ★
- **elements**:
  - `表格標題`: `h2`, `required`, `"硬約束 (Hard Constraints / MUST) ★"`
  - `約束表格`: `editable-table`, `required`, `四欄表格：約束代碼 (auto-generated: M1, M2, M3...) / 約束描述 (text input, ★必填) / 來源依據 (text input) / 操作 ([刪除] button)。每行自動編號。至少保留 1 行有效數據。`
  - `新增約束按鈕`: `button (ghost)`, `required`, `"+ 新增約束"，點擊在表格底部插入空行。`
  - `AI 建議補充按鈕 (Agent)`: `button (secondary)`, `optional`, `"AI 建議補充 [AI]"。點擊後 AI 根據 Mission 分析可能遺漏的硬約束，以灰底卡片顯示建議清單。每條建議有 [採用] (插入表格) / [跳過] 按鈕。`
- **states**:
  - 正常: 表格至少 1 行已填寫。
  - empty-row: 新增的空行，欄位為空，placeholder 提示 (如 "空間限制" / "空間 ≤ 200mm" / "規格書 v2.1")。
  - error: 表格為空 (0 行有效數據) 時，表格邊框變紅 + 提示 "至少需要 1 項硬約束"。
  - ai-suggestion: AI 建議卡片顯示在表格下方，灰底 + [AI] badge。
- **copy_constraints**:
  - constraint_code: 自動生成 (M1, M2, M3...)，不可編輯。
  - description: 最少 2 字元，最多 200 字元。
  - source: 最多 200 字元，可為空。

### Section: KPI 區
- **layout**: 動態列表，每項包含四欄 (kpi_name / target_value / unit / measurement_method)，底部 "+ 新增 KPI" 按鈕 + "AI 建議 KPI" 按鈕。最多 5 項，至少 1 項。
- **input_category**: 必填 (Human Input) -- 白底輸入框 + 紅色星號 ★
- **elements**:
  - `列表標題`: `h2`, `required`, `"關鍵績效指標 (KPI) ★"`
  - `KPI 項目 (x1~5)`: `kpi-row (repeating)`, `required`, `每行四欄：指標名稱 (text input, ★必填) / 目標值 (text input, ★必填) / 單位 (text input, ★必填) / 衡量方式 (text input, ★必填)。每行有刪除按鈕 (最少保留 1 行時禁用)。`
  - `新增 KPI 按鈕`: `button (ghost)`, `optional`, `"+ 新增 KPI"，當列表 < 5 項時可見，否則隱藏。`
  - `AI 建議 KPI 按鈕 (Agent)`: `button (secondary)`, `optional`, `"AI 建議 KPI [AI]"。點擊後 AI 根據 Mission + Constraints 建議可能的 KPI，以灰底卡片顯示。每條建議有 [採用] / [跳過] 按鈕。`
- **states**:
  - 正常: 列表有 1~5 項 KPI。
  - max-reached: 已達 5 項，新增按鈕隱藏。
  - error: 列表為空時，提示 "至少需要 1 項 KPI"。
  - ai-suggestion: AI 建議 KPI 卡片顯示在列表下方。
- **copy_constraints**:
  - kpi_name: 最少 2 字元，最多 80 字元。
  - target_value: 最少 1 字元，最多 50 字元 (如 "≥ 95%", "≤ 50dB")。
  - unit: 最少 1 字元，最多 20 字元 (如 "%", "dB", "mm")。
  - measurement_method: 最少 2 字元，最多 200 字元 (如 "熱仿真", "ISO 測試方法 A")。

### Section: AI 任務定義表 (Agent)
- **layout**: 可收合灰底卡片 (預設收合)，展開後顯示 5W1H 結構化表格。
- **input_category**: Agent 處理 (Auto) -- 灰底卡片 (#F8F9FA) + `[AI]` 標籤
- **elements**:
  - `卡片標題`: `h3 + badge`, `required`, `"任務定義表 [AI]" -- [AI] 為灰色圓角 badge (#6c757d 底, 白字)。`
  - `收合/展開切換`: `chevron-toggle`, `required`, `預設收合，點擊展開。`
  - `5W1H 表格 (Agent 產出)`: `readonly-table`, `required`, `六行表格: Who (誰負責) / What (做什麼) / Where (在哪裡) / When (時間軸) / Why (為什麼) / How (怎麼做)。每格為 AI 生成的文字，灰底。`
  - `編輯按鈕`: `button (ghost)`, `optional`, `"[編輯]" -- 點擊後 5W1H 表格切換為可編輯模式 (textarea)。`
  - `重新生成按鈕`: `button (ghost)`, `optional`, `"[重新生成]" -- 點擊後以當前 Mission + Constraints + KPI 重新觸發 AI 生成。顯示 loading spinner。`
- **states**:
  - collapsed: 僅顯示標題列 + [AI] badge + chevron。
  - expanded: 顯示完整 5W1H 表格。
  - loading: 表格區域顯示 skeleton + "AI 正在分析..." 提示。
  - editing: 表格切換為 textarea，背景變白，出現 [儲存] / [取消] 按鈕。
  - no-data: Mission 尚未填寫時，顯示 "請先完成 Mission 填寫，AI 將自動生成任務定義表"。
- **copy_constraints**:
  - 5W1H 每格: 最多 500 字元。
  - AI 生成觸發條件: Mission 字段有值且 ≥ 10 字元。

### Section: Gate 1.1 Checklist (Display)
- **layout**: 頁面底部嵌入，水平分隔線上方，checklist 格式。Step Gate 樣式 (單線框 + Phase 1 藍色色帶)。
- **input_category**: 必須呈現 (Display) -- 彩色徽章 + 進度指示
- **elements**:
  - `Gate 標題`: `h3`, `required`, `"Gate 1.1 -- 任務定義完整性檢查" + Phase 1 藍色色帶 (#3B82F6)。`
  - `Checklist 項目 (x3)`: `checklist-item (repeating, Display)`, `required`, `三項檢查：(1) Mission 已填寫 (✅/❌)、(2) 至少 1 項硬約束 (✅/❌)、(3) 至少 1 項 KPI (✅/❌)。即時檢查，自動更新圖示。`
  - `Gate 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ 時顯示 "Gate 1.1 Passed" (綠色 badge #28a745)；否則顯示 "Gate 1.1 未通過" (紅色 badge #dc3545)。`
  - `前往下一步按鈕`: `button (primary)`, `required`, `"通過 → 進入 Explore"。Gate 通過時啟用 (blue)，未通過時禁用 (greyed out) + tooltip "請完成上方所有必填項目"。`
- **states**:
  - all-passed: 三項皆 ✅，綠色 badge，按鈕啟用。
  - partial: 部分 ✅ 部分 ❌，紅色 badge，按鈕禁用。
  - none: 三項皆 ❌，紅色 badge，按鈕禁用。
- **copy_constraints**:
  - Checklist 文字: 固定文字，不可自訂。

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入 Brief 頁面，系統載入已有的 Mission / Constraints / KPI 數據 (若有)。
  2. 用戶填寫 Mission textarea (★必填)，系統即時前端驗證。
  3. 當 Mission 填寫完成 (≥10 字元)，AI 改寫建議自動觸發 (debounce 1.5s)。用戶可 [採用] / [編輯] / [跳過]。
  4. 用戶在硬約束表格新增/編輯/刪除約束行 (★必填至少 1 行)。可點擊 "AI 建議補充" 獲取 AI 建議。
  5. 用戶在 KPI 列表新增/編輯/刪除 KPI 項目 (★必填至少 1 項)。可點擊 "AI 建議 KPI" 獲取 AI 建議。
  6. Mission + Constraints + KPI 皆有值後，AI 任務定義表自動觸發生成 (5W1H)。用戶可展開查看、編輯或重新生成。
  7. Gate 1.1 Checklist 即時反映三項檢查狀態。
  8. 所有必填項完成後，Gate 1.1 badge 轉綠，「通過 → 進入 Explore」按鈕啟用。
  9. 用戶點擊按鈕，數據自動保存 (auto-save)，導航至 `/projects/:id/explore`。

- **Auto-Save 策略**：
  - 每個欄位 onBlur 或每 5 秒 debounce 自動保存至後端 (PUT)。
  - 儲存中顯示 "Saving..." 小型 indicator (右上角)，成功後顯示 "Saved" 持續 2 秒。

- **表單驗證規則**：
  - `Mission`: 必填，最少 10 字元 → "Mission 為必填項，且需至少 10 個字元。"
  - `Hard Constraints`: 至少 1 行有效數據 (description 不為空) → "至少需要 1 項硬約束。"
  - `KPI`: 至少 1 項有效數據 (kpi_name + target_value + unit + measurement_method 皆不為空) → "至少需要 1 項 KPI。"

- **資料更新策略**：
  - 初始載入: GET definitions，填充表單。
  - Auto-save: PUT definitions (debounced)。
  - AI 改寫建議: POST trigger (非同步)，結果寫入臨時狀態，用戶 [採用] 後才寫入 Mission。
  - AI 5W1H 生成: POST trigger (非同步)，結果寫入 definitions.task_definition_5w1h。
  - AI 約束/KPI 建議: POST trigger (非同步)，用戶 [採用] 後才寫入 constraints / kpis。
  - Gate check: GET gates/1.1/check，結果更新 checklist UI (可前端自行計算，亦可 API 校驗)。

- **RWD 行為差異**：
  - Desktop (>1024px): Mission + Constraints + KPI 單欄佈局，AI 改寫建議卡片在 textarea 下方展示。
  - Tablet (768px - 1023px): 全部單欄堆疊。
  - Mobile (<768px): 全部單欄堆疊，表格轉為卡片式輸入 -- 每行約束/KPI 為獨立卡片，避免水平捲動。

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/definitions` -- 取得專案的任務定義 (mission, constraints, kpis, task_definition_5w1h)。
  - PUT `/api/projects/:id/definitions` -- 更新任務定義 (auto-save 用)。
  - GET `/api/projects/:id/gates/1.1/check` -- 檢查 Gate 1.1 通過狀態。
- **request shape** (PUT `/api/projects/:id/definitions`):
  ```json
  {
    "mission": "string",
    "constraints": [
      {
        "constraint_code": "M1",
        "description": "string",
        "source": "string"
      }
    ],
    "kpis": [
      {
        "kpi_name": "string",
        "target_value": "string",
        "unit": "string",
        "measurement_method": "string"
      }
    ],
    "task_definition_5w1h": {
      "who": "string",
      "what": "string",
      "where": "string",
      "when": "string",
      "why": "string",
      "how": "string"
    }
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/1.1/check`):
  ```json
  {
    "gate_id": "1.1",
    "passed": false,
    "checklist": [
      { "label": "Mission 已填寫", "passed": true },
      { "label": "至少 1 項硬約束", "passed": false },
      { "label": "至少 1 項 KPI", "passed": true }
    ]
  }
  ```
- **error cases**:
  - 定義載入失敗 (500): 顯示全頁錯誤提示 + 重試按鈕。
  - Auto-save 失敗 (500): 右上角顯示 "儲存失敗，3 秒後重試" 並自動 retry (max 3 次)。
  - AI 改寫建議生成失敗 (500): 改寫建議卡片顯示 "AI 生成失敗" + [重新生成] 按鈕。
  - AI 5W1H 生成失敗 (500): AI 卡片內顯示 "AI 生成失敗" + [重新生成] 按鈕。
  - AI 約束/KPI 建議失敗 (500): 對應按鈕恢復可點擊 + toast "AI 建議生成失敗"。
  - Gate check 失敗 (500): Checklist 顯示 "無法檢查" badge (灰色)，仍允許手動導航。

## [STATE DESIGN]

### Zustand Store Slice
```typescript
interface BriefPageState {
  // Form data
  mission: string;
  constraints: Constraint[];
  kpis: KPI[];
  task_definition_5w1h: Record<string, string> | null;

  // UI state
  activeAISuggestion: 'mission' | 'constraints' | 'kpis' | null;
  aiTaskDefinitionExpanded: boolean;
  saveStatus: 'idle' | 'saving' | 'saved' | 'error';

  // Gate state
  gateCheckResult: GateCheckResult | null;
}

interface Constraint {
  constraint_code: string; // M1, M2, ...
  description: string;
  source: string;
}

interface KPI {
  kpi_name: string;
  target_value: string;
  unit: string;
  measurement_method: string;
}
```

### React Query Keys
```typescript
const briefQueryKeys = {
  definitions: (projectId: string) => ['projects', projectId, 'definitions'],
  gateCheck: (projectId: string) => ['projects', projectId, 'gates', '1.1', 'check'],
};
```

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **Auto-Save 取代明確 Submit**: 此頁不設「提交」按鈕，改用 auto-save 機制。原因：Brief 是漸進填寫的起點頁面，減少用戶操作摩擦。用戶隨時可離開，數據不會丟失。
- **AI 觸發為自動 (非按鈕)**: AI 改寫建議和 5W1H 任務定義表在 Mission 填寫後自動觸發，不需用戶主動點擊。原因：Apple 的 "AI as Invisible Infrastructure" 哲學 -- AI 自動出現，用戶決定是否查看。AI 約束建議和 KPI 建議則需手動點擊觸發，因為這些需要用戶明確意圖。
- **constraint_code 自動編號**: 約束代碼 (M1, M2, ...) 由系統自動生成，不可手動輸入。原因：確保代碼一致性，避免重複編號。

## [ACCEPTANCE CRITERIA]
- [ ] Mission textarea 以模板提示引導用戶填寫，驗證最少 10 字元。
- [ ] Mission 填寫後 AI 自動生成改寫建議，顯示灰底卡片 + [AI] badge + [採用] / [編輯] / [跳過] 按鈕。
- [ ] 硬約束表格支援新增/編輯/刪除行，自動編號 (M1, M2, ...)，至少保留 1 行。
- [ ] "AI 建議補充" 按鈕觸發 AI 生成約束建議，每條有 [採用] / [跳過]。
- [ ] KPI 列表支援新增/編輯/刪除項目，四欄 (名稱/目標值/單位/衡量方式)，限制 1~5 項。
- [ ] "AI 建議 KPI" 按鈕觸發 AI 生成 KPI 建議。
- [ ] AI 任務定義表在 Mission 填寫後自動生成 5W1H 內容，預設收合，可展開/編輯/重新生成。
- [ ] 所有 AI 卡片顯示灰底 (#F8F9FA) + [AI] badge，符合 Agent 處理視覺規範。
- [ ] Gate 1.1 Checklist 即時反映三項檢查狀態 (Mission / Constraint / KPI)，全部通過後啟用導航按鈕。
- [ ] Auto-save 機制正常運作，儲存狀態有視覺回饋 (Saving... / Saved)。
- [ ] RWD 在 Desktop / Tablet / Mobile 三個斷點下佈局正確，Mobile 下表格轉卡片式。

## [VERSION]
- **version**: v2.0
- **last_updated**: 2026-02-25
- **changelog**:
  - v1.0 -- 初版建立 (Mission + Constraints + KPI + Gate 1.1)
  - v2.0 -- 新增 AI 改寫建議、AI 約束/KPI 建議、constraint_code 自動編號、KPI 四欄擴充 (加 unit)、STATE DESIGN 區塊
