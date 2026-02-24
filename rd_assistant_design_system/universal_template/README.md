# 網站設計 Prompt 通用模板系統

## 完整 Pipeline 總覽

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 0: 需求與架構（前置輸入）                                   │
│                                                                 │
│  PRD + SA 文件                                                  │
│      │                                                          │
│      ▼                                                          │
│  ① 前端設計藍圖 (00_FRONTEND_BLUEPRINT)                          │
│     Part A: 架構與技術基礎                                       │
│       → 技術選型、分層架構、設計系統、效能策略、安全規範             │
│     Part B: 資訊架構與頁面規格                                    │
│       → 頁面地圖、用戶旅程、導航結構、URL規範、頁面規格             │
│     Part C: 整合檢查清單                                         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: 設計 Prompt 產出（本模板系統）                           │
│                                                                 │
│      ▼                                                          │
│  ② Global System Prompt (01_GLOBAL)                             │
│     ← 從 Part A 萃取：配色、字體、元件風格、技術棧、UX Pattern     │
│      │                                                          │
│      ▼                                                          │
│  ③ Page-Level Prompt (02_PAGE) × N 頁                           │
│     ← 從 Part B 萃取：每頁的目標、區塊、元件、狀態、API            │
│      │                                                          │
│      ▼                                                          │
│  ④ Assembly Prompt (03_ASSEMBLY)                                │
│     → Global精簡版 + Page內容 → 丟進 Lovable / AI 工具            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: 驗證                                                   │
│                                                                 │
│  ⑤ Quality Checklist (04_QUALITY)                               │
│     → 驗證 AI 輸出是否符合規範                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: 從 PRD/SA 到前端設計藍圖

填寫 `00_FRONTEND_BLUEPRINT.template.md`，這是一份整合文件，包含：

| Part | 章節 | 萃取內容 | 下游用途 |
|------|------|----------|----------|
| **A** | §3 設計系統 | 配色、字體、圓角、陰影、Icon | → 01_GLOBAL `[VISUAL]` |
| **A** | §4 技術選型 | 框架、狀態管理、樣式方案 | → 01_GLOBAL `[TECH]` |
| **A** | §5 效能策略 | Core Web Vitals 目標 | → 01_GLOBAL 效能要求 |
| **A** | §2 系統分層 | 互動層、狀態層、通訊層 | → 02_PAGE `[INTERACTION]` `[DATA]` |
| **B** | §11 架構總覽 | 頁面總覽矩陣 | → 決定需要幾份 Page Prompt |
| **B** | §12 用戶旅程 | 旅程映射表 | → 02_PAGE `[USER CONTEXT]` |
| **B** | §13 網站地圖 | 導航連結矩陣 | → 02_PAGE `[INTERACTION]` 導航流 |
| **B** | §14 頁面規格 | 區塊結構、元件、KPI | → 02_PAGE `[SECTIONS]` `[COMPONENT]` |
| **B** | §15 數據流 | API 端點、狀態管理 | → 02_PAGE `[DATA & API]` |
| **B** | §16 URL 結構 | 路由規範 | → 02_PAGE `[PAGE META]` route_path |

---

## Phase 1: 使用模板產出 Prompt

### Step 1: 定版 Global Prompt

填寫 `01_GLOBAL_SYSTEM_PROMPT.template.md`

```
00 Part A §3 設計系統  →  Global [VISUAL DESIGN SYSTEM]
00 Part A §4 技術選型  →  Global [TECH & CONSTRAINT]
00 Part A §2 系統分層  →  Global [UX PATTERN] [INTERACTION]
PRD 產品定位           →  Global [PRODUCT] [BRAND & VOICE]
```

### Step 2: 逐頁撰寫 Page Prompt

每頁複製一份 `02_PAGE_PROMPT.template.md`

```
00 Part B §14 頁面規格  →  Page [SECTIONS] [COMPONENT SPEC]
00 Part B §12 用戶旅程  →  Page [USER CONTEXT]
00 Part B §13 網站地圖  →  Page [INTERACTION] 導航出口
00 Part B §15 數據流    →  Page [DATA & API]
00 Part B §16 URL結構   →  Page [PAGE META] route_path
```

### Step 3: 組裝最終 Prompt

用 `03_ASSEMBLY.template.md` 把 Global（精簡版）+ Page 合併。

### Step 4: 驗證輸出

用 `04_QUALITY_CHECKLIST.template.md` 檢查 AI 產出。

---

## 檔案結構

```
universal_template/
│
├── 📐 模板區（template）— 通用模板，不修改原檔，複製後填寫
│   ├── 00_FRONTEND_BLUEPRINT.template.md      # Phase 0: 前端設計藍圖
│   ├── 01_GLOBAL_SYSTEM_PROMPT.template.md    # Phase 1: 全域設計系統
│   ├── 02_PAGE_PROMPT.template.md             # Phase 1: 單頁需求規格
│   ├── 03_ASSEMBLY.template.md                # Phase 1: 組裝最終 Prompt
│   ├── 04_QUALITY_CHECKLIST.template.md       # Phase 2: 品質檢查清單
│   └── README.md                              # 本文件
│
└── 📁 output/ — 產出存放區（每次使用模板的實際產出放這裡）
    ├── 00_blueprint/                          # ← 填好的前端設計藍圖
    │   └── {專案名}_frontend_blueprint.md
    │
    ├── 01_global/                             # ← 定版的 Global Prompt
    │   └── {專案名}_global_v1.0.md
    │
    ├── 02_pages/                              # ← 各頁面 Prompt（每頁一份）
    │   ├── page_01_{頁面名}.md
    │   ├── page_02_{頁面名}.md
    │   └── ...
    │
    ├── 03_assembly/                           # ← 組裝完成，可直接丟 AI
    │   ├── assembly_01_{頁面名}.md
    │   ├── assembly_02_{頁面名}.md
    │   └── ...
    │
    └── 04_quality/                            # ← 品質檢查紀錄
        └── checklist_{專案名}_v1.0.md
```

### 模板 → 產出對應表

| 模板 (template) | 產出位置 (output/) | 命名規則 |
|-----------------|-------------------|----------|
| `00_FRONTEND_BLUEPRINT.template.md` | `output/00_blueprint/` | `{專案名}_frontend_blueprint.md` |
| `01_GLOBAL_SYSTEM_PROMPT.template.md` | `output/01_global/` | `{專案名}_global_v{版號}.md` |
| `02_PAGE_PROMPT.template.md` × N 頁 | `output/02_pages/` | `page_{序號}_{頁面名}.md` |
| `03_ASSEMBLY.template.md` × N 頁 | `output/03_assembly/` | `assembly_{序號}_{頁面名}.md` |
| `04_QUALITY_CHECKLIST.template.md` | `output/04_quality/` | `checklist_{專案名}_v{版號}.md` |

### 輸入來源對照

| 編號 | 用途 | 輸入來源 |
|------|------|----------|
| 00 | 前端設計藍圖（架構 + 資訊架構） | PRD + SA |
| 01 | 專案層：全域設計系統 | 00 Part A + PRD |
| 02 | 頁面層：單頁需求規格 | 00 Part B §14 |
| 03 | 組裝層：最終丟 AI 的 prompt | 01 + 02 |
| 04 | 品質檢查清單 | 01 全域規範 |

---

## 核心原則

1. **先架構，再設計** — 先完成 00 藍圖，再進入 Prompt 模板
2. **先立憲，再寫法** — 先定 Global，再寫每頁 Page
3. **一頁一 PRD，一次一任務** — 組裝時只處理一頁
4. **全域約束 > 在地細節** — Global 不可被 Page 推翻，除非在 EXCEPTION 明確說明
5. **資料有源頭** — 每個 placeholder 都能追溯到 00 的具體章節
