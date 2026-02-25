# output/ — 專案產出存放區

此資料夾用於存放每次使用模板系統產出的實際文件。
每個新專案建議複製整個 `output/` 結構，或在此下建立專案子資料夾。

## 資料夾結構與存放規則

```
output/
├── 00_blueprint/       ← Phase 0 產出：前端設計藍圖
│   └── {專案名}_frontend_blueprint.md
│
├── 01_global/          ← Phase 1-Step1 產出：全域設計系統
│   └── {專案名}_global_v1.0.md
│
├── 02_pages/           ← Phase 1-Step2 產出：各頁面 Prompt（每頁一份）
│   ├── page_01_{頁面名}.md
│   ├── page_02_{頁面名}.md
│   ├── page_03_{頁面名}.md
│   └── ...
│
├── 03_assembly/        ← Phase 1-Step3 產出：組裝完成可直接丟 AI 的 Prompt
│   ├── assembly_01_{頁面名}.md
│   ├── assembly_02_{頁面名}.md
│   └── ...
│
└── 04_quality/         ← Phase 2 產出：品質檢查紀錄
    ├── checklist_{專案名}_v1.0.md
    └── review_log_{日期}.md
```

## 命名規則

| 資料夾 | 命名格式 | 範例 |
|--------|----------|------|
| `00_blueprint/` | `{專案名}_frontend_blueprint.md` | `tmf_kb_frontend_blueprint.md` |
| `01_global/` | `{專案名}_global_v{版號}.md` | `tmf_kb_global_v1.0.md` |
| `02_pages/` | `page_{序號}_{頁面名}.md` | `page_01_dashboard.md` |
| `03_assembly/` | `assembly_{序號}_{頁面名}.md` | `assembly_01_dashboard.md` |
| `04_quality/` | `checklist_{專案名}_v{版號}.md` | `checklist_tmf_kb_v1.0.md` |

## 對應關係

```
模板 (template)                          產出 (output)
─────────────────                        ─────────────
00_FRONTEND_BLUEPRINT.template.md   →    00_blueprint/{專案名}_frontend_blueprint.md
01_GLOBAL_SYSTEM_PROMPT.template.md →    01_global/{專案名}_global_v1.0.md
02_PAGE_PROMPT.template.md (× N)    →    02_pages/page_01_{名}.md ~ page_N_{名}.md
03_ASSEMBLY.template.md (× N)       →    03_assembly/assembly_01_{名}.md ~ assembly_N_{名}.md
04_QUALITY_CHECKLIST.template.md    →    04_quality/checklist_{專案名}_v1.0.md
```

## 版本管理

- `01_global/` 內的文件有版號（v1.0 → v1.1），改版時保留舊版
- `02_pages/` 的序號對應 Blueprint Part B §11 頁面總覽矩陣的編號
- `03_assembly/` 的序號與 `02_pages/` 一一對應
