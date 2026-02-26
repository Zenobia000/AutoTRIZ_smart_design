# output/ — 專案產出存放區

此資料夾存放 RD Design Copilot 模板系統產出的實際設計文件。
所有文件基於 **6+1 頁面架構 v2.0** 和 **Apple 設計哲學**。

## 資料夾結構

```
output/
├── 00_blueprint/       ← 前端設計藍圖 (Part A + Part B)
│   └── RD_Design_Copilot_frontend_blueprint.md
│
├── 01_global/          ← 全域系統 Prompt (v2.0)
│   └── RD_Design_Copilot_global_v1.0.md
│
├── 02_pages/           ← 各頁面 Page-Level Prompt（7 份，對應 6+1 頁面）
│   ├── page_00_dashboard.md    ← Dashboard (專案總覽)
│   ├── page_01_brief.md        ← Brief (定義簡報) — Step 1.1
│   ├── page_02_explore.md      ← Explore (問題探索) — Step 1.2+1.3
│   ├── page_03_track.md        ← Track (假設追蹤) — Step 2.1
│   ├── page_04_create.md       ← Create (方案創造) — Step 2.2+2.3
│   ├── page_05_review.md       ← Review (設計審查) — Step 3.1+3.1.loop
│   └── page_06_decide.md       ← Decide (最終決策) — Step 3.2+3.3
│
├── 03_assembly/        ← 組裝完成的完整 Prompt（Global + Page，可直接餵入 AI）
│   ├── assembly_00_dashboard.md
│   ├── assembly_01_brief.md
│   ├── assembly_02_explore.md
│   ├── assembly_03_track.md
│   ├── assembly_04_create.md
│   ├── assembly_05_review.md
│   └── assembly_06_decide.md
│
└── 04_quality/         ← 品質檢查紀錄
    └── checklist_{專案名}_v{版號}.md
```

## 6+1 頁面對照表

| # | 頁面 | 檔案 | 對應 Step | 內嵌 Gate | 頁型 |
|---|------|------|-----------|-----------|------|
| 0 | Dashboard | page_00 / assembly_00 | — | — | dashboard |
| 1 | Brief | page_01 / assembly_01 | 1.1 | Gate 1.1 | form |
| 2 | Explore | page_02 / assembly_02 | 1.2, 1.3 | Gate 1.2, Phase Gate 1 | tabs (3) |
| 3 | Track | page_03 / assembly_03 | 2.1 | Gate 2.1 | tabs (2) |
| 4 | Create | page_04 / assembly_04 | 2.2.1~2.2.6, 2.3 | Gate 2.2, Phase Gate 2 | accordion (7) |
| 5 | Review | page_05 / assembly_05 | 3.1, 3.1.loop | Gate 3.1 | tabs (3) |
| 6 | Decide | page_06 / assembly_06 | 3.2, 3.3 | Gate 3.2, Phase Gate 3 | tabs (3) |

## 使用方式

1. **分批餵入 AI 工具** (Lovable / Claude / GPT-4):
   - 先餵 `assembly_XX.md` (已包含 Global + Page 完整內容)
   - 或分開餵: 先 `01_global/` 再 `02_pages/page_XX.md`

2. **版本**: v2.0 (2026-02-25)
   - 6+1 頁面架構
   - Apple 設計哲學 (Progressive Disclosure, Direct Manipulation, AI as Invisible Infrastructure)
   - 8-Gate 內嵌系統
   - 必填/Agent/Display 三分類
