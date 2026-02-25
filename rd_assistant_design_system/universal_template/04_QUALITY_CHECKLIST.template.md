# 品質檢查清單

## 一、視覺一致性

### 1.1 色彩系統
- [ ] 主色使用 {{primary_color}}
- [ ] 次要色使用 {{secondary_color}}
- [ ] 強調色使用 {{accent_color}}
- [ ] 錯誤色使用 {{error_color}}
- [ ] 無未定義的顏色使用

### 1.2 字體系統
- [ ] 字體使用 {{font_family}}
- [ ] 字級遵循模組化比例（{{type_scale_ratio}}）
- [ ] 行高設定正確（標題 {{line_height_heading}} / 正文 {{line_height_body}}）

### 1.3 元件風格
- [ ] 圓角統一 {{border_radius}}
- [ ] 陰影使用 {{shadow_style}}
- [ ] 邊框 {{border_style}}
- [ ] Icon 大小一致

### 1.4 間距與佈局
- [ ] 使用 {{grid_system}} 網格系統
- [ ] 區塊間距遵循規範
- [ ] 無隨意間距值

## 二、功能完整性

### 2.1 頁面功能
- [ ] Primary Goal 達成
- [ ] Secondary Goal 達成（如有）
- [ ] 所有必要區塊都存在
- [ ] 導航路徑清晰

### 2.2 互動功能
- [ ] Hover 狀態正確
- [ ] Focus 狀態可見
- [ ] Disabled 狀態合理
- [ ] 點擊/輸入響應正常

### 2.3 狀態處理
- [ ] Loading 狀態有顯示（skeleton / spinner）
- [ ] Error 狀態有提示 + 重試
- [ ] Empty 狀態有引導
- [ ] Success 狀態有回饋

## 三、內容品質

- [ ] 語氣符合品牌調性
- [ ] 無禁用詞
- [ ] 術語使用準確
- [ ] 資料格式正確（日期、數字、百分比）

## 四、技術實作

### 4.1 程式碼
- [ ] 使用指定技術棧（{{tech_stack}}）
- [ ] 元件命名遵循約定（{{component_naming}}）
- [ ] 檔案命名遵循約定（{{file_naming}}）
- [ ] 無使用禁用的函式庫或寫法

### 4.2 效能
- [ ] 首次載入 < {{fcp_target}}
- [ ] 互動響應 < {{interaction_target}}
- [ ] 大資料有虛擬滾動或分頁
- [ ] 圖片延遲載入

## 五、響應式與無障礙

### 5.1 RWD
- [ ] Desktop 佈局正確
- [ ] Tablet 適配良好
- [ ] 關鍵斷點設置正確（{{breakpoints}}）
- [ ] 內容不溢出或斷行

### 5.2 無障礙
- [ ] Tab 順序合理
- [ ] 圖片有 alt 文字
- [ ] 表單標籤關聯正確
- [ ] 錯誤訊息可被螢幕閱讀器讀取

## 六、最終確認

- [ ] 與 Global 規範零衝突（或 Exception 有明確說明）
- [ ] AI 有按三步驟回應（結構確認 → 設計決策 → 程式碼）
- [ ] 所有 Acceptance Criteria 通過

---

**評分標準**：
- **通過**：Critical 0 個，Major ≤ 3 個
- **有條件通過**：Critical 0 個，Major ≤ 5 個，需排程修正
- **不通過**：有 Critical 或 Major > 5 個
