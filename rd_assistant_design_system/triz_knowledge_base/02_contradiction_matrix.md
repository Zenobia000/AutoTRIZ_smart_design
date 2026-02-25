# TRIZ 39×39 矛盾矩陣 (Contradiction Matrix)

> **用途**：Step 2.2.2 矛盾矩陣查表。給定改善參數和惡化參數，查詢推薦的 TRIZ 發明原理。
> **注入方式**：RAG 按需檢索——Step 1.3 確定參數後，僅注入相關行（~200 token/行）。

## 讀法

- **行** = 改善參數 (Improving Parameter)
- **列** = 惡化參數 (Worsening Parameter)
- **格值** = 推薦的 TRIZ 40 發明原理編號
- 空格 = 該組合無經典推薦（可嘗試物理矛盾分離原則）

---

## 參數 1: 移動物體的重量 (Weight of moving object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 2 靜止物體的重量 (Weight of stationary object) | 15, 8, 29, 34 |
| 3 移動物體的長度 (Length of moving object) | 29, 17, 38, 34 |
| 4 靜止物體的長度 (Length of stationary object) | 29, 2, 40, 28 |
| 5 移動物體的面積 (Area of moving object) | 2, 17, 29, 4 |
| 7 移動物體的體積 (Volume of moving object) | 2, 26, 29, 40 |
| 8 靜止物體的體積 (Volume of stationary object) | 2, 26, 29, 40 |
| 9 速度 (Speed) | 2, 28, 13, 38 |
| 10 力 (Force) | 8, 10, 18, 37 |
| 11 應力/壓力 (Stress or pressure) | 10, 36, 37, 40 |
| 12 形狀 (Shape) | 10, 14, 35, 40 |
| 13 物體結構的穩定性 (Stability of composition) | 1, 8, 10, 29 |
| 14 強度 (Strength) | 1, 8, 15, 34 |
| 15 移動物體的耐久性 (Durability of moving object) | 19, 5, 34, 31 |
| 17 溫度 (Temperature) | 36, 22, 6, 38 |
| 18 照度/亮度 (Illumination intensity) | 19, 1, 32 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 12, 18, 28, 31 |
| 21 功率 (Power) | 8, 36, 38, 31 |
| 22 能量損失 (Loss of energy) | 15, 6, 19, 28 |
| 23 物質損失 (Loss of substance) | 35, 6, 23, 40 |
| 25 時間浪費 (Loss of time) | 6, 29, 4, 38 |
| 26 物質的量 (Quantity of substance) | 29, 30, 34 |
| 28 量測精度 (Measurement accuracy) | 1, 26, 2, 36 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 21, 18, 27 |
| 33 可操作性 (Ease of operation) | 2, 27, 28, 11 |
| 34 可修復性 (Ease of repair) | 1, 6, 15, 8 |
| 35 適應性/多功能性 (Adaptability) | 15, 29, 37, 28 |
| 36 裝置複雜度 (Device complexity) | 26, 30, 34, 36 |
| 39 生產力/效率 (Productivity) | 35, 3, 24, 37 |

## 參數 2: 靜止物體的重量 (Weight of stationary object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 10, 1, 29, 35 |
| 3 移動物體的長度 (Length of moving object) | 35, 30, 13, 2 |
| 5 移動物體的面積 (Area of moving object) | 5, 35, 14, 2 |
| 6 靜止物體的面積 (Area of stationary object) | 30, 2, 14, 18 |
| 7 移動物體的體積 (Volume of moving object) | 35, 8, 2, 14 |
| 8 靜止物體的體積 (Volume of stationary object) | 35, 8, 2, 14 |
| 9 速度 (Speed) | 10, 15, 36, 28 |
| 10 力 (Force) | 13, 29, 10, 18 |
| 11 應力/壓力 (Stress or pressure) | 13, 10, 29, 14 |
| 12 形狀 (Shape) | 35, 1, 40, 18 |
| 13 物體結構的穩定性 (Stability of composition) | 2, 11, 13 |
| 14 強度 (Strength) | 28, 2, 27 |
| 17 溫度 (Temperature) | 6, 22, 26, 1 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 19, 6, 18, 26 |
| 22 能量損失 (Loss of energy) | 19, 6, 18, 26 |
| 25 時間浪費 (Loss of time) | 10, 20, 26, 5 |
| 26 物質的量 (Quantity of substance) | 35, 2, 10, 34 |
| 27 可靠性 (Reliability) | 11, 28, 1, 34 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 1, 18, 4 |
| 33 可操作性 (Ease of operation) | 27, 2, 39, 35 |
| 34 可修復性 (Ease of repair) | 15, 1, 28, 16 |
| 35 適應性/多功能性 (Adaptability) | 1, 15, 29, 4 |
| 36 裝置複雜度 (Device complexity) | 26, 30, 36, 34 |
| 39 生產力/效率 (Productivity) | 28, 29, 15, 16 |

## 參數 3: 移動物體的長度 (Length of moving object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 8, 15, 29, 34 |
| 4 靜止物體的長度 (Length of stationary object) | 15, 17, 4 |
| 7 移動物體的體積 (Volume of moving object) | 7, 17, 4, 35 |
| 8 靜止物體的體積 (Volume of stationary object) | 35, 8, 2, 14 |
| 9 速度 (Speed) | 13, 4, 8 |
| 10 力 (Force) | 17, 10, 4 |
| 11 應力/壓力 (Stress or pressure) | 1, 8, 35 |
| 12 形狀 (Shape) | 1, 8, 10, 29 |
| 13 物體結構的穩定性 (Stability of composition) | 1, 8, 15, 34 |
| 14 強度 (Strength) | 8, 35, 29, 34 |
| 17 溫度 (Temperature) | 36, 22 |
| 25 時間浪費 (Loss of time) | 4, 29, 23, 10 |
| 26 物質的量 (Quantity of substance) | 1, 29, 4, 35 |
| 28 量測精度 (Measurement accuracy) | 1, 26 |
| 31 物體產生的有害副作用 (Harmful side effects) | 1, 24 |
| 33 可操作性 (Ease of operation) | 4, 28, 10, 34 |
| 35 適應性/多功能性 (Adaptability) | 15, 29, 28, 37 |
| 36 裝置複雜度 (Device complexity) | 14, 4, 28, 29 |
| 39 生產力/效率 (Productivity) | 10, 14, 34, 17 |

## 參數 4: 靜止物體的長度 (Length of stationary object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 35, 28, 40, 29 |
| 3 移動物體的長度 (Length of moving object) | 17, 7, 10, 40 |
| 7 移動物體的體積 (Volume of moving object) | 35, 8, 2, 14 |
| 9 速度 (Speed) | 28, 10, 1, 39 |
| 10 力 (Force) | 15, 17, 27 |
| 11 應力/壓力 (Stress or pressure) | 40, 26 |
| 13 物體結構的穩定性 (Stability of composition) | 2, 11, 13 |
| 14 強度 (Strength) | 40, 26, 27, 1 |
| 17 溫度 (Temperature) | 22, 26, 2 |
| 26 物質的量 (Quantity of substance) | 30, 29, 14 |
| 28 量測精度 (Measurement accuracy) | 26, 28, 32, 3 |
| 31 物體產生的有害副作用 (Harmful side effects) | 14, 22, 19, 32 |
| 33 可操作性 (Ease of operation) | 2, 5 |
| 35 適應性/多功能性 (Adaptability) | 1, 15, 17, 28 |
| 36 裝置複雜度 (Device complexity) | 1, 26, 26 |

## 參數 5: 移動物體的面積 (Area of moving object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 2, 17, 29, 4 |
| 6 靜止物體的面積 (Area of stationary object) | 29, 30, 4, 34 |
| 7 移動物體的體積 (Volume of moving object) | 15, 17, 4 |
| 9 速度 (Speed) | 29, 30, 34 |
| 10 力 (Force) | 19, 30, 35, 2 |
| 11 應力/壓力 (Stress or pressure) | 10, 15, 36, 28 |
| 12 形狀 (Shape) | 5, 34, 29, 4 |
| 14 強度 (Strength) | 30, 26, 35, 2 |
| 17 溫度 (Temperature) | 19, 32, 26 |
| 26 物質的量 (Quantity of substance) | 29, 30, 6, 13 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 33, 28, 1 |
| 33 可操作性 (Ease of operation) | 15, 32, 35, 2 |
| 36 裝置複雜度 (Device complexity) | 2, 18, 40, 4 |
| 39 生產力/效率 (Productivity) | 30, 26 |

## 參數 6: 靜止物體的面積 (Area of stationary object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 30, 2, 14, 18 |
| 5 移動物體的面積 (Area of moving object) | 26, 7, 9, 39 |
| 7 移動物體的體積 (Volume of moving object) | 2, 38, 7, 35 |
| 9 速度 (Speed) | 1, 18, 35, 36 |
| 10 力 (Force) | 10, 15, 36, 37 |
| 11 應力/壓力 (Stress or pressure) | 36, 35, 21 |
| 14 強度 (Strength) | 30, 26, 35, 2 |
| 16 靜止物體的耐久性 (Durability of stationary object) | 39, 30, 35, 4 |
| 17 溫度 (Temperature) | 19, 32, 26 |
| 26 物質的量 (Quantity of substance) | 29, 1, 40 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 33, 28, 1 |
| 36 裝置複雜度 (Device complexity) | 2, 18, 40, 4 |

## 參數 7: 移動物體的體積 (Volume of moving object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 2, 26, 29, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 1, 7, 4, 35 |
| 3 移動物體的長度 (Length of moving object) | 7, 17, 4, 35 |
| 4 靜止物體的長度 (Length of stationary object) | 35, 8, 2, 14 |
| 5 移動物體的面積 (Area of moving object) | 15, 13, 30, 26 |
| 6 靜止物體的面積 (Area of stationary object) | 2, 38, 7, 35 |
| 9 速度 (Speed) | 29, 4, 38, 34 |
| 10 力 (Force) | 15, 35, 36, 37 |
| 11 應力/壓力 (Stress or pressure) | 6, 35, 36, 37 |
| 12 形狀 (Shape) | 14, 4, 15, 22 |
| 13 物體結構的穩定性 (Stability of composition) | 29, 30, 4, 34 |
| 14 強度 (Strength) | 1, 40, 35 |
| 17 溫度 (Temperature) | 34, 39, 40, 18 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 2, 18, 37 |
| 22 能量損失 (Loss of energy) | 7, 2, 35 |
| 26 物質的量 (Quantity of substance) | 15, 29, 28, 37 |
| 31 物體產生的有害副作用 (Harmful side effects) | 35, 34, 38 |
| 35 適應性/多功能性 (Adaptability) | 34, 39, 10, 18 |
| 36 裝置複雜度 (Device complexity) | 1, 4, 29 |

## 參數 8: 靜止物體的體積 (Volume of stationary object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 2, 26, 29, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 35, 10, 19, 14 |
| 3 移動物體的長度 (Length of moving object) | 35, 8, 2, 14 |
| 6 靜止物體的面積 (Area of stationary object) | 30, 2, 14, 18 |
| 7 移動物體的體積 (Volume of moving object) | 35, 10, 19, 14 |
| 9 速度 (Speed) | 2, 18, 37 |
| 10 力 (Force) | 13, 29, 10, 18 |
| 11 應力/壓力 (Stress or pressure) | 35, 24, 18, 30 |
| 12 形狀 (Shape) | 35, 10, 19, 14 |
| 14 強度 (Strength) | 30, 26, 35, 2 |
| 17 溫度 (Temperature) | 35, 39, 38 |
| 26 物質的量 (Quantity of substance) | 35, 10, 6 |
| 31 物體產生的有害副作用 (Harmful side effects) | 2, 18, 37 |
| 36 裝置複雜度 (Device complexity) | 35, 10, 6 |

## 參數 9: 速度 (Speed)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 2, 28, 13, 38 |
| 2 靜止物體的重量 (Weight of stationary object) | 13, 14, 8 |
| 3 移動物體的長度 (Length of moving object) | 29, 30, 34 |
| 4 靜止物體的長度 (Length of stationary object) | 7, 29, 34 |
| 5 移動物體的面積 (Area of moving object) | 13, 28, 15, 19 |
| 7 移動物體的體積 (Volume of moving object) | 29, 4, 38, 34 |
| 10 力 (Force) | 13, 28, 15, 12 |
| 11 應力/壓力 (Stress or pressure) | 6, 18, 38, 40 |
| 12 形狀 (Shape) | 35, 15, 18, 34 |
| 13 物體結構的穩定性 (Stability of composition) | 28, 33, 1, 18 |
| 14 強度 (Strength) | 8, 3, 26, 14 |
| 15 移動物體的耐久性 (Durability of moving object) | 19, 35, 38, 2 |
| 17 溫度 (Temperature) | 28, 30, 36, 2 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 13, 28, 15, 12 |
| 21 功率 (Power) | 35, 38 |
| 22 能量損失 (Loss of energy) | 28, 10, 29, 35 |
| 23 物質損失 (Loss of substance) | 10, 13, 28, 38 |
| 25 時間浪費 (Loss of time) | 10, 28, 32, 25 |
| 26 物質的量 (Quantity of substance) | 10, 28, 4, 34 |
| 27 可靠性 (Reliability) | 21, 35, 11, 28 |
| 28 量測精度 (Measurement accuracy) | 28, 32, 1, 24 |
| 30 物體受到的有害因素 (Harmful factors acting on object) | 13, 26, 2 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 35, 32 |
| 33 可操作性 (Ease of operation) | 32, 28, 13, 12 |
| 34 可修復性 (Ease of repair) | 25, 34, 6, 35 |
| 35 適應性/多功能性 (Adaptability) | 15, 10, 26 |
| 36 裝置複雜度 (Device complexity) | 13, 35, 1 |
| 37 控制複雜度 (Difficulty of detecting) | 34, 28, 35, 40 |
| 38 自動化程度 (Extent of automation) | 28, 26, 18, 35 |
| 39 生產力/效率 (Productivity) | 10, 34, 28, 32 |

## 參數 10: 力 (Force)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 8, 1, 37, 18 |
| 2 靜止物體的重量 (Weight of stationary object) | 18, 13, 1, 28 |
| 3 移動物體的長度 (Length of moving object) | 17, 19, 9, 36 |
| 5 移動物體的面積 (Area of moving object) | 19, 10, 15 |
| 6 靜止物體的面積 (Area of stationary object) | 1, 18, 36, 37 |
| 7 移動物體的體積 (Volume of moving object) | 15, 9, 12, 37 |
| 9 速度 (Speed) | 13, 28, 15, 12 |
| 11 應力/壓力 (Stress or pressure) | 18, 21, 11 |
| 12 形狀 (Shape) | 10, 35, 40, 34 |
| 13 物體結構的穩定性 (Stability of composition) | 35, 10, 21 |
| 14 強度 (Strength) | 35, 10, 14, 27 |
| 17 溫度 (Temperature) | 35, 10, 21 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 19, 17, 10 |
| 22 能量損失 (Loss of energy) | 7, 18, 23 |
| 23 物質損失 (Loss of substance) | 35, 10, 24 |
| 25 時間浪費 (Loss of time) | 10, 37, 36, 5 |
| 26 物質的量 (Quantity of substance) | 35, 21 |
| 27 可靠性 (Reliability) | 11, 3, 10, 32 |
| 28 量測精度 (Measurement accuracy) | 6, 19, 37, 18 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 2, 37 |
| 33 可操作性 (Ease of operation) | 1, 35, 11, 10 |
| 34 可修復性 (Ease of repair) | 15, 34, 33 |
| 36 裝置複雜度 (Device complexity) | 36, 35, 21 |
| 39 生產力/效率 (Productivity) | 35, 10, 21, 16 |

## 參數 11: 應力/壓力 (Stress or pressure)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 10, 36, 37, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 13, 29, 10, 18 |
| 3 移動物體的長度 (Length of moving object) | 35, 10, 36 |
| 6 靜止物體的面積 (Area of stationary object) | 35, 4, 15, 10 |
| 7 移動物體的體積 (Volume of moving object) | 6, 35, 10 |
| 9 速度 (Speed) | 6, 35, 36 |
| 10 力 (Force) | 36, 35, 21 |
| 12 形狀 (Shape) | 35, 4, 15, 10 |
| 13 物體結構的穩定性 (Stability of composition) | 35, 33, 2, 40 |
| 14 強度 (Strength) | 34, 15, 10, 14 |
| 17 溫度 (Temperature) | 35, 39, 19, 2 |
| 22 能量損失 (Loss of energy) | 36, 35, 21 |
| 26 物質的量 (Quantity of substance) | 10, 36, 3, 37 |
| 28 量測精度 (Measurement accuracy) | 6, 35, 36 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 2, 37 |
| 33 可操作性 (Ease of operation) | 1, 35, 16 |
| 35 適應性/多功能性 (Adaptability) | 15, 35, 22, 2 |
| 36 裝置複雜度 (Device complexity) | 10, 36, 3, 37 |
| 39 生產力/效率 (Productivity) | 35, 10, 25, 16 |

## 參數 12: 形狀 (Shape)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 10, 14, 35, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 35, 15, 34, 18 |
| 5 移動物體的面積 (Area of moving object) | 5, 34, 4, 10 |
| 7 移動物體的體積 (Volume of moving object) | 14, 4, 15, 22 |
| 9 速度 (Speed) | 35, 15, 18, 34 |
| 10 力 (Force) | 10, 15, 36, 28 |
| 11 應力/壓力 (Stress or pressure) | 35, 4, 15, 10 |
| 13 物體結構的穩定性 (Stability of composition) | 14, 4, 15, 22 |
| 14 強度 (Strength) | 9, 14, 15, 7 |
| 17 溫度 (Temperature) | 4, 6, 2 |
| 22 能量損失 (Loss of energy) | 14, 22, 19, 32 |
| 26 物質的量 (Quantity of substance) | 22, 14, 19, 32 |
| 31 物體產生的有害副作用 (Harmful side effects) | 1, 32, 17, 28 |
| 33 可操作性 (Ease of operation) | 15, 13, 39 |
| 35 適應性/多功能性 (Adaptability) | 1, 15, 29, 4 |
| 36 裝置複雜度 (Device complexity) | 1, 15, 29, 4 |
| 39 生產力/效率 (Productivity) | 35, 34, 15, 10 |

## 參數 13: 物體結構的穩定性 (Stability of composition)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 21, 35, 2, 39 |
| 2 靜止物體的重量 (Weight of stationary object) | 26, 39, 1, 40 |
| 3 移動物體的長度 (Length of moving object) | 13, 15, 1, 28 |
| 5 移動物體的面積 (Area of moving object) | 30, 26, 35, 2 |
| 7 移動物體的體積 (Volume of moving object) | 29, 26, 4, 1 |
| 9 速度 (Speed) | 28, 33, 1, 18 |
| 10 力 (Force) | 33, 15, 28, 18 |
| 11 應力/壓力 (Stress or pressure) | 35, 33, 2, 40 |
| 12 形狀 (Shape) | 14, 4, 15, 22 |
| 14 強度 (Strength) | 2, 11, 13 |
| 17 溫度 (Temperature) | 2, 35, 40 |
| 22 能量損失 (Loss of energy) | 23, 35, 40, 3 |
| 25 時間浪費 (Loss of time) | 24, 26, 28, 32 |
| 26 物質的量 (Quantity of substance) | 2, 13, 28 |
| 27 可靠性 (Reliability) | 11, 32, 1 |
| 28 量測精度 (Measurement accuracy) | 32, 35, 27, 31 |
| 31 物體產生的有害副作用 (Harmful side effects) | 27, 4, 29, 18 |
| 33 可操作性 (Ease of operation) | 32, 35, 13, 24 |
| 34 可修復性 (Ease of repair) | 2, 35, 34, 27 |
| 35 適應性/多功能性 (Adaptability) | 15, 32, 35 |
| 36 裝置複雜度 (Device complexity) | 13, 35, 1, 27 |
| 39 生產力/效率 (Productivity) | 35, 22, 39, 23 |

## 參數 14: 強度 (Strength)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 1, 8, 40, 15 |
| 2 靜止物體的重量 (Weight of stationary object) | 40, 26, 27, 1 |
| 3 移動物體的長度 (Length of moving object) | 1, 15, 8, 35 |
| 5 移動物體的面積 (Area of moving object) | 26, 35, 2 |
| 7 移動物體的體積 (Volume of moving object) | 1, 40, 35 |
| 9 速度 (Speed) | 3, 35, 13, 21 |
| 10 力 (Force) | 35, 10, 14, 27 |
| 11 應力/壓力 (Stress or pressure) | 34, 15, 10, 14 |
| 12 形狀 (Shape) | 9, 14, 17, 15 |
| 13 物體結構的穩定性 (Stability of composition) | 10, 26, 35, 28 |
| 17 溫度 (Temperature) | 2, 14, 17, 25 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 35, 28, 31, 40 |
| 22 能量損失 (Loss of energy) | 30, 10, 40 |
| 26 物質的量 (Quantity of substance) | 3, 35, 40, 14 |
| 27 可靠性 (Reliability) | 11, 28, 1, 34 |
| 28 量測精度 (Measurement accuracy) | 3, 27, 18, 40 |
| 30 物體受到的有害因素 (Harmful factors acting on object) | 22, 2, 37 |
| 31 物體產生的有害副作用 (Harmful side effects) | 17, 9, 15 |
| 33 可操作性 (Ease of operation) | 32, 40, 25, 2 |
| 34 可修復性 (Ease of repair) | 27, 11, 3 |
| 35 適應性/多功能性 (Adaptability) | 15, 3, 32 |
| 36 裝置複雜度 (Device complexity) | 29, 3, 28, 10 |
| 39 生產力/效率 (Productivity) | 35, 10, 23, 24 |

## 參數 15: 移動物體的耐久性 (Durability of moving object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 19, 5, 34, 31 |
| 2 靜止物體的重量 (Weight of stationary object) | 2, 19, 9 |
| 3 移動物體的長度 (Length of moving object) | 3, 17, 19 |
| 5 移動物體的面積 (Area of moving object) | 3, 17, 19 |
| 7 移動物體的體積 (Volume of moving object) | 10, 2, 19, 30 |
| 9 速度 (Speed) | 19, 35, 38, 2 |
| 10 力 (Force) | 19, 2, 16 |
| 11 應力/壓力 (Stress or pressure) | 19, 3, 27 |
| 12 形狀 (Shape) | 14, 26, 28, 25 |
| 13 物體結構的穩定性 (Stability of composition) | 13, 3, 35 |
| 14 強度 (Strength) | 28, 27, 3, 18 |
| 17 溫度 (Temperature) | 19, 35, 39 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 2, 19, 6 |
| 22 能量損失 (Loss of energy) | 3, 35, 5 |
| 25 時間浪費 (Loss of time) | 34, 27, 6, 40 |
| 26 物質的量 (Quantity of substance) | 10, 28, 24, 35 |
| 27 可靠性 (Reliability) | 11, 28, 3 |
| 31 物體產生的有害副作用 (Harmful side effects) | 3, 35, 10, 40 |
| 33 可操作性 (Ease of operation) | 32, 35, 30 |
| 34 可修復性 (Ease of repair) | 27, 1, 4 |
| 35 適應性/多功能性 (Adaptability) | 15, 29, 37, 28 |
| 36 裝置複雜度 (Device complexity) | 19, 29, 39, 35 |
| 39 生產力/效率 (Productivity) | 35, 17, 14, 19 |

## 參數 16: 靜止物體的耐久性 (Durability of stationary object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 19, 18, 36, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 6, 27, 19, 16 |
| 6 靜止物體的面積 (Area of stationary object) | 39, 3, 35, 23 |
| 9 速度 (Speed) | 19, 35, 39 |
| 10 力 (Force) | 14, 26, 28, 25 |
| 13 物體結構的穩定性 (Stability of composition) | 13, 35, 1 |
| 14 強度 (Strength) | 2, 27, 35, 11 |
| 17 溫度 (Temperature) | 19, 35, 39 |
| 22 能量損失 (Loss of energy) | 3, 35, 39, 23 |
| 25 時間浪費 (Loss of time) | 34, 27, 6, 40 |
| 26 物質的量 (Quantity of substance) | 10, 26, 24 |
| 27 可靠性 (Reliability) | 11, 1, 2, 9 |
| 31 物體產生的有害副作用 (Harmful side effects) | 3, 35, 10, 40 |
| 33 可操作性 (Ease of operation) | 39, 3, 35, 23 |
| 34 可修復性 (Ease of repair) | 27, 40, 28, 8 |
| 35 適應性/多功能性 (Adaptability) | 15, 29, 37, 28 |
| 36 裝置複雜度 (Device complexity) | 29, 1, 4, 16 |
| 39 生產力/效率 (Productivity) | 35, 17, 14, 19 |

## 參數 17: 溫度 (Temperature)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 36, 22, 6, 38 |
| 2 靜止物體的重量 (Weight of stationary object) | 22, 35, 32 |
| 3 移動物體的長度 (Length of moving object) | 15, 19, 9 |
| 7 移動物體的體積 (Volume of moving object) | 34, 39, 40, 18 |
| 9 速度 (Speed) | 28, 30, 36, 2 |
| 10 力 (Force) | 35, 10, 3, 21 |
| 11 應力/壓力 (Stress or pressure) | 35, 39, 19, 2 |
| 12 形狀 (Shape) | 4, 6, 2 |
| 13 物體結構的穩定性 (Stability of composition) | 21, 36, 29, 31 |
| 14 強度 (Strength) | 21, 17, 35, 38 |
| 15 移動物體的耐久性 (Durability of moving object) | 19, 35, 3, 17 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 32, 30, 21, 16 |
| 22 能量損失 (Loss of energy) | 22, 19, 29, 40 |
| 26 物質的量 (Quantity of substance) | 21, 36, 39, 31 |
| 27 可靠性 (Reliability) | 21, 11, 27, 19 |
| 31 物體產生的有害副作用 (Harmful side effects) | 19, 13, 39 |
| 33 可操作性 (Ease of operation) | 22, 33, 35, 2 |
| 35 適應性/多功能性 (Adaptability) | 35, 33, 31, 38 |
| 36 裝置複雜度 (Device complexity) | 2, 18, 27, 19 |
| 39 生產力/效率 (Productivity) | 35, 28, 21, 18 |

## 參數 18: 照度/亮度 (Illumination intensity)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 19, 1, 32 |
| 9 速度 (Speed) | 32, 35, 19 |
| 10 力 (Force) | 19, 32, 26 |
| 17 溫度 (Temperature) | 32, 35, 1, 15 |
| 22 能量損失 (Loss of energy) | 32, 1, 19 |
| 26 物質的量 (Quantity of substance) | 1, 19, 32, 13 |
| 31 物體產生的有害副作用 (Harmful side effects) | 19, 1, 31 |
| 33 可操作性 (Ease of operation) | 1, 13, 32, 15 |
| 35 適應性/多功能性 (Adaptability) | 15, 1, 19 |
| 36 裝置複雜度 (Device complexity) | 19, 1, 29 |
| 39 生產力/效率 (Productivity) | 32, 15, 26, 1 |

## 參數 19: 移動物體消耗的能量 (Energy use by moving object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 12, 18, 28, 31 |
| 2 靜止物體的重量 (Weight of stationary object) | 15, 19, 25 |
| 3 移動物體的長度 (Length of moving object) | 12, 28 |
| 5 移動物體的面積 (Area of moving object) | 19, 10, 32, 18 |
| 7 移動物體的體積 (Volume of moving object) | 2, 35, 18 |
| 9 速度 (Speed) | 8, 35, 24 |
| 10 力 (Force) | 19, 24, 3, 14 |
| 11 應力/壓力 (Stress or pressure) | 12, 36, 18, 31 |
| 12 形狀 (Shape) | 15, 19, 25 |
| 14 強度 (Strength) | 35, 28, 31, 40 |
| 15 移動物體的耐久性 (Durability of moving object) | 19, 6, 27 |
| 17 溫度 (Temperature) | 32, 30, 21, 16 |
| 22 能量損失 (Loss of energy) | 12, 28, 35 |
| 23 物質損失 (Loss of substance) | 35, 18, 24, 5 |
| 25 時間浪費 (Loss of time) | 28, 27, 18, 38 |
| 26 物質的量 (Quantity of substance) | 5, 35, 18, 31 |
| 27 可靠性 (Reliability) | 3, 35, 31 |
| 28 量測精度 (Measurement accuracy) | 6, 19, 28, 24 |
| 31 物體產生的有害副作用 (Harmful side effects) | 12, 22, 15, 24 |
| 33 可操作性 (Ease of operation) | 6, 19, 37, 18 |
| 35 適應性/多功能性 (Adaptability) | 15, 19, 25 |
| 36 裝置複雜度 (Device complexity) | 35, 38, 19, 18 |
| 39 生產力/效率 (Productivity) | 28, 27, 18, 31 |

## 參數 20: 靜止物體消耗的能量 (Energy use by stationary object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 19, 9, 6, 27 |
| 2 靜止物體的重量 (Weight of stationary object) | 36, 37, 19, 26 |
| 5 移動物體的面積 (Area of moving object) | 19, 10, 32, 18 |
| 7 移動物體的體積 (Volume of moving object) | 35, 6, 18, 31 |
| 9 速度 (Speed) | 19, 35, 38, 2 |
| 10 力 (Force) | 1, 35, 6, 36 |
| 11 應力/壓力 (Stress or pressure) | 19, 2, 35, 32 |
| 13 物體結構的穩定性 (Stability of composition) | 5, 28, 11, 29 |
| 14 強度 (Strength) | 35, 28, 31, 40 |
| 17 溫度 (Temperature) | 32, 35, 19, 2 |
| 22 能量損失 (Loss of energy) | 7, 23, 35 |
| 25 時間浪費 (Loss of time) | 28, 35, 18, 27 |
| 26 物質的量 (Quantity of substance) | 5, 35, 18, 31 |
| 27 可靠性 (Reliability) | 10, 35, 17, 7 |
| 31 物體產生的有害副作用 (Harmful side effects) | 12, 22, 15, 24 |
| 33 可操作性 (Ease of operation) | 15, 35, 2 |
| 35 適應性/多功能性 (Adaptability) | 35, 18, 34, 4 |
| 36 裝置複雜度 (Device complexity) | 26, 10, 18, 32 |

## 參數 21: 功率 (Power)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 8, 36, 38, 31 |
| 2 靜止物體的重量 (Weight of stationary object) | 19, 26, 17, 27 |
| 3 移動物體的長度 (Length of moving object) | 1, 10, 35, 37 |
| 5 移動物體的面積 (Area of moving object) | 19, 38, 7 |
| 7 移動物體的體積 (Volume of moving object) | 35, 6, 38 |
| 9 速度 (Speed) | 1, 28, 35, 23 |
| 10 力 (Force) | 19, 35, 18, 37 |
| 11 應力/壓力 (Stress or pressure) | 2, 36, 18, 37 |
| 12 形狀 (Shape) | 19, 26, 17, 27 |
| 14 強度 (Strength) | 1, 35, 6, 27 |
| 17 溫度 (Temperature) | 2, 14, 17, 25 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 35, 20, 10, 6 |
| 22 能量損失 (Loss of energy) | 7, 2, 6, 13 |
| 25 時間浪費 (Loss of time) | 28, 10, 29, 35 |
| 26 物質的量 (Quantity of substance) | 35, 2, 10, 34 |
| 27 可靠性 (Reliability) | 11, 2, 13, 39 |
| 28 量測精度 (Measurement accuracy) | 6, 19, 37, 18 |
| 31 物體產生的有害副作用 (Harmful side effects) | 19, 22, 31, 2 |
| 33 可操作性 (Ease of operation) | 32, 2 |
| 35 適應性/多功能性 (Adaptability) | 26, 35, 10, 18 |
| 36 裝置複雜度 (Device complexity) | 19, 10, 35, 38 |
| 39 生產力/效率 (Productivity) | 20, 10, 28, 18 |

## 參數 22: 能量損失 (Loss of energy)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 15, 6, 19, 28 |
| 2 靜止物體的重量 (Weight of stationary object) | 19, 6, 18, 9 |
| 3 移動物體的長度 (Length of moving object) | 7, 2, 6, 13 |
| 5 移動物體的面積 (Area of moving object) | 6, 38, 7 |
| 7 移動物體的體積 (Volume of moving object) | 7, 2, 35 |
| 9 速度 (Speed) | 28, 10, 29, 35 |
| 10 力 (Force) | 3, 38, 35, 27 |
| 11 應力/壓力 (Stress or pressure) | 36, 35, 21 |
| 12 形狀 (Shape) | 14, 2, 39, 6 |
| 13 物體結構的穩定性 (Stability of composition) | 23, 14, 25 |
| 14 強度 (Strength) | 12, 2, 29 |
| 15 移動物體的耐久性 (Durability of moving object) | 3, 35, 31 |
| 17 溫度 (Temperature) | 22, 19, 29, 40 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 21, 22, 35, 2 |
| 22 能量損失 (Loss of energy) | 3, 27, 35, 16 |
| 25 時間浪費 (Loss of time) | 3, 35, 31 |
| 26 物質的量 (Quantity of substance) | 3, 35, 31 |
| 27 可靠性 (Reliability) | 3, 10, 27, 40 |
| 28 量測精度 (Measurement accuracy) | 3, 27, 35, 31 |
| 31 物體產生的有害副作用 (Harmful side effects) | 19, 24, 3, 14 |
| 33 可操作性 (Ease of operation) | 32, 2 |
| 35 適應性/多功能性 (Adaptability) | 32, 2, 13 |
| 36 裝置複雜度 (Device complexity) | 14, 2, 39, 6 |
| 39 生產力/效率 (Productivity) | 28, 10, 35, 23 |

## 參數 23: 物質損失 (Loss of substance)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 35, 6, 23, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 35, 6, 22, 32 |
| 3 移動物體的長度 (Length of moving object) | 14, 29, 10, 39 |
| 5 移動物體的面積 (Area of moving object) | 10, 29, 39, 35 |
| 7 移動物體的體積 (Volume of moving object) | 29, 35, 3, 5 |
| 9 速度 (Speed) | 10, 13, 28, 38 |
| 10 力 (Force) | 14, 15, 18, 40 |
| 11 應力/壓力 (Stress or pressure) | 3, 36, 37, 10 |
| 13 物體結構的穩定性 (Stability of composition) | 2, 14, 30, 40 |
| 14 強度 (Strength) | 35, 10, 28, 24 |
| 15 移動物體的耐久性 (Durability of moving object) | 10, 18, 39, 31 |
| 17 溫度 (Temperature) | 27, 16, 18, 38 |
| 22 能量損失 (Loss of energy) | 21, 36, 39, 31 |
| 25 時間浪費 (Loss of time) | 10, 36, 14, 3 |
| 26 物質的量 (Quantity of substance) | 15, 34, 33, 30 |
| 27 可靠性 (Reliability) | 34, 39, 19, 27 |
| 28 量測精度 (Measurement accuracy) | 33, 22, 30, 40 |
| 31 物體產生的有害副作用 (Harmful side effects) | 10, 1, 34, 29 |
| 33 可操作性 (Ease of operation) | 22, 35, 13, 24 |
| 35 適應性/多功能性 (Adaptability) | 35, 22, 1, 39 |
| 36 裝置複雜度 (Device complexity) | 33, 22, 30, 40 |
| 39 生產力/效率 (Productivity) | 35, 28, 34, 4 |

## 參數 24: 資訊損失 (Loss of information)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 10, 24, 35 |
| 9 速度 (Speed) | 24, 26, 28, 32 |
| 10 力 (Force) | 10, 35, 5 |
| 22 能量損失 (Loss of energy) | 19, 10, 32, 18 |
| 26 物質的量 (Quantity of substance) | 1, 26, 17 |
| 27 可靠性 (Reliability) | 27, 26, 1 |
| 28 量測精度 (Measurement accuracy) | 6, 19, 28, 24 |
| 31 物體產生的有害副作用 (Harmful side effects) | 10, 19 |
| 33 可操作性 (Ease of operation) | 27, 22, 26, 1 |
| 35 適應性/多功能性 (Adaptability) | 13, 35, 1 |
| 36 裝置複雜度 (Device complexity) | 35, 28, 6, 37 |
| 39 生產力/效率 (Productivity) | 10, 28, 23 |

## 參數 25: 時間浪費 (Loss of time)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 10, 20, 37, 35 |
| 2 靜止物體的重量 (Weight of stationary object) | 10, 20, 26, 5 |
| 3 移動物體的長度 (Length of moving object) | 15, 2, 29 |
| 5 移動物體的面積 (Area of moving object) | 30, 26, 34 |
| 7 移動物體的體積 (Volume of moving object) | 10, 26, 34, 2 |
| 9 速度 (Speed) | 10, 28, 32, 25 |
| 10 力 (Force) | 35, 29, 34, 28 |
| 11 應力/壓力 (Stress or pressure) | 35, 10, 2, 18 |
| 12 形狀 (Shape) | 20, 10, 28, 18 |
| 13 物體結構的穩定性 (Stability of composition) | 24, 26, 28, 18 |
| 14 強度 (Strength) | 35, 10, 18, 5 |
| 15 移動物體的耐久性 (Durability of moving object) | 34, 27, 6, 40 |
| 17 溫度 (Temperature) | 2, 5, 34, 10 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 28, 27, 18, 38 |
| 22 能量損失 (Loss of energy) | 35, 29, 21, 18 |
| 25 時間浪費 (Loss of time) | 4, 10, 34, 17 |
| 26 物質的量 (Quantity of substance) | 35, 18, 10, 39 |
| 27 可靠性 (Reliability) | 10, 30, 4 |
| 28 量測精度 (Measurement accuracy) | 24, 34, 28, 32 |
| 30 物體受到的有害因素 (Harmful factors acting on object) | 35, 18, 34, 4 |
| 31 物體產生的有害副作用 (Harmful side effects) | 35, 22, 18, 39 |
| 33 可操作性 (Ease of operation) | 4, 10, 34, 17 |
| 35 適應性/多功能性 (Adaptability) | 10, 26, 34, 2 |
| 36 裝置複雜度 (Device complexity) | 35, 29, 34, 28 |
| 39 生產力/效率 (Productivity) | 35, 28, 34, 4 |

## 參數 26: 物質的量 (Quantity of substance)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 35, 6, 18, 31 |
| 2 靜止物體的重量 (Weight of stationary object) | 27, 26, 18, 35 |
| 3 移動物體的長度 (Length of moving object) | 29, 14, 35, 18 |
| 5 移動物體的面積 (Area of moving object) | 15, 14, 29 |
| 7 移動物體的體積 (Volume of moving object) | 15, 20, 29 |
| 9 速度 (Speed) | 2, 18, 40, 4 |
| 10 力 (Force) | 35, 29, 34, 18 |
| 11 應力/壓力 (Stress or pressure) | 10, 36, 14, 3 |
| 12 形狀 (Shape) | 29, 22, 35, 1 |
| 13 物體結構的穩定性 (Stability of composition) | 3, 13, 27, 10 |
| 14 強度 (Strength) | 3, 35, 40, 14 |
| 15 移動物體的耐久性 (Durability of moving object) | 3, 35, 31 |
| 17 溫度 (Temperature) | 21, 36, 29, 31 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 2, 22, 17, 19 |
| 22 能量損失 (Loss of energy) | 3, 35, 31 |
| 24 資訊損失 (Loss of information) | 15, 34, 33 |
| 25 時間浪費 (Loss of time) | 35, 10, 18, 39 |
| 27 可靠性 (Reliability) | 34, 29, 16, 18 |
| 28 量測精度 (Measurement accuracy) | 33, 30, 35, 40 |
| 30 物體受到的有害因素 (Harmful factors acting on object) | 35, 33, 29, 31 |
| 31 物體產生的有害副作用 (Harmful side effects) | 33, 22, 30, 40 |
| 33 可操作性 (Ease of operation) | 27, 22, 26, 1 |
| 34 可修復性 (Ease of repair) | 34, 19, 16, 18 |
| 35 適應性/多功能性 (Adaptability) | 6, 3, 10, 24 |
| 36 裝置複雜度 (Device complexity) | 29, 1, 35, 27 |
| 39 生產力/效率 (Productivity) | 35, 28, 34, 4 |

## 參數 27: 可靠性 (Reliability)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 3, 8, 10, 40 |
| 2 靜止物體的重量 (Weight of stationary object) | 3, 10, 8, 28 |
| 3 移動物體的長度 (Length of moving object) | 15, 9, 14, 4 |
| 5 移動物體的面積 (Area of moving object) | 11, 32, 13 |
| 7 移動物體的體積 (Volume of moving object) | 21, 35, 11, 28 |
| 9 速度 (Speed) | 21, 35, 11, 28 |
| 10 力 (Force) | 8, 28, 10, 3 |
| 11 應力/壓力 (Stress or pressure) | 10, 24, 35, 19 |
| 12 形狀 (Shape) | 11, 35, 27, 28 |
| 13 物體結構的穩定性 (Stability of composition) | 2, 35, 3, 25 |
| 14 強度 (Strength) | 3, 10, 8, 28 |
| 15 移動物體的耐久性 (Durability of moving object) | 11, 32, 1 |
| 17 溫度 (Temperature) | 21, 11, 27, 19 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 32, 3, 27, 16 |
| 22 能量損失 (Loss of energy) | 21, 11, 27, 19 |
| 25 時間浪費 (Loss of time) | 10, 11, 35 |
| 26 物質的量 (Quantity of substance) | 34, 27, 6, 40 |
| 28 量測精度 (Measurement accuracy) | 11, 32, 1 |
| 31 物體產生的有害副作用 (Harmful side effects) | 27, 40, 28, 8 |
| 33 可操作性 (Ease of operation) | 13, 35, 1 |
| 34 可修復性 (Ease of repair) | 1, 11, 2, 13 |
| 35 適應性/多功能性 (Adaptability) | 27, 40, 28, 8 |
| 36 裝置複雜度 (Device complexity) | 13, 35, 1, 27 |
| 39 生產力/效率 (Productivity) | 1, 35, 11, 10 |

## 參數 28: 量測精度 (Measurement accuracy)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 32, 35, 26, 28 |
| 2 靜止物體的重量 (Weight of stationary object) | 28, 35, 25, 26 |
| 3 移動物體的長度 (Length of moving object) | 28, 26, 5, 16 |
| 5 移動物體的面積 (Area of moving object) | 26, 28, 5, 16 |
| 7 移動物體的體積 (Volume of moving object) | 32, 35, 13 |
| 9 速度 (Speed) | 28, 32, 1, 24 |
| 10 力 (Force) | 34, 26, 28, 32 |
| 11 應力/壓力 (Stress or pressure) | 26, 35, 28, 32 |
| 12 形狀 (Shape) | 26, 32, 27 |
| 13 物體結構的穩定性 (Stability of composition) | 6, 28, 32 |
| 14 強度 (Strength) | 28, 6, 32 |
| 17 溫度 (Temperature) | 27, 35, 2, 40 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 26, 32, 27 |
| 22 能量損失 (Loss of energy) | 6, 28, 32 |
| 24 資訊損失 (Loss of information) | 26, 32, 27 |
| 25 時間浪費 (Loss of time) | 24, 34, 28, 32 |
| 27 可靠性 (Reliability) | 3, 33, 39, 10 |
| 31 物體產生的有害副作用 (Harmful side effects) | 26, 28, 32, 3 |
| 33 可操作性 (Ease of operation) | 28, 32, 1, 24 |
| 35 適應性/多功能性 (Adaptability) | 5, 11, 1, 23 |
| 36 裝置複雜度 (Device complexity) | 28, 6, 32 |
| 39 生產力/效率 (Productivity) | 26, 32, 27, 35 |

## 參數 29: 製造精度 (Manufacturing precision)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 32, 28, 13, 18 |
| 2 靜止物體的重量 (Weight of stationary object) | 35, 25, 18, 10 |
| 3 移動物體的長度 (Length of moving object) | 35, 1, 26, 24 |
| 5 移動物體的面積 (Area of moving object) | 30, 18, 35, 4 |
| 7 移動物體的體積 (Volume of moving object) | 32, 28, 2, 24 |
| 9 速度 (Speed) | 30, 28, 40, 19 |
| 10 力 (Force) | 14, 35, 10, 28 |
| 11 應力/壓力 (Stress or pressure) | 2, 18, 40, 4 |
| 12 形狀 (Shape) | 35, 10, 28, 29 |
| 13 物體結構的穩定性 (Stability of composition) | 32, 2, 29, 18 |
| 14 強度 (Strength) | 35, 10, 28, 24 |
| 17 溫度 (Temperature) | 35, 19, 32, 39 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 30, 18, 35, 4 |
| 22 能量損失 (Loss of energy) | 28, 18, 35, 26 |
| 25 時間浪費 (Loss of time) | 26, 2, 18, 32 |
| 26 物質的量 (Quantity of substance) | 18, 32, 39, 22 |
| 27 可靠性 (Reliability) | 25, 10, 35, 18 |
| 28 量測精度 (Measurement accuracy) | 30, 16, 18, 10 |
| 31 物體產生的有害副作用 (Harmful side effects) | 32, 2, 29, 18 |
| 33 可操作性 (Ease of operation) | 30, 18, 35, 4 |
| 34 可修復性 (Ease of repair) | 18, 29, 28, 32 |
| 35 適應性/多功能性 (Adaptability) | 10, 32, 35, 26 |
| 36 裝置複雜度 (Device complexity) | 35, 10, 28, 29 |
| 39 生產力/效率 (Productivity) | 30, 18, 29, 28 |

## 參數 30: 物體受到的有害因素 (Harmful factors acting on object)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 22, 21, 27, 39 |
| 2 靜止物體的重量 (Weight of stationary object) | 22, 35, 13, 24 |
| 3 移動物體的長度 (Length of moving object) | 1, 17, 24, 39 |
| 5 移動物體的面積 (Area of moving object) | 22, 1, 33, 28 |
| 7 移動物體的體積 (Volume of moving object) | 33, 22, 19, 40 |
| 9 速度 (Speed) | 22, 35, 2, 24 |
| 10 力 (Force) | 2, 19, 22, 37 |
| 11 應力/壓力 (Stress or pressure) | 35, 22, 1, 39 |
| 12 形狀 (Shape) | 17, 1, 39, 4 |
| 13 物體結構的穩定性 (Stability of composition) | 1, 18, 36, 37 |
| 14 強度 (Strength) | 22, 1, 33, 28 |
| 17 溫度 (Temperature) | 24, 35, 2 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 2, 35, 22, 26 |
| 22 能量損失 (Loss of energy) | 19, 22, 31, 2 |
| 25 時間浪費 (Loss of time) | 35, 28, 34, 4 |
| 26 物質的量 (Quantity of substance) | 10, 18, 39, 31 |
| 27 可靠性 (Reliability) | 21, 22, 35, 2 |
| 28 量測精度 (Measurement accuracy) | 22, 19, 29, 40 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 35, 18, 39 |
| 33 可操作性 (Ease of operation) | 22, 35, 13, 24 |
| 34 可修復性 (Ease of repair) | 22, 2, 37 |
| 35 適應性/多功能性 (Adaptability) | 35, 22, 1, 39 |
| 36 裝置複雜度 (Device complexity) | 22, 35, 18, 39 |
| 39 生產力/效率 (Productivity) | 35, 22, 18, 39 |

## 參數 31: 物體產生的有害副作用 (Harmful side effects)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 22, 35, 31, 39 |
| 2 靜止物體的重量 (Weight of stationary object) | 19, 22, 15, 39 |
| 3 移動物體的長度 (Length of moving object) | 1, 19, 32, 13 |
| 5 移動物體的面積 (Area of moving object) | 22, 33, 28, 1 |
| 7 移動物體的體積 (Volume of moving object) | 21, 22, 35, 2 |
| 9 速度 (Speed) | 22, 35, 2, 24 |
| 10 力 (Force) | 19, 22, 31, 2 |
| 11 應力/壓力 (Stress or pressure) | 22, 2, 37 |
| 12 形狀 (Shape) | 17, 2, 18, 39 |
| 13 物體結構的穩定性 (Stability of composition) | 19, 24, 39, 32 |
| 14 強度 (Strength) | 19, 35, 39, 2 |
| 15 移動物體的耐久性 (Durability of moving object) | 3, 35, 10, 40 |
| 17 溫度 (Temperature) | 1, 19, 32, 13 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 2, 35, 22, 26 |
| 22 能量損失 (Loss of energy) | 19, 24, 3, 14 |
| 25 時間浪費 (Loss of time) | 35, 22, 18, 39 |
| 26 物質的量 (Quantity of substance) | 33, 22, 30, 40 |
| 27 可靠性 (Reliability) | 22, 35, 13, 24 |
| 28 量測精度 (Measurement accuracy) | 26, 28, 32, 3 |
| 31 物體產生的有害副作用 (Harmful side effects) | 1, 22, 35, 39 |
| 33 可操作性 (Ease of operation) | 22, 35, 13, 24 |
| 34 可修復性 (Ease of repair) | 17, 1, 39, 4 |
| 35 適應性/多功能性 (Adaptability) | 22, 1, 33, 28 |
| 36 裝置複雜度 (Device complexity) | 22, 35, 18, 39 |
| 39 生產力/效率 (Productivity) | 35, 22, 18, 39 |

## 參數 32: 可製造性 (Ease of manufacture)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 28, 29, 15, 16 |
| 2 靜止物體的重量 (Weight of stationary object) | 28, 29, 35, 27 |
| 3 移動物體的長度 (Length of moving object) | 1, 35, 12, 18 |
| 5 移動物體的面積 (Area of moving object) | 15, 34, 33 |
| 7 移動物體的體積 (Volume of moving object) | 35, 13, 8, 1 |
| 9 速度 (Speed) | 35, 12, 34, 31 |
| 10 力 (Force) | 35, 19, 1, 37 |
| 11 應力/壓力 (Stress or pressure) | 1, 28, 35, 23 |
| 12 形狀 (Shape) | 1, 32, 17, 28 |
| 13 物體結構的穩定性 (Stability of composition) | 11, 13, 1 |
| 14 強度 (Strength) | 1, 3, 10, 32 |
| 15 移動物體的耐久性 (Durability of moving object) | 35, 12, 34, 31 |
| 17 溫度 (Temperature) | 35, 19, 1, 37 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 1, 28, 13, 27 |
| 22 能量損失 (Loss of energy) | 11, 13, 1 |
| 25 時間浪費 (Loss of time) | 1, 35, 12, 18 |
| 26 物質的量 (Quantity of substance) | 35, 1, 26, 24 |
| 27 可靠性 (Reliability) | 11, 13, 1 |
| 28 量測精度 (Measurement accuracy) | 28, 26, 5, 16 |
| 31 物體產生的有害副作用 (Harmful side effects) | 1, 28, 35, 23 |
| 33 可操作性 (Ease of operation) | 2, 5, 13, 16 |
| 34 可修復性 (Ease of repair) | 27, 26, 1 |
| 35 適應性/多功能性 (Adaptability) | 35, 1, 11, 9 |
| 36 裝置複雜度 (Device complexity) | 1, 28, 10, 25 |
| 39 生產力/效率 (Productivity) | 35, 28, 34, 4 |

## 參數 33: 可操作性 (Ease of operation)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 25, 2, 13, 15 |
| 2 靜止物體的重量 (Weight of stationary object) | 6, 13, 1, 25 |
| 3 移動物體的長度 (Length of moving object) | 1, 17, 13, 12 |
| 5 移動物體的面積 (Area of moving object) | 4, 18, 39, 31 |
| 7 移動物體的體積 (Volume of moving object) | 29, 1, 4 |
| 9 速度 (Speed) | 15, 34, 33 |
| 10 力 (Force) | 32, 35, 30 |
| 11 應力/壓力 (Stress or pressure) | 32, 40, 3, 28 |
| 12 形狀 (Shape) | 15, 34, 33, 30 |
| 13 物體結構的穩定性 (Stability of composition) | 32, 35, 30 |
| 14 強度 (Strength) | 32, 40, 3, 28 |
| 15 移動物體的耐久性 (Durability of moving object) | 2, 32, 12 |
| 17 溫度 (Temperature) | 22, 33, 35, 2 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 27, 2, 39, 35 |
| 22 能量損失 (Loss of energy) | 25, 28, 17, 15 |
| 25 時間浪費 (Loss of time) | 4, 10, 34, 17 |
| 26 物質的量 (Quantity of substance) | 13, 1, 26, 24 |
| 27 可靠性 (Reliability) | 2, 32, 12 |
| 28 量測精度 (Measurement accuracy) | 32, 35, 30 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 35, 13, 24 |
| 34 可修復性 (Ease of repair) | 1, 2, 35, 30 |
| 35 適應性/多功能性 (Adaptability) | 15, 34, 1, 16 |
| 36 裝置複雜度 (Device complexity) | 32, 26, 12, 17 |
| 39 生產力/效率 (Productivity) | 35, 28, 34, 4 |

## 參數 34: 可修復性 (Ease of repair)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 2, 27, 35, 11 |
| 2 靜止物體的重量 (Weight of stationary object) | 2, 27, 35, 11 |
| 3 移動物體的長度 (Length of moving object) | 1, 28, 10, 34 |
| 5 移動物體的面積 (Area of moving object) | 15, 10, 32, 2 |
| 7 移動物體的體積 (Volume of moving object) | 34, 27, 6, 40 |
| 9 速度 (Speed) | 25, 34, 6, 35 |
| 10 力 (Force) | 1, 12, 26, 15 |
| 11 應力/壓力 (Stress or pressure) | 15, 34, 32, 1 |
| 12 形狀 (Shape) | 16, 25, 1, 15 |
| 13 物體結構的穩定性 (Stability of composition) | 34, 27, 6, 40 |
| 14 強度 (Strength) | 11, 1, 2, 9 |
| 15 移動物體的耐久性 (Durability of moving object) | 1, 13, 2, 4 |
| 17 溫度 (Temperature) | 4, 18, 39, 31 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 15, 1, 13, 16 |
| 22 能量損失 (Loss of energy) | 15, 34, 1, 16 |
| 25 時間浪費 (Loss of time) | 34, 10, 28, 32 |
| 26 物質的量 (Quantity of substance) | 34, 19, 16, 18 |
| 27 可靠性 (Reliability) | 1, 11, 2, 13 |
| 28 量測精度 (Measurement accuracy) | 13, 2, 35 |
| 31 物體產生的有害副作用 (Harmful side effects) | 2, 35, 34, 27 |
| 33 可操作性 (Ease of operation) | 1, 2, 35, 30 |
| 35 適應性/多功能性 (Adaptability) | 25, 34, 6, 35 |
| 36 裝置複雜度 (Device complexity) | 1, 34, 12, 3 |
| 39 生產力/效率 (Productivity) | 35, 1, 13, 11 |

## 參數 35: 適應性/多功能性 (Adaptability)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 15, 37, 1, 8 |
| 2 靜止物體的重量 (Weight of stationary object) | 35, 30, 14 |
| 3 移動物體的長度 (Length of moving object) | 15, 29, 37, 28 |
| 5 移動物體的面積 (Area of moving object) | 35, 10, 14, 27 |
| 7 移動物體的體積 (Volume of moving object) | 35, 3, 15, 39 |
| 9 速度 (Speed) | 15, 10, 26 |
| 10 力 (Force) | 35, 10, 14 |
| 11 應力/壓力 (Stress or pressure) | 35, 10, 14, 27 |
| 12 形狀 (Shape) | 35, 30, 14 |
| 13 物體結構的穩定性 (Stability of composition) | 15, 10, 2, 13 |
| 14 強度 (Strength) | 3, 35, 15 |
| 15 移動物體的耐久性 (Durability of moving object) | 15, 29, 37, 28 |
| 17 溫度 (Temperature) | 3, 35, 15, 39 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 35, 10, 14 |
| 22 能量損失 (Loss of energy) | 35, 10, 14, 27 |
| 25 時間浪費 (Loss of time) | 35, 10, 14 |
| 26 物質的量 (Quantity of substance) | 35, 30, 14, 3 |
| 27 可靠性 (Reliability) | 35, 3, 15, 39 |
| 28 量測精度 (Measurement accuracy) | 5, 12, 35, 26 |
| 31 物體產生的有害副作用 (Harmful side effects) | 22, 1, 33, 28 |
| 33 可操作性 (Ease of operation) | 15, 34, 1, 16 |
| 34 可修復性 (Ease of repair) | 35, 10, 25, 34 |
| 36 裝置複雜度 (Device complexity) | 35, 30, 34, 2 |
| 39 生產力/效率 (Productivity) | 35, 10, 28, 24 |

## 參數 36: 裝置複雜度 (Device complexity)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 26, 30, 34, 36 |
| 2 靜止物體的重量 (Weight of stationary object) | 19, 26, 1, 36 |
| 3 移動物體的長度 (Length of moving object) | 6, 36, 37, 1 |
| 5 移動物體的面積 (Area of moving object) | 29, 1, 4, 16 |
| 7 移動物體的體積 (Volume of moving object) | 34, 26, 6 |
| 9 速度 (Speed) | 34, 10, 28, 32 |
| 10 力 (Force) | 36, 35, 21 |
| 11 應力/壓力 (Stress or pressure) | 36, 35, 21 |
| 12 形狀 (Shape) | 1, 15, 29, 4 |
| 13 物體結構的穩定性 (Stability of composition) | 36, 35, 21, 28 |
| 14 強度 (Strength) | 26, 30, 34, 36 |
| 15 移動物體的耐久性 (Durability of moving object) | 19, 1, 35 |
| 17 溫度 (Temperature) | 2, 26, 35, 39 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 19, 1, 35, 38 |
| 22 能量損失 (Loss of energy) | 1, 6, 15, 8 |
| 25 時間浪費 (Loss of time) | 35, 29, 34, 28 |
| 26 物質的量 (Quantity of substance) | 29, 1, 35, 27 |
| 27 可靠性 (Reliability) | 15, 10, 37, 28 |
| 28 量測精度 (Measurement accuracy) | 15, 1, 24 |
| 31 物體產生的有害副作用 (Harmful side effects) | 12, 17, 28, 24 |
| 33 可操作性 (Ease of operation) | 2, 26, 35, 39 |
| 34 可修復性 (Ease of repair) | 34, 28, 35, 40 |
| 35 適應性/多功能性 (Adaptability) | 35, 30, 34, 2 |
| 39 生產力/效率 (Productivity) | 35, 34, 2, 10 |

## 參數 37: 控制複雜度 (Difficulty of detecting)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 27, 26, 28, 13 |
| 2 靜止物體的重量 (Weight of stationary object) | 6, 13, 28, 1 |
| 3 移動物體的長度 (Length of moving object) | 16, 34, 31, 28 |
| 5 移動物體的面積 (Area of moving object) | 26, 24, 32, 28 |
| 7 移動物體的體積 (Volume of moving object) | 27, 13, 1, 39 |
| 9 速度 (Speed) | 26, 24, 32, 28 |
| 10 力 (Force) | 26, 35, 28, 18 |
| 11 應力/壓力 (Stress or pressure) | 28, 32, 1, 24 |
| 12 形狀 (Shape) | 32, 26, 28, 18 |
| 13 物體結構的穩定性 (Stability of composition) | 27, 35, 2, 40 |
| 14 強度 (Strength) | 28, 6, 32 |
| 15 移動物體的耐久性 (Durability of moving object) | 34, 31, 28, 40 |
| 17 溫度 (Temperature) | 27, 35, 2, 40 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 35, 26, 28, 18 |
| 22 能量損失 (Loss of energy) | 5, 28, 11, 29 |
| 25 時間浪費 (Loss of time) | 35, 18, 34, 21 |
| 26 物質的量 (Quantity of substance) | 28, 32, 1, 24 |
| 27 可靠性 (Reliability) | 5, 28, 11, 1 |
| 28 量測精度 (Measurement accuracy) | 28, 26, 32, 3 |
| 31 物體產生的有害副作用 (Harmful side effects) | 27, 35, 2, 40 |
| 33 可操作性 (Ease of operation) | 27, 35, 2, 40 |
| 34 可修復性 (Ease of repair) | 27, 35, 10, 34 |
| 35 適應性/多功能性 (Adaptability) | 35, 2, 10, 34 |
| 36 裝置複雜度 (Device complexity) | 27, 26, 28, 13 |
| 39 生產力/效率 (Productivity) | 18, 28, 32, 10 |

## 參數 38: 自動化程度 (Extent of automation)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 28, 26, 18, 35 |
| 2 靜止物體的重量 (Weight of stationary object) | 28, 26, 35, 10 |
| 3 移動物體的長度 (Length of moving object) | 14, 13, 17, 28 |
| 5 移動物體的面積 (Area of moving object) | 23, 14, 25 |
| 7 移動物體的體積 (Volume of moving object) | 17, 14, 13 |
| 9 速度 (Speed) | 35, 13, 16 |
| 10 力 (Force) | 35, 10, 18, 5 |
| 11 應力/壓力 (Stress or pressure) | 15, 10, 35, 2 |
| 12 形狀 (Shape) | 35, 10, 14, 27 |
| 13 物體結構的穩定性 (Stability of composition) | 13, 35, 2 |
| 14 強度 (Strength) | 11, 22, 39, 30 |
| 15 移動物體的耐久性 (Durability of moving object) | 25, 34, 6, 35 |
| 17 溫度 (Temperature) | 13, 35, 2 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 35, 13, 18 |
| 22 能量損失 (Loss of energy) | 28, 10, 35, 23 |
| 25 時間浪費 (Loss of time) | 5, 12, 35, 26 |
| 26 物質的量 (Quantity of substance) | 28, 2, 27 |
| 27 可靠性 (Reliability) | 11, 13, 27, 32 |
| 28 量測精度 (Measurement accuracy) | 28, 26, 18, 35 |
| 31 物體產生的有害副作用 (Harmful side effects) | 1, 2, 13, 35 |
| 33 可操作性 (Ease of operation) | 15, 10, 37, 28 |
| 34 可修復性 (Ease of repair) | 34, 27, 25 |
| 35 適應性/多功能性 (Adaptability) | 35, 10, 2, 16 |
| 36 裝置複雜度 (Device complexity) | 27, 26, 18, 35 |
| 39 生產力/效率 (Productivity) | 5, 12, 35, 26 |

## 參數 39: 生產力/效率 (Productivity)

| 惡化 → | 推薦原理 |
|--------|---------|
| 1 移動物體的重量 (Weight of moving object) | 35, 26, 24, 37 |
| 2 靜止物體的重量 (Weight of stationary object) | 28, 27, 15, 3 |
| 3 移動物體的長度 (Length of moving object) | 18, 4, 28, 38 |
| 5 移動物體的面積 (Area of moving object) | 30, 7, 14, 26 |
| 7 移動物體的體積 (Volume of moving object) | 10, 26, 34, 31 |
| 9 速度 (Speed) | 10, 28, 32, 25 |
| 10 力 (Force) | 28, 15, 10, 36 |
| 11 應力/壓力 (Stress or pressure) | 10, 37, 14 |
| 12 形狀 (Shape) | 14, 10, 34, 40 |
| 13 物體結構的穩定性 (Stability of composition) | 35, 3, 22, 39 |
| 14 強度 (Strength) | 29, 28, 10, 18 |
| 15 移動物體的耐久性 (Durability of moving object) | 35, 10, 2, 18 |
| 17 溫度 (Temperature) | 35, 21, 28, 10 |
| 19 移動物體消耗的能量 (Energy use by moving object) | 28, 15, 10, 36 |
| 22 能量損失 (Loss of energy) | 13, 15, 23 |
| 25 時間浪費 (Loss of time) | 35, 28, 34, 4 |
| 26 物質的量 (Quantity of substance) | 35, 18, 27, 2 |
| 27 可靠性 (Reliability) | 5, 35, 10, 28 |
| 28 量測精度 (Measurement accuracy) | 10, 28, 24, 35 |
| 30 物體受到的有害因素 (Harmful factors acting on object) | 35, 22, 18, 39 |
| 31 物體產生的有害副作用 (Harmful side effects) | 35, 22, 18, 39 |
| 33 可操作性 (Ease of operation) | 1, 28, 7, 19 |
| 34 可修復性 (Ease of repair) | 35, 1, 10, 28 |
| 35 適應性/多功能性 (Adaptability) | 1, 35, 28, 37 |
| 36 裝置複雜度 (Device complexity) | 35, 10, 2, 18 |
| 39 生產力/效率 (Productivity) | 1, 28, 15, 35 |
