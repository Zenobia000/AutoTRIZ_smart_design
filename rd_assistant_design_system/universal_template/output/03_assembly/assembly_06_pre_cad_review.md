# Assembly Prompt — Pre-CAD 審查

> **使用方式**：填完後，將下方 ``` 區塊內的完整內容複製貼到 Lovable / Claude / GPT-4 等 AI 工具。

---

```markdown
=== GLOBAL PROJECT GUIDELINE (DO NOT OVERRIDE) ===

你是「RD Design Copilot」專案的資深產品設計師與前端工程師，負責維護整個專案的設計一致性。

### 核心設計系統
- **配色**：Primary(#007bff) / Secondary(#6c757d) / Accent(#fd7e14) / Error(#dc3545)
- **字體**："Noto Sans TC", "Helvetica Neue", Arial, "Segoe UI", sans-serif，模組化比例 1.25
- **元件風格**：圓角 8px (0.5rem)，輕微陰影，增加層次感 (e.g., box-shadow: 0 4px 6px rgba(0,0,0,0.1))，1px solid $color-divider
- **語氣**：專業精準、結構化、數據驅動、實用主義
- **技術棧**：React (Frontend)

### 重要規範
- 本區段定義整個專案的設計系統與風格
- 所有頁面相關需求都必須遵守這裡的規範
- 除非在 [EXCEPTION TO GLOBAL RULES] 中明確說明，否則不准違反

=== CURRENT TASK: BUILD ONE PAGE ===

本次任務：根據上方 Global Guideline，設計並實作「Pre-CAD 審查」。

### [PAGE SPECIFICATION]

**頁面元資料**：
- 路徑：`/projects/:id/pre-cad-review`
- 類型：列表/詳情/審查表單
- 主要目標：在投入大量 CAD 繪製和詳細模擬之前，利用「可驗證的最小信息」篩選和縮減候選設計方案。
- 次要目標：記錄 Pre-CAD 審查過程與結果，確保決策可追溯。

**目標用戶**：
- 主要：RD 主管, RD 工程師
- 次要：專案經理 (PM), 製造工程師

**進入方式**：
- 從「方案探索頁面」完成後自動導航，或從「專案儀表板」點擊導航進入。
- 預估停留時間：中 (15-25 分鐘)

**頁面結構**（由上至下）：

1. **候選方案列表區**
   - 用途：展示通過 MUST 快篩的候選設計方案概覽，供審查團隊選擇。
   - 佈局：響應式列表或卡片佈局。
   - 元件：
     - `方案卡片/列表項` (card/list item, required)：顯示方案名稱（最長 100 字元）、簡短描述、MUST 快篩結果 (以標籤或圖標表示)、操作按鈕 (查看詳情)。
   - 狀態：正常、empty（無候選方案時顯示「沒有候選方案」提示）、loading（方案載入中顯示骨架屏）、error（數據載入失敗）

2. **Pre-CAD 審查表單區**
   - 用途：根據審查維度（MUST、解耦、可驗證性、主要風險、最小 CAD 工作量）評估並記錄審查結果。
   - 佈局：模態框 (Modal) 或頁面內展開式表單佈局。
   - 元件：
     - `審查維度評估` (checklist/rating, required)：每個維度 (如空間約束、解耦程度) 包含評估輸入 (文字/選擇框) 和證據上傳選項。
     - `評估摘要` (textarea, optional)：輸入此維度的簡短評估總結。最長 200 字元。
   - 狀態：正常、error（評估項未完成或輸入不符合要求）

3. **審查結論與決策區**
   - 用途：總結審查結果，決定保留方案，並記錄結論。
   - 佈局：底部固定操作欄或獨立區塊。
   - 元件：
     - `保留方案選擇器` (checkbox group/multi-select, required)：從候選方案中選擇 3-5 條要保留的方案。
     - `審查結論備註` (textarea, optional)：記錄審查會議的關鍵討論和決策原因。最長 500 字元。
     - `批准審查按鈕` (button primary, required)：點擊後保存審查結果並推進專案階段。
   - 狀態：正常、disabled（未選擇足夠方案或評估項未完成時按鈕禁用）、loading（提交中顯示 Loading Spinner）

**互動要求**：
1. 用戶進入 Pre-CAD 審查頁面，系統載入通過 MUST 快篩的候選方案列表。
2. 用戶點擊某方案，打開 Pre-CAD 審查表單進行詳細評估和記錄。
3. 用戶完成所有評估後，從候選方案中選擇 3-5 條要保留的方案，並點擊「批准審查」按鈕。
4. 審查結果成功提交後，專案狀態推進至下一階段。

**表單驗證規則**：
- `保留方案選擇器`: 必須選擇 3-5 條方案 → 請至少選擇 3 條候選方案。
- `審查維度評估`: 所有審查維度必須填寫 → 所有評估項為必填。

**資料更新策略**：
- 保存審查結果後，候選方案列表和專案狀態自動刷新。

**資料處理**：
- API 端點：
  - GET `/api/projects/:id/solutions/candidates` — 獲取通過 MUST 快篩的候選方案列表。
  - POST `/api/projects/:id/pre-cad-reviews` — 提交 Pre-CAD 審查結果。
- 載入策略：漸進式載入 (Skeleton Screen)，關鍵數據優先。
- 錯誤處理：
  - 獲取候選方案失敗：頁面顯示錯誤提示訊息，提供重試按鈕。
  - 提交審查結果失敗：顯示提交失敗提示，並提供重新提交選項。

**RWD 行為差異**：
- Desktop (>1024px)：候選方案列表和審查表單可並排顯示，提升審查效率。
- Tablet (768px - 1023px)：佈局調整為堆疊，審查表單可能以全屏形式顯示。
- Mobile (<768px)：列表卡片化，審查表單以全屏模態框顯示。

=== EXCEPTION RULES ===

本頁面允許的例外（如有）：
- 無特殊例外，完全遵循 Global System Prompt 規範。

=== OUTPUT REQUIREMENTS ===

請依照以下步驟輸出：

### Step 1: 結構確認
列出本頁面的：
- 主要 sections 及其用途
- 每個 section 的關鍵元件
- 資料流與狀態管理策略

### Step 2: 設計決策說明
說明 2-3 個關鍵設計決策：
- 決策點與選擇理由
- 如何確保與 Global 規範一致
- 任何必要的權衡考量

### Step 3: 實作方案
產出完整的 React 程式碼，包含：
- 元件結構與 props 定義
- 狀態管理邏輯
- 互動處理與錯誤處理
- 響應式設計
- 關鍵區塊註解

### 品質檢查清單
- [ ] 色彩系統一致性
- [ ] 字體層級正確
- [ ] 元件風格統一
- [ ] 響應式設計完整
- [ ] 狀態處理完善（loading / error / empty）
```

---

**執行優先順序**：
1. Global 規範為最高優先級
2. Page 特定需求次之
3. Exception 需明確說明且最小化

**版本資訊**：
- Global System Prompt 版本：v1.0
- Assembly 日期：2026-02-24
- 負責人：AI Agent
