# TRIZ Knowledge Base — Prompt Markdown 參照表

## 用途

本資料夾存放 TRIZ 方法論的結構化參照表，以 Markdown 格式供 Copilot Prompt / RAG 上下文注入使用。
所有表格皆為**靜態知識**（TRIZ 經典理論幾乎不變），版本管理透過 Git 即可。

## 檔案清單

| 檔案 | 內容 | 筆數 | 用於 Copilot Step |
|------|------|------|------------------|
| `01_39_parameters.md` | TRIZ 39 工程參數 | 39 筆 | Step 3 (矛盾定義) |
| `02_contradiction_matrix.md` | 39×39 矛盾矩陣 | 1,521 格 | Step 5a-1 (查表推薦) |
| `03_40_principles.md` | TRIZ 40 發明原理 + 子原理 | 40 筆 | Step 5a (原理具體化) |
| `04_separation_principles.md` | 物理矛盾分離原則 | 4 大類 | Step 5a-2 (分離策略) |
| `05_76_standard_solutions.md` | Su-Field 76 標準解 | 76 筆 (5 大類) | Step 5a-3 (標準解) |

## 使用方式

### 方式 1：全量注入 (小模型/短矩陣)
直接將對應 `.md` 檔內容放入 System Prompt 或 User Message 上下文。

### 方式 2：RAG 檢索注入 (推薦用於矛盾矩陣)
矛盾矩陣 39×39 佔大量 token，建議：
1. Step 3 確定改善/惡化參數後
2. 僅檢索矩陣中對應的 1-3 行注入上下文
3. LLM 從候選原理中選擇並具體化

### 方式 3：混合注入
- 39 參數 + 分離原則 + 40 原理 → 全量注入（token 可控）
- 矛盾矩陣 + 76 標準解 → RAG 按需檢索

## Token 估算

| 檔案 | 預估字元數 | 預估 token (中英混合) |
|------|-----------|---------------------|
| 39 參數 | ~3,000 | ~1,500 |
| 矛盾矩陣 (全量) | ~40,000 | ~15,000 |
| 矛盾矩陣 (單行) | ~500 | ~200 |
| 40 原理 | ~8,000 | ~4,000 |
| 分離原則 | ~2,000 | ~1,000 |
| 76 標準解 | ~12,000 | ~5,000 |

## 與整合流程的對應

```
RD_Design_Copilot_整合流程.md §1.5 AutoTRIZ 混合架構
  │
  ├── 規則引擎區 (本資料夾提供參照表)
  │   ├── Step 3.4 → 01_39_parameters.md (參數驗證)
  │   ├── Step 5a-1 → 02_contradiction_matrix.md (查表)
  │   ├── Step 5a-2 → 04_separation_principles.md (分離)
  │   └── Step 5a-3 → 05_76_standard_solutions.md (標準解)
  │
  └── LLM 驅動區 (使用參照表作為上下文)
      ├── Step 3.4 → LLM 翻譯人話→參數 (參考 01)
      └── Step 5a-4 → LLM 原理具體化 (參考 03)
```
