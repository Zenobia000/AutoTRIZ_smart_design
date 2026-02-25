# RD Design Copilot 命名規範 (Naming Convention)

> **版本**: v1.1 | **日期**: 2026-02-25
> **目的**: 統一流程節點（Phase / Step / Gate / Activity）的命名規則與階層關係，確保 UX 一致性與可預測性。

---

## 1. 設計原則

1. **一致性 (Consistency)**: 相同層級一律用相同命名模式
2. **可預測性 (Predictability)**: 看到編號就知道在哪個 Phase、第幾步
3. **簡潔性 (Brevity)**: 編號短，適合 UI sidebar 和 breadcrumb
4. **語意清晰 (Semantic Clarity)**: 名字本身傳達目的，不需查表

---

## 2. 階層結構

```
Phase (大階段)
  └── Step (步驟)          → Gate (步驟閘門)
        └── Activity (子活動)  → Activity Gate (子活動閘門)

Phase 之間: Phase Gate (階段閘門)
```

### 層級定義

| 層級 | 定義 | 命名格式 | 範例 |
|------|------|---------|------|
| **Phase** | 大階段，代表設計流程的宏觀階段 | `Phase {N}: {英文名}` | Phase 1: Define |
| **Step** | 步驟，Phase 內的主要活動單元 | `Step {Phase}.{Seq}` | Step 1.1, Step 2.2 |
| **Activity** | 子活動，Step 內的細分動作 | `Step {Phase}.{Step}.{Seq}` | Step 2.2.1, Step 2.2.2 |
| **Loop** | 迴圈步驟，可反覆執行 | `Step {Phase}.{Step}.loop` | Step 3.1.loop |
| **Gate** | 閘門，控制流程推進 | `Gate {對應 Step 編號}` | Gate 1.1, Gate 2.2 |
| **Phase Gate** | 階段閘門，觸發 Phase 轉換 | `Phase Gate {N}` (= Gate {N}.{last}) | Phase Gate 1 (= Gate 1.3) |
| **Activity Gate** | 子活動閘門 | `Gate {對應 Activity 編號}` | Gate 2.2.1 |

---

## 3. 完整命名映射

### 3.1 Phase

| 編號 | 英文名 | 中文名 | DB 狀態值 |
|------|--------|--------|----------|
| Phase 1 | Define | 定義問題空間 | `PHASE_1` |
| Phase 2 | Diverge | 假設與發散 | `PHASE_2` |
| Phase 3 | Converge | 收斂與驗證 | `PHASE_3` |

專案狀態流轉: `DRAFT` → `PHASE_1` → `PHASE_2` → `PHASE_3` → `COMPLETED`

### 3.2 Step & Activity

#### Phase 1: Define (定義問題空間)

| 編號 | 名稱 | 方法論 | 核心工件 |
|------|------|--------|---------|
| **Step 1.1** | 問題界定 | 白帽 + 5W1H | Constraint |
| **Step 1.2** | 理解全貌 | 索克拉底問答 | Contradiction, Assumption |
| **Step 1.3** | 系統建模 | 因果迴路 + TRIZ 矛盾 + 斷路點 | Contradiction, Breakpoint |

#### Phase 2: Diverge (假設與發散)

| 編號 | 名稱 | 方法論 | 核心工件 |
|------|------|--------|---------|
| **Step 2.1** | 假設驗證規劃 | HDA + 未知集合 | Assumption |
| **Step 2.2** | 創造與調整 | TRIZ + SCAMPER + MUST | Concept Route, Interface |
| Step 2.2.1 | Anti-Anchor Sprint | 反路徑依賴 | — |
| Step 2.2.2 | TRIZ 解矛盾 | 矩陣查表 + 原理具體化 | Concept Route (部分) |
| Step 2.2.3 | 子系統定義 | 受影響子系統識別 | Concept Route (部分) |
| Step 2.2.4 | SCAMPER 變形 | 每子系統 × 7 動作 | Concept Route (部分) |
| Step 2.2.5 | 方案生成 | 整合 TRIZ + SCAMPER | Concept Route, Interface |
| Step 2.2.6 | MUST 快篩 | Go/No-Go 淘汰 | Concept Route |
| **Step 2.3** | Pre-CAD 審查 | Pre-CAD Gate | Pre-CAD Review Report |

#### Phase 3: Converge (收斂與驗證)

| 編號 | 名稱 | 方法論 | 核心工件 |
|------|------|--------|---------|
| **Step 3.1** | 設計審查 | CAD Gate - MVP CAD Review | Evidence Matrix, Risk, MVP CAD Model |
| **Step 3.1.loop** | 證據補齊 | Evidence Closure (迴圈) | Evidence |
| **Step 3.2** | 決策與行動 | KT Decision Analysis | Decision Record |
| **Step 3.3** | 內化與傳達 | 費曼 | Asset |

### 3.3 Gate

| Gate | 位置 | 類型 | Phase 轉換 | 關鍵工件狀態轉換 |
|------|------|------|-----------|-----------------|
| **Gate 1.1** | Step 1.1 → Step 1.2 | Step Gate | — | Constraint: Draft → Reviewed |
| **Gate 1.2** | Step 1.2 → Step 1.3 | Step Gate | — | Contradiction, Assumption: Draft → Reviewed |
| **Phase Gate 1** (= Gate 1.3) | Step 1.3 → Step 2.1 | **Phase Gate** | **Phase 1 → Phase 2** | Contradiction: Reviewed → Verified; Breakpoint: Draft → Reviewed |
| **Gate 2.1** | Step 2.1 → Step 2.2 | Step Gate | — | Assumption: Reviewed → Verified |
| **Gate 2.2.1** | Step 2.2.1 → Step 2.2.2 | Activity Gate | — | ≥1 非對標路線且初步通過 M1 + M4 |
| **Gate 2.2** | Step 2.2 → Step 2.3 | Step Gate | — | Concept Route, Interface: Draft → Reviewed |
| **Phase Gate 2** (= Gate 2.3) | Step 2.3 → Step 3.1 | **Phase Gate** | **Phase 2 → Phase 3** | Concept Route: Reviewed → Verified; Pre-CAD Review Report: Draft → Reviewed |
| **Gate 3.1** | Step 3.1 → Step 3.1.loop / Step 3.2 | Step Gate | — | Evidence Matrix, Risk: Draft → Reviewed |
| **Gate 3.2** | Step 3.2 → Step 3.3 | Step Gate | — | Concept Route: Verified → Baselined; Decision Record: Draft → Reviewed |
| **Phase Gate 3** (= Gate 3.3) | Step 3.3 → Completed | **Phase Gate** | **Phase 3 → Completed** | All Core Artifacts: Baselined → Released |

---

## 4. 舊名 → 新名 對照表

### 4.1 Step 對照

| 舊名 | 新名 |
|------|------|
| Step 1 | Step 1.1 |
| Step 2 | Step 1.2 |
| Step 3 | Step 1.3 |
| Step 4 | Step 2.1 |
| Step 5 | Step 2.2 |
| Step 5-0 | Step 2.2.1 |
| Step 5a | Step 2.2.2 |
| Step 5b | Step 2.2.3 |
| Step 5c | Step 2.2.4 |
| Step 5d | Step 2.2.5 |
| Step 5e | Step 2.2.6 |
| Step P | Step 2.3 |
| Step 6 | Step 3.1 |
| Step 6e | Step 3.1.loop |
| Step 7 | Step 3.2 |
| Step 8 | Step 3.3 |

### 4.2 Gate 對照

| 舊名 | 新名 |
|------|------|
| Gate 1 | Gate 1.1 |
| Gate 2 | Gate 1.2 |
| Gate 3 | Phase Gate 1 (= Gate 1.3) |
| Gate 4 | Gate 2.1 |
| Anti-Anchor Gate | Gate 2.2.1 |
| Gate P / Gate 5 | Gate 2.2 |
| Gate C | Phase Gate 2 (= Gate 2.3) |
| Gate 6 | Gate 3.1 |
| Gate 7 | Gate 3.2 |
| Gate 8 | Phase Gate 3 (= Gate 3.3) |

### 4.3 Phase 對照

| 舊名 | 新名 |
|------|------|
| Phase I | Phase 1: Define |
| Phase II | Phase 2: Diverge |
| Phase III | Phase 3: Converge |
| PHASE_I (DB) | PHASE_1 |
| PHASE_II (DB) | PHASE_2 |
| PHASE_III (DB) | PHASE_3 |

---

## 5. UI 呈現規則

### 5.1 Sidebar 導覽

```
Phase 1: Define
  ├── 1.1 問題界定
  ├── 1.2 理解全貌
  └── 1.3 系統建模
Phase 2: Diverge
  ├── 2.1 假設驗證規劃
  ├── 2.2 創造與調整
  │     ├── 2.2.1 Anti-Anchor Sprint
  │     ├── 2.2.2 TRIZ 解矛盾
  │     ├── 2.2.3 子系統定義
  │     ├── 2.2.4 SCAMPER 變形
  │     ├── 2.2.5 方案生成
  │     └── 2.2.6 MUST 快篩
  └── 2.3 Pre-CAD 審查
Phase 3: Converge
  ├── 3.1 設計審查
  │     └── 3.1.loop 證據補齊
  ├── 3.2 決策與行動
  └── 3.3 內化與傳達
```

### 5.2 Breadcrumb

```
Phase 1: Define > Step 1.2 理解全貌
Phase 2: Diverge > Step 2.2 創造與調整 > 2.2.4 SCAMPER 變形
Phase 3: Converge > Step 3.1 設計審查 > 3.1.loop 證據補齊
```

### 5.3 Gate 顯示

- Step Gate: 在 Step 完成後顯示為 checkpoint（如 `✅ Gate 1.1 通過`）
- Phase Gate: 醒目顯示為里程碑（如 `🏁 Phase Gate 1 通過 → 進入 Phase 2: Diverge`）
- Activity Gate: 在 Activity 內部顯示（如 `✅ Gate 2.2.1 通過`）

---

## 6. 程式碼命名規則

### 6.1 DB 狀態值

```python
# project.status
VALID_STATUSES = ["DRAFT", "PHASE_1", "PHASE_2", "PHASE_3", "COMPLETED"]
```

### 6.2 Gate 編號 (程式碼中)

```python
# gate_id 使用字串點記法表示（與 UI / 文件一致）
# DB: GateCheck.gate_id = String(10)
# API: GET /projects/{pid}/gates/{gate_id}/check
VALID_GATES = {
    "1.1",   # Gate 1.1 — Step Gate
    "1.2",   # Gate 1.2 — Step Gate
    "1.3",   # Phase Gate 1
    "2.1",   # Gate 2.1 — Step Gate
    "2.2",   # Gate 2.2 — Step Gate
    "2.3",   # Phase Gate 2
    "3.2",   # Gate 3.2 — Step Gate
    "3.3",   # Phase Gate 3
}
```

### 6.3 Step 編號 (程式碼中)

```python
# step_id 使用字串表示
VALID_STEPS = [
    "1.1", "1.2", "1.3",
    "2.1", "2.2", "2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5", "2.2.6", "2.3",
    "3.1", "3.1.loop", "3.2", "3.3",
]
```

---

**版本**: v1.1
**最後更新**: 2026-02-25
**適用範圍**: RD Design Copilot 所有文件、程式碼、UI
