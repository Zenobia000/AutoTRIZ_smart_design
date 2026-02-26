# Page-Level Prompt: Review -- 設計審查

## [PAGE META]
- **page_name**: Review -- 設計審查
- **route_path**: `/projects/:id/review`
- **page_type**: tabs (3 Tabs)
  <!-- landing / form / dashboard / report / search / detail / settings / accordion / tabs -->
- **primary_goal**: 以證據矩陣熱力圖、風險 P x S 矩陣和最小實驗卡片，建構完整的證據驅動設計審查體系。
- **secondary_goal**: 透過 evidence gap 分析驅動最小實驗迴圈 (Step 3.1.loop)，確保所有高風險假設都有足夠證據等級，所有 H/H* 風險都有緩解措施。
- **phase**: Phase 3 Converge (#10B981 綠)
- **mapped_steps**: Step 3.1 設計審查 + Step 3.1.loop 證據補齊
- **embedded_gate**: Gate 3.1

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：RD 工程師
  - 次要：RD 主管、品質工程師
- **entry_point**:
  - 從「方案創造 (Create)」頁面 Phase Gate 2 通過後導航進入。
  - 從 Dashboard / Sidebar 直接點擊「Review」卡片進入。
  - 從 Decide 頁面 breadcrumb 返回。
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: 長 (20-40 分鐘)
  <!-- 證據矩陣需要反覆更新，實驗迴圈可能跨多次 session -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **Phase Header**
   - section_type: header
   - section_purpose: 顯示 "Phase 3: Converge > Step 3.1 設計審查" breadcrumb 及 Phase 3 綠色色帶。

2. **Tab A -- 證據矩陣 (Evidence Matrix)**
   - section_type: tab / heatmap-table
   - section_purpose: 以熱力圖呈現假設 x 證據等級 (E0-E4) 的覆蓋狀態，識別證據缺口，驅動實驗迴圈。

3. **Tab B -- 風險評估 (Risk Assessment)**
   - section_type: tab / matrix-form
   - section_purpose: 以 P x S 色階矩陣視覺化風險分布，登錄並管理每條風險的 probability、severity、mitigation。

4. **Tab C -- 最小實驗 (Minimum Experiments)**
   - section_type: tab / card-list-form
   - section_purpose: 規劃、執行、記錄最小實驗，填補證據缺口。實驗結果回饋至 Tab A 證據矩陣，形成 Step 3.1.loop。

5. **Gate 3.1 Checklist**
   - section_type: gate-indicator (inline)
   - section_purpose: 頁面底部內嵌 Gate 3.1，即時檢查三項通過條件，引導用戶前往 Decide。

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: Phase Header
- **layout**: 頂部橫幅，Phase 3 綠色色帶 (#10B981)，breadcrumb 路徑。
- **elements**:
  - `Phase 色帶`: `div (4px height)`, `Display`, `背景色 #10B981，頁面頂部。`
  - `Breadcrumb`: `text`, `Display`, `"Phase 3: Converge > Step 3.1 設計審查"。`
- **states**:
  - 正常：色帶 + breadcrumb 靜態顯示。

### Section: Tab A -- 證據矩陣 (Evidence Matrix)
- **layout**: 熱力圖表格 (Recharts)，行 = 假設 (assumption_code + 摘要)，列 = 證據等級 E0-E4。表格下方為 AI 缺口分析摘要。
- **input_category**: 必須呈現 (Display) -- 此 Tab 為唯讀聚合視圖，數據來自假設台帳 + 實驗結果。
- **visual_highlight**: 證據矩陣熱力圖 (Evidence Heatmap)
- **elements**:
  - `熱力圖表格`: `heatmap-table (Recharts)`, `Display`, `行標題：假設 assumption_code (如 A-001, A-002...) + 假設內容摘要 (40 字截斷)。列標題：E0 (無證據) / E1 (工程估算) / E2 (仿真) / E3 (原型) / E4 (量產驗證)。儲存格以實心色塊標記該假設目前最高證據等級。`
  - `儲存格色塊`: `cell-indicator`, `Display`, `色塊顏色：E0=紅 (#dc3545) / E1=橙 (#fd7e14) / E2=黃綠 (#84CC16) / E3=淺綠 (#34D399) / E4=深綠 (#059669)。E0-E1 為缺口(gap)，需關注；E2+ 為安全。`
  - `Gap 分析摘要`: `alert-bar`, `Display`, `底部統計欄：高亮 E0/E1 項目數量。格式："X 項假設仍處於 E0/E1，存在證據缺口"。有缺口時以橙色警告底色 (#FFF7ED) 呈現。`
  - `[查看實驗] 連結`: `link (inline)`, `optional`, `點擊色塊可跳轉至 Tab C 對應實驗，支持 Tab 間聯動。`
  - `AI 缺口分析卡片`: `agent-card`, `Agent`, `灰底卡片 (#F8F9FA) + [AI] 標籤。AI 分析證據缺口並建議優先補齊順序。格式："證據缺口: A-002 無任何證據，建議進行..."。附 [採用] [編輯] [重生成] [跳過] 按鈕。`
- **states**:
  - 正常：熱力圖完整顯示，色塊清晰可辨。
  - empty：無假設時顯示空狀態："尚無數據，請先在 Track 頁建立假設" + CTA 按鈕導航至 Track。
  - loading：表格區域顯示骨架屏 (Skeleton)。
  - warning：E0/E1 項目存在時，Gap 分析摘要以橙色底高亮。
  - all-clear：所有假設均達 E2+，Gap 分析顯示 "所有假設已有充足證據 ✅" (綠色底)。
- **copy_constraints**:
  - 假設內容摘要：表格內最多 40 字元，超出截斷加 `...`，hover 顯示完整文字。
  - 證據等級標籤：固定文字 E0/E1/E2/E3/E4，不可自訂。

### Section: Tab B -- 風險評估 (Risk Assessment)
- **layout**: 上方為 P x S 色階矩陣 (5x5 grid)，下方為風險表格 (可排序可編輯)。
- **input_category**: 必填 (Human Input) -- probability 和 severity 為用戶必填判斷。
- **visual_highlight**: Risk P x S 色階矩陣
- **elements**:
  - `P x S 色階矩陣`: `mini-heatmap (5x5 grid)`, `Display`, `X 軸 = Severity (1-5)，Y 軸 = Probability (1-5)。格子顏色：P x S ≥ 20=深紅 (#8B0000, H*) / 15-19=紅 (#dc3545, H) / 8-14=橙 (#fd7e14, M) / ≤ 7=綠 (#28a745, L)。格子內標記對應 risk_code (如 R1, R3)，可點擊跳轉至下方表格行。`
  - `風險表格`: `table (React Table, sortable)`, `required`, `欄位：risk_code (auto: R-001, R-002...) / description ★ / probability (P, 1-5) ★ / severity (S, 1-5) ★ / risk_score (P x S, auto) / risk_level (auto badge) / mitigation。`
  - `risk_code`: `text (auto-generated)`, `Display`, `系統自動產生序號。`
  - `description`: `textarea (inline-edit)`, `required ★`, `風險描述，白底 + 紅色星號。`
  - `probability (P)`: `dropdown (1-5)`, `required ★`, `1=極低 / 2=低 / 3=中 / 4=高 / 5=極高。白底 + 紅色星號。`
  - `severity (S)`: `dropdown (1-5)`, `required ★`, `1=可忽略 / 2=輕微 / 3=中度 / 4=嚴重 / 5=災難。白底 + 紅色星號。`
  - `risk_score`: `badge`, `Display`, `自動計算 P x S。色彩同矩陣：H*(≥20)=深紅 / H(15-19)=紅 / M(8-14)=橙 / L(≤7)=綠。`
  - `mitigation`: `textarea (inline-edit)`, `optional`, `緩解措施描述。H/H* 風險若無 mitigation 會觸發 Gate 3.1 警告。`
  - `[+ 新增風險] 按鈕`: `button (secondary)`, `required`, `在表格底部新增空白列。`
  - `[AI 識別風險] 按鈕`: `button (primary)`, `Agent`, `AI 根據方案、假設和實驗結果自動識別潛在風險，結果以灰底卡片顯示，附 [AI] 標籤 + [採用] [編輯] [跳過] 按鈕。`
  - `AI 緩解措施建議`: `agent-card (inline)`, `Agent`, `選中特定風險行後，AI 建議 mitigation 策略。灰底 + [AI] 標籤。`
- **states**:
  - 正常：表格可互動，行內編輯，P x S 矩陣同步更新。
  - empty：無風險時顯示 "尚無風險，建議使用 AI 識別潛在風險" 引導提示。
  - loading：AI 識別中，顯示 skeleton 卡片。
  - error：數據載入/保存失敗，Toast 提示 + 行內保留 local state。
  - warning：H/H* 風險缺少 mitigation 時，該行以淺紅底色高亮。
- **copy_constraints**:
  - description：最少 10 字元，最多 300 字元。
  - mitigation：最多 500 字元。

### Section: Tab C -- 最小實驗 (Minimum Experiments)
- **layout**: 實驗卡片列表 + 新增/編輯表單 (Modal 或 Drawer)。此 Tab 是 Step 3.1.loop 的核心，實驗完成後回饋至 Tab A 證據矩陣。
- **input_category**: 必填 (Human Input) -- hypothesis、method、success_criteria 為用戶核心判斷。
- **elements**:
  - `實驗卡片列表`: `card-list`, `required`, `每張卡片顯示：experiment_code (auto: Exp-001, Exp-002...) / hypothesis / method / success_criteria / evidence_level (E0-E4 badge) / result / status (badge)。`
  - `experiment_code`: `text (auto)`, `Display`, `系統自動產生序號。`
  - `hypothesis`: `text (card title)`, `required ★`, `實驗假說，白底 + 紅色星號。如 "散熱片面積 ≥ 50cm2 可維持 T ≤ 85C"。`
  - `method`: `text`, `required ★`, `實驗方法。如 "熱仿真 (ANSYS)"。白底 + 紅色星號。`
  - `success_criteria`: `text`, `required ★`, `成功標準。如 "deltaT ≤ 5C"。白底 + 紅色星號。`
  - `evidence_level`: `badge`, `Display`, `目標證據等級 E0-E4，色彩同 Tab A。`
  - `result`: `textarea`, `required ★ (conditional: status=Done)`, `實驗結果描述。僅在 status=Done 時必填。如 "仿真顯示 deltaT=3.2C，通過"。`
  - `status`: `badge`, `Display`, `Plan=藍 (#3B82F6) / Running=橙 (#F59E0B) / Done=綠 (#10B981)。`
  - `[+ 新增實驗] 按鈕`: `button (secondary)`, `required`, `開啟 Modal/Drawer 填寫新實驗。`
  - `[AI 建議實驗] 按鈕`: `button (primary)`, `Agent`, `AI 根據 Tab A 證據缺口建議最小實驗。結果以灰底卡片顯示，附 [AI] 標籤 + [採用] [編輯] [跳過] 按鈕。`
  - `新增/編輯 Modal 欄位`:
    - `hypothesis`: `textarea`, `required ★`, `實驗假說。`
    - `method`: `textarea`, `required ★`, `實驗方法。`
    - `success_criteria`: `textarea`, `required ★`, `成功標準。`
    - `linked_assumption`: `dropdown (multi-select)`, `required ★`, `關聯假設，從假設列表中選取。`
    - `evidence_level`: `dropdown`, `required`, `目標證據等級 E0-E4。`
    - `status`: `dropdown`, `required`, `Plan / Running / Done。`
    - `result`: `textarea`, `required ★ (conditional)`, `status=Done 時必填。`
- **states**:
  - 正常：卡片列表正常顯示，每張卡片可展開查看詳情。
  - empty：無實驗時顯示 "尚無實驗，查看證據矩陣確認缺口後規劃實驗" + CTA 按鈕。
  - loading：AI 建議中，顯示 skeleton 卡片。
  - loop-indicator：Tab A 有 E0/E1 gap 時，Tab C 標題旁顯示 ⚠️ 提醒圖示，引導用戶補齊實驗。
  - done：實驗 status=Done 時卡片左側出現綠色確認邊線。
- **copy_constraints**:
  - hypothesis：最少 10 字元，最多 300 字元。
  - method：最少 5 字元，最多 500 字元。
  - success_criteria：最少 5 字元，最多 200 字元。
  - result：最少 10 字元 (when required)，最多 500 字元。

### Section: Gate 3.1 Checklist
- **layout**: 頁面底部嵌入，水平分隔線上方，checklist 格式。Step Gate 樣式 (單線框) + Phase 3 綠色色帶。
- **input_category**: 必須呈現 (Display) -- 彩色徽章 + checklist 指示器
- **elements**:
  - `Gate 標題`: `h3`, `required`, `"Gate 3.1 -- 設計審查完整性檢查" + Phase 3 綠色色帶 (#10B981)。`
  - `Checklist 項目 (x3)`: `checklist-item (repeating, Display)`, `required`, `三項即時檢查：(1) 證據矩陣無 E0 缺口 (所有假設 ≥ E1) (✅/⚠️/❌)、(2) 所有 H/H* Risk 有 mitigation (✅/❌)、(3) 至少 1 項實驗已完成 (status=Done) (✅/❌)。`
  - `Gate 狀態 badge`: `badge (Display)`, `required`, `全部 ✅ 時顯示 "Gate 3.1 Passed" (綠色 badge #28a745)；否則顯示 "Gate 3.1 未通過" (紅色 badge #dc3545)。`
  - `前往下一步按鈕`: `button (primary)`, `required`, `"通過 → 進入 Decide"。Gate 通過時啟用 (#10B981 green)，未通過時禁用 (greyed out) + tooltip "請完成上方所有檢查項目"。`
- **states**:
  - all-passed：三項皆 ✅，綠色 badge，按鈕啟用。
  - partial：部分 ✅ 部分 ❌/⚠️，紅色 badge，按鈕禁用。
  - none：三項皆 ❌，紅色 badge，按鈕禁用。

## [WIREFRAME]

```
┌─ Header: Phase 3: Converge > Step 3.1 設計審查 ──────────────┐
│                                                                │
│ [證據矩陣] [風險評估] [最小實驗]              ← 3 Tabs         │
│ ─────────────────────────────────                              │
│                                                                │
│ Tab A: 證據矩陣                                                │
│ ┌────────┬────┬────┬────┬────┬────┐                           │
│ │ 假設    │ E0 │ E1 │ E2 │ E3 │ E4 │                           │
│ ├────────┼────┼────┼────┼────┼────┤                           │
│ │ A-001  │    │    │ ██ │    │    │  ← E2 仿真 (green)         │
│ │ A-002  │ ██ │    │    │    │    │  ← E0 無證據 (red!)        │
│ │ A-003  │    │ ██ │    │    │    │  ← E1 估算 (orange)        │
│ └────────┴────┴────┴────┴────┴────┘                           │
│ [AI] 證據缺口: A-002 無任何證據，建議進行...                     │
│                                                                │
│ Tab B: 風險評估                                                │
│ ┌─────────────────────────────────┐                           │
│ │ Severity →  1   2   3   4   5   │                           │
│ │ Prob ↓                          │                           │
│ │  5         [ ] [ ] [R3][ ] [ ]  │                           │
│ │  4         [ ] [ ] [ ] [R1][ ]  │                           │
│ │  3         [ ] [R4][ ] [ ] [ ]  │                           │
│ │  2         [ ] [ ] [ ] [ ] [ ]  │                           │
│ │  1         [ ] [ ] [R2][ ] [ ]  │                           │
│ └─────────────────────────────────┘                           │
│                                                                │
│ Tab C: 最小實驗                                                │
│ ┌─ Exp-001 ────────────────────────────────────────────┐      │
│ │ 假說: 散熱片面積≥50cm² 可維持 T≤85°C                   │      │
│ │ 方法: 熱仿真 (ANSYS)  │ 成功標準: ΔT≤5°C              │      │
│ │ 證據等級: E2  │ 狀態: 已完成 ✅                         │      │
│ │ 結果: 仿真顯示 ΔT=3.2°C，通過                          │      │
│ └──────────────────────────────────────────────────────┘      │
│ [+ 新增實驗]  [AI 建議實驗]                                     │
│                                                                │
│ ── Gate 3.1 ──────────────────────────────────                 │
│ ⚠️ 無 E0 缺口  ✅ H/H* Risk 有 mitigation  ✅ ≥1 實驗完成     │
│ [通過 → 進入 Decide]                                           │
└────────────────────────────────────────────────────────────────┘
```

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. 用戶進入頁面，系統載入假設列表、實驗數據、風險數據，預設顯示 Tab A 證據矩陣。
  2. Tab A 渲染熱力圖。用戶查看 E0/E1 缺口，Gap 分析摘要自動高亮需要關注的假設。AI 自動分析並顯示缺口建議 (預設收合)。
  3. 用戶切換至 Tab B 風險評估。P x S 矩陣即時顯示風險分布。用戶手動新增風險或使用 [AI 識別風險] 自動生成。填寫 P ★ / S ★ 後系統自動計算 risk_score 並更新矩陣。AI 可建議 mitigation 策略。
  4. 用戶切換至 Tab C 最小實驗。根據 Tab A 證據缺口規劃新實驗。可使用 [AI 建議實驗] 獲取建議。填寫 hypothesis ★ / method ★ / success_criteria ★。
  5. 實驗完成後，用戶更新 status=Done 並填寫 result ★。系統自動更新 Tab A 證據矩陣（React Query invalidation）。
  6. **實驗迴圈 (Step 3.1.loop)**：若 Tab A 仍有 E0/E1 缺口，Tab C 標題顯示 ⚠️，用戶重複步驟 2-5 直到所有關鍵假設達到足夠證據等級。
  7. 頁面底部 Gate 3.1 checklist 自動更新，三項全部通過後 "通過 → 進入 Decide" 按鈕啟用。

- **Tab 間聯動**：
  - Tab C 新增/完成實驗 → Tab A 熱力圖自動 refetch 更新。
  - Tab A 點擊色塊 → 自動切換至 Tab C 並滾動至對應實驗。
  - Tab B 高風險項 (H/H*) → Tab C 可關聯對應實驗以補齊證據。
  - Tab A/B/C 數據變化 → Gate 3.1 checklist 自動 re-evaluate。

- **表單驗證規則**：
  - Tab B `probability`：必填，1-5 → "請選擇風險發生機率"。
  - Tab B `severity`：必填，1-5 → "請選擇風險嚴重程度"。
  - Tab B `description`：必填，最少 10 字元 → "請描述風險"。
  - Tab C `hypothesis`：必填，最少 10 字元 → "請描述實驗假說"。
  - Tab C `method`：必填，最少 5 字元 → "請描述實驗方法"。
  - Tab C `success_criteria`：必填，最少 5 字元 → "請描述成功標準"。
  - Tab C `linked_assumption`：必填，至少 1 個 → "請選擇關聯假設"。
  - Tab C `result`：status=Done 時必填，最少 10 字元 → "請填寫實驗結果"。

- **資料更新策略**：
  - Tab A 證據矩陣：由假設 + 實驗數據聚合計算，純 Display，透過 React Query 自動 refetch (staleTime: 10s)。
  - Tab B 風險表格：行內編輯 auto-save (debounce 1s)，saving indicator 右上角。
  - Tab C 實驗列表：新增/編輯後自動刷新列表，並觸發 Tab A refetch (invalidateQueries)。
  - Gate check：每次 Tab 切換或數據變更時自動 GET `/api/projects/:id/gates/3.1/check`。

- **RWD 行為差異**：
  - Desktop (>1024px): Tab 水平排列。證據矩陣完整表格。P x S 矩陣 5x5 完整顯示。風險表格完整欄位。實驗卡片 2 欄。
  - Tablet (768px - 1023px): Tab 水平排列。證據矩陣可水平滾動。P x S 矩陣縮小。風險表格隱藏次要欄位 (展開查看)。實驗卡片 1 欄。
  - Mobile (<768px): Tab 改為下拉選單切換。證據矩陣轉為假設卡片式 (每張卡片顯示該假設的 E0-E4 進度條)。P x S 矩陣改為列表排序。風險/實驗表格轉為卡片式。

## [STATE DESIGN]

### Zustand Store Slice: `reviewStore`
```typescript
interface ReviewState {
  activeTab: 'evidence' | 'risk' | 'experiment';
  evidenceGapCount: number;
  highRiskWithoutMitigation: number;
  completedExperimentCount: number;
  setActiveTab: (tab: ReviewState['activeTab']) => void;
}
```

### React Query Keys
```typescript
const reviewQueryKeys = {
  evidenceMatrix: (projectId: string) => ['projects', projectId, 'evidence-matrix'],
  risks: (projectId: string) => ['projects', projectId, 'risks'],
  experiments: (projectId: string) => ['projects', projectId, 'experiments'],
  gate31: (projectId: string) => ['projects', projectId, 'gates', '3.1'],
};
```

### Cross-Tab Invalidation Flow
```
Tab C: mutation (create/update experiment)
  → invalidateQueries(['projects', projectId, 'evidence-matrix'])
  → invalidateQueries(['projects', projectId, 'gates', '3.1'])

Tab B: mutation (create/update risk)
  → invalidateQueries(['projects', projectId, 'gates', '3.1'])
```

## [DATA & API]
- **uses_api**: true
- **endpoints**:
  - GET `/api/projects/:id/evidence-matrix` -- 獲取聚合後的證據矩陣 (假設 x 證據等級 x 實驗存在狀態)。
  - GET `/api/projects/:id/risks` -- 獲取風險列表。
  - POST `/api/projects/:id/risks` -- 新增風險。
  - PUT `/api/projects/:id/risks/:risk_id` -- 更新風險 (含 P/S/mitigation)。
  - POST `/api/projects/:id/risks/ai-identify` -- AI 識別潛在風險。
  - GET `/api/projects/:id/experiments` -- 獲取實驗列表。
  - POST `/api/projects/:id/experiments` -- 新增實驗。
  - PUT `/api/projects/:id/experiments/:exp_id` -- 更新實驗 (含 result/status)。
  - POST `/api/projects/:id/experiments/ai-suggest` -- AI 建議實驗。
  - GET `/api/projects/:id/gates/3.1/check` -- 檢查 Gate 3.1 狀態。
- **response shape** (GET `/api/projects/:id/evidence-matrix`):
  ```json
  {
    "assumptions": [
      {
        "assumption_code": "A-001",
        "summary": "散熱片面積 ≥ 50cm2 足以控溫",
        "current_evidence_level": "E2",
        "experiments": [
          { "exp_code": "Exp-001", "evidence_level": "E2", "status": "Done" }
        ]
      }
    ],
    "gap_summary": {
      "e0_count": 1,
      "e1_count": 2,
      "total_assumptions": 10
    }
  }
  ```
- **response shape** (GET `/api/projects/:id/gates/3.1/check`):
  ```json
  {
    "gate_id": "3.1",
    "passed": false,
    "checklist": [
      { "label": "證據矩陣無 E0 缺口", "passed": false },
      { "label": "所有 H/H* Risk 有 mitigation", "passed": true },
      { "label": "至少 1 項實驗已完成", "passed": true }
    ]
  }
  ```
- **error cases**:
  - 證據矩陣載入失敗 (500): Tab A 顯示錯誤提示 + 重試按鈕。
  - 風險 AI 識別失敗 (500): Toast 提示 "AI 暫時不可用"，用戶可手動新增。
  - 實驗 AI 建議失敗 (500): Toast 提示，不阻塞流程。
  - 風險/實驗保存失敗 (500): 行內錯誤提示，資料保留 local state 不丟失。
  - Gate API 查詢失敗 (500): Gate 指示器顯示 ⚠️ + "無法檢查" badge (灰色)，提供重試按鈕。

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- **證據矩陣行動端轉為進度條卡片**：覆蓋 Global 預設的表格 RWD 行為 (水平滾動)，改用假設卡片 + E0-E4 進度條。原因：5 列熱力圖在窄螢幕完全失去可讀性，卡片式呈現更直觀。
- **Tab 標題帶 ⚠️ 提醒徽章**：Tab C 標題在有 evidence gap 時顯示 ⚠️ 圖示，覆蓋 Global 預設的 Tab 標題純文字規則。原因：引導用戶注意實驗迴圈 (Step 3.1.loop) 需求，是 Progressive Disclosure 的延伸。
- **P x S 矩陣行動端轉為排序列表**：覆蓋 Global 的矩陣元件 RWD 行為。原因：5x5 互動矩陣在小螢幕不可用，改為依 risk_score 降序排列的卡片列表更實用。

## [HANDOFF CHECKLIST]
- [ ] 設計稿 (Figma) 已完成 Tab A/B/C 三個 Tab 視圖及 Desktop/Tablet/Mobile 斷點。
- [ ] 熱力圖色彩 (E0 紅→E4 綠) 對比度已通過 WCAG AA 檢測。
- [ ] P x S 矩陣色彩 (H*/H/M/L) 除色彩外另有文字/圖標區分 (非色彩唯一)。
- [ ] API 契約已與後端確認 (evidence-matrix, risks, experiments, gates/3.1)。
- [ ] React Query invalidation flow 已確認跨 Tab 聯動邏輯。
- [ ] Recharts 熱力圖元件已確認可接受動態行列數。
- [ ] AI Agent 卡片 (缺口分析 / 風險識別 / 實驗建議) 遵循 Global [AI] 標籤 + 灰底規範。
- [ ] Gate 3.1 三項 checklist 條件與後端 API 一致。
- [ ] Skeleton 骨架屏已設計 Tab A/B/C 各自的 loading 態。
- [ ] E2E 測試腳本覆蓋：建立實驗→完成實驗→證據矩陣更新→Gate 通過→導航至 Decide。

## [ACCEPTANCE CRITERIA]
- [ ] Tab A 證據矩陣熱力圖正確渲染，顏色編碼 (E0 紅→E4 綠) 清晰可辨。
- [ ] Tab A Gap 分析摘要正確計算 E0/E1 項目數並高亮提示。
- [ ] Tab A AI 缺口分析卡片正確顯示灰底 + [AI] 標籤，可採用/編輯/重生成/跳過。
- [ ] Tab B P x S 色階矩陣 (5x5) 正確渲染，格子內標記對應 risk_code。
- [ ] Tab B 風險表格可新增、行內編輯、排序。P/S 填寫後 risk_score 自動計算並顯示正確色彩。
- [ ] Tab B H/H* 風險無 mitigation 時該行以淺紅底色警告。
- [ ] Tab B [AI 識別風險] 和 AI 緩解措施建議功能正常。
- [ ] Tab C 實驗卡片列表正確顯示，status 徽章色彩正確 (Plan 藍 / Running 橙 / Done 綠)。
- [ ] Tab C hypothesis / method / success_criteria 為必填，驗證正常。
- [ ] Tab C status=Done 時 result 轉為必填，驗證正常。
- [ ] Tab C [AI 建議實驗] 功能正常。
- [ ] Tab 間聯動正常：Tab C 完成實驗 → Tab A 熱力圖自動刷新；Tab A 點擊色塊 → 跳轉 Tab C。
- [ ] Gate 3.1 三項 checklist 正確反映條件，全部通過後導航按鈕啟用。
- [ ] 響應式設計在 Desktop / Tablet / Mobile 三種視口正確呈現。
- [ ] 實驗迴圈 (Step 3.1.loop) 可重複：新增實驗→完成→證據更新→再次評估缺口。

## [VERSION]
- **current_version**: v2.0
- **last_updated**: 2026-02-25
- **changelog**:
  - v1.0 -- 初版建立 (基於 Blueprint 14.5 規格)
  - v2.0 -- 完整重寫：新增 wireframe、STATE DESIGN、HANDOFF CHECKLIST；修正 Gate ID 為 3.1；細化 Tab A/B/C 元件規格；新增 AI Agent 互動模式；補充 API response shape
