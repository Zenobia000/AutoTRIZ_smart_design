# TRIZ 76 標準解（76 Standard Solutions / Inventive Standards）

> **適用階段**：Step 5a-3 Su-Field 標準解匹配
> 本文件為 RD 設計助手在進行物質-場（Su-Field）分析後，自動匹配標準解法的知識庫。

---

## 一、物質-場（Su-Field）模型簡介

**Su-Field**（Substance-Field）模型是 TRIZ 中用於描述技術系統最小功能單元的建模方法。一個完整的 Su-Field 模型包含：

- **S1（物質1）**：被作用的對象（Object）
- **S2（物質2）**：作用工具（Tool）
- **F（場）**：S2 對 S1 施加作用所需的能量/場（機械場、熱場、電場、磁場、化學場等）

模型狀態分類：
| 狀態 | 說明 |
|------|------|
| **不完整系統** | 缺少 S1、S2 或 F 中的某個元素 |
| **有效完整系統** | 三要素齊全且功能正常 |
| **有害完整系統** | 三要素齊全但產生有害效應 |
| **不足效應系統** | 三要素齊全但作用效果不足 |

76 標準解的核心邏輯：根據 Su-Field 模型的狀態，從五大類標準解中匹配最適合的改進方向。

---

## 二、76 標準解總覽

| 類別 | 名稱 | 子群數 | 標準解數量 |
|------|------|--------|-----------|
| Class 1 | 不改變或少量改變系統的改進 | 3 | 13 |
| Class 2 | 改變系統的改進 | 4 | 23 |
| Class 3 | 系統轉換 | 2 | 6 |
| Class 4 | 檢測與測量 | 5 | 6 |
| Class 5 | 簡化與改進策略 | 5 | 17 |
| **合計** | | **19** | **76** |

---

## Class 1：不改變或少量改變系統的改進（Improving the System with No or Little Change）

> 適用情境：系統結構基本不變，透過補全、消除有害作用或強化現有作用來改進。

### 1.1 建構 Su-Field 模型（Synthesis of Su-Field Models）— 2 個標準解

#### 1.1.1 建構完整 Su-Field（Build a Complete Su-Field）
**建構完整物質-場模型**

若系統不完整（缺少 S1、S2 或 F），應補全缺失元素以形成完整的 Su-Field。

> **eBike 範例**：電動自行車煞車系統中，若僅有煞車碟盤（S1）和煞車卡鉗（S2）但缺少液壓場（F），則需加入液壓油路形成完整的液壓煞車 Su-Field。

#### 1.1.2 內部添加物（Add Internal Additive）
**引入內部添加物以完善 Su-Field**

當無法直接建構完整 Su-Field 時，可在 S1 或 S2 內部添加物質，使系統功能完整。

> **eBike 範例**：電池芯內部添加導熱填料（添加物），使電池模組（S1）與散熱結構（S2）之間的熱場（F）傳遞更完整。

---

### 1.2 消除或中和有害作用（Destroying Su-Field）— 4 個標準解

#### 1.2.1 引入第三物質消除有害作用（Introduce S3 to Eliminate Harmful Effect）
**引入新物質 S3 消除有害效應**

在產生有害效應的 S1 與 S2 之間，引入第三物質 S3 以消除或隔離有害作用。

> **eBike 範例**：馬達運轉振動（有害場）傳遞至車架，可在馬達與車架之間加入橡膠減振墊（S3）隔離振動。

#### 1.2.2 引入 S1 或 S2 的變體消除有害作用（Introduce Modified S1 or S2）
**以 S1 或 S2 的變體取代原物質**

用 S1 或 S2 自身的改良版本來消除有害效應，避免引入全新物質。

> **eBike 範例**：鏈條傳動噪音問題，將金屬鏈條（S2）改為碳纖維皮帶（S2'），消除金屬摩擦噪音。

#### 1.2.3 引入反向場抵消有害場（Introduce Counter-Field F'）
**引入與有害場方向相反的場 F' 來抵消**

當有害場無法用物質隔離時，施加反向場來中和。

> **eBike 範例**：電磁干擾（EMI）影響控制器，加入反向電磁遮罩場（F'）或主動消噪電路抵消干擾。

#### 1.2.4 利用磁場與磁性物質消除有害作用（Use Magnetic Field and Ferromagnetic Substance）
**利用磁場結合鐵磁物質來隔離或消除有害效應**

> **eBike 範例**：速度感測器受外部磁場干擾產生誤讀，加入鐵磁遮罩層包覆感測器，引導雜散磁場繞過。

---

### 1.3 其他（進階合成與強化）— 7 個標準解

#### 1.3.1 將系統鏈式連接（Chain Su-Field）
**串聯鏈式 Su-Field 結構**

若單一 Su-Field 效果不足，可串聯多個 Su-Field 形成鏈式結構，將上一級輸出作為下一級輸入。

> **eBike 範例**：踏板力矩（F1）→ 力矩感測器（S2）→ 電子信號（F2）→ 控制器（S3）→ PWM 驅動（F3）→ 馬達（S4），形成鏈式 Su-Field。

#### 1.3.2 雙重 Su-Field（Double Su-Field）
**引入第二個場使作用加倍**

在原有 Su-Field 上疊加第二個場，增強或細化作用效果。

> **eBike 範例**：煞車系統同時使用機械場（碟煞）和電磁場（再生煞車），雙重制動提升效能。

#### 1.3.3 擴展至外部環境（Expand to External Environment）
**利用外部環境資源強化系統**

將外部環境中可用的物質或場納入 Su-Field，不增加系統複雜度。

> **eBike 範例**：利用行駛風流（外部氣流場）作為電池散熱的輔助通道，無需額外風扇。

#### 1.3.4 利用外部環境中的物質（Use Substances from External Environment）
**借用環境中已存在的物質**

直接利用環境中已有的物質作為 S3，降低系統成本。

> **eBike 範例**：利用雨水（環境物質）沖洗車架上的泥沙，設計引流槽將雨水導向關鍵清潔部位。

#### 1.3.5 利用最少量的添加物（Use Minimal Additive - Very Small Dose）
**以極少量的添加物實現目的**

引入微量物質即可達到改善效果，最大化效率。

> **eBike 範例**：在軸承中加入微量奈米級潤滑劑，即可大幅降低摩擦損耗。

#### 1.3.6 利用最大量的添加物後再移除（Use Maximal Additive then Remove）
**先大量引入物質完成作用，再將其移除**

暫時性地引入大量物質來完成特定功能，之後移除以恢復原狀。

> **eBike 範例**：車架焊接時在管內充入大量保護氣體（Ar）防止氧化，焊接完成後氣體自然排出。

#### 1.3.7 利用場的變化替代物質（Use Field Instead of Substance）
**用場來替代物質的引入**

當不方便引入物質時，使用場（電場、磁場、熱場等）達到同樣效果。

> **eBike 範例**：以超音波場（F）清潔電路板，替代傳統化學清洗溶劑（S）。

---

## Class 2：改變系統的改進（Improving the System by Changing the System）

> 適用情境：現有系統結構不足以滿足需求，需要進行結構性變更。

### 2.1 轉換為雙系統或多系統（Transition to Bi- and Poly-Systems）— 6 個標準解

#### 2.1.1 建立雙系統或多系統（Create Bi- or Poly-System）
**將單一系統組合為雙系統或多系統**

將兩個或多個相同系統並聯以增強功能。

> **eBike 範例**：單馬達驅動改為前後雙馬達（雙系統），提升全輪驅動能力與扭矩分配。

#### 2.1.2 建立強化的雙系統（Create Enhanced Bi-System）
**由兩個互補的子系統組合成增強系統**

兩個具有互補特性的系統結合，彌補彼此不足。

> **eBike 範例**：鋰電池（高能量密度）+ 超級電容（高功率密度）組成混合儲能系統，兼顧續航與瞬間大電流輸出。

#### 2.1.3 建立反向的雙系統（Create Inverse Bi-System）
**由兩個性質相反的子系統組合**

> **eBike 範例**：加熱 + 冷卻的雙向溫控系統，低溫時預熱電池、高溫時主動冷卻，維持最佳工作溫度。

#### 2.1.4 組合不相容的特性（Combine Incompatible Properties）
**在同一系統中實現看似矛盾的特性**

> **eBike 範例**：車架需同時滿足「剛性」（動力傳遞）和「柔性」（舒適避震），透過局部碳纖維鋪層角度調整，不同區域實現不同剛性。

#### 2.1.5 增加系統元素間的差異性（Increase Difference Between Elements）
**增大多系統中各元素的差異以產生新功能**

> **eBike 範例**：多段變速齒輪組中，齒數比差異加大，使低速爬坡與高速巡航的切換更加明顯有效。

#### 2.1.6 多系統收斂為單系統（Fold Poly-System into Mono-System）
**多系統整合收斂為更簡潔的單一系統**

當多系統過於複雜，可將功能整合至單一元件。

> **eBike 範例**：將分離的馬達、減速齒輪箱、力矩感測器整合為一體化中置馬達單元。

---

### 2.2 發展 Su-Field（Developing Su-Field）— 6 個標準解

#### 2.2.1 以更易控制的場替代（Replace Field with More Controllable One）
**將不易控制的場替換為更易控制的場**

場的可控性排序：機械 < 熱 < 化學 < 電 < 磁。

> **eBike 範例**：將機械式調速（摩擦離合器）替換為電子調速（PWM 控制器），提升精確度。

#### 2.2.2 將物質碎片化（Fragment S2）
**將工具物質 S2 分解為更細小的顆粒或碎片**

> **eBike 範例**：將整塊散熱片改為微通道散熱鰭片陣列，增大散熱面積。

#### 2.2.3 使用毛細管或多孔結構（Use Capillary / Porous Structures）
**引入毛細管或多孔材料增強物質傳輸**

> **eBike 範例**：在電池液冷板中採用微孔燒結結構，利用毛細作用均勻分配冷卻液。

#### 2.2.4 增加系統動態性（Increase Dynamism）
**使系統從剛性轉為可變形、可調節**

> **eBike 範例**：可調節角度的車把手立管，騎行者可根據路況即時調整騎姿。

#### 2.2.5 結構化場（Structure the Field）
**將均勻場改為非均勻（結構化）場以提高效能**

> **eBike 範例**：馬達定子繞組採用集中繞組（非均勻磁場分佈），在特定位置集中磁通量提升效率。

#### 2.2.6 結構化物質（Structure the Substance）
**將均質物質改為非均質結構以提高效能**

> **eBike 範例**：車架管材從等壁厚改為變壁厚（受力處加厚、非受力處減薄），減重同時維持強度。

---

### 2.3 利用節奏與共振（Rhythms and Resonance Coordination）— 3 個標準解

#### 2.3.1 場的節奏匹配（Match Field Rhythm to System Rhythm）
**使外加場的頻率與系統自然頻率匹配或刻意錯開**

> **eBike 範例**：PWM 驅動頻率避開馬達機械共振頻率，避免產生振動噪音。

#### 2.3.2 場與場之間的節奏匹配（Match Rhythms of Two Fields）
**協調兩個場之間的節奏關係**

> **eBike 範例**：電池充電脈衝頻率與電池內部化學反應速率匹配，提高充電效率減少衰減。

#### 2.3.3 利用兩個不同場（Use Two Incompatible Fields）
**同時施加兩個不同頻率/類型的場，利用其交互作用**

> **eBike 範例**：馬達同時接受高頻 PWM 電場驅動與低頻機械振動反饋，實現自適應控制。

---

### 2.4 利用鐵磁物質與磁場（Ferromagnetic Su-Field / Fe-Field）— 8 個標準解

#### 2.4.1 引入鐵磁物質（Introduce Ferromagnetic Substance）
**在 Su-Field 中引入鐵磁粒子作為中介物質**

> **eBike 範例**：磁流變液應用於避震器，透過磁場控制鐵磁顆粒排列改變阻尼特性。

#### 2.4.2 利用鐵磁顆粒（Use Ferromagnetic Particles）
**以鐵磁微粒替代整體鐵磁物質**

> **eBike 範例**：煞車系統中使用鐵磁粉末離合器，透過電磁場調節粉末摩擦力控制制動力道。

#### 2.4.3 利用外部磁場控制鐵磁物質（Use External Magnetic Field）
**用外部可控磁場操控鐵磁物質的行為**

> **eBike 範例**：在鎖具中使用電磁鐵控制鐵磁鎖芯，實現無鑰匙電子解鎖。

#### 2.4.4 利用磁流體（Use Magnetic Fluid / Ferrofluid）
**以磁流體替代固態鐵磁物質**

> **eBike 範例**：馬達軸承密封處使用磁流體密封，無接觸摩擦且防塵防水。

#### 2.4.5 利用複合鐵磁物質（Use Composite Ferromagnetic Structures）
**鐵磁物質與非鐵磁物質組合形成複合結構**

> **eBike 範例**：馬達轉子使用矽鋼片（鐵磁）與絕緣層（非鐵磁）交替層壓，降低渦電流損耗。

#### 2.4.6 引入外部鐵磁環境（Introduce Ferromagnetic Environment）
**將鐵磁物質引入系統外部環境**

> **eBike 範例**：充電座底部嵌入磁鐵陣列，自動對準與吸附充電接頭位置。

#### 2.4.7 利用磁場的物理效應（Use Physical Effects of Magnetic Field）
**直接利用磁場的居里點、磁致伸縮等物理效應**

> **eBike 範例**：利用磁致伸縮材料作為力矩感測元件，將扭力變化轉為磁場變化進行量測。

#### 2.4.8 利用動態磁場（Use Dynamic / Oscillating Magnetic Field）
**使用交變或旋轉磁場替代靜態磁場**

> **eBike 範例**：無線充電系統使用高頻交變磁場進行非接觸式能量傳輸。

---

## Class 3：系統轉換（System Transitions）

> 適用情境：在現有系統層級內已無法進一步改進，需向更高或更低層級轉換。

### 3.1 轉換至超系統（Transition to Super-System）— 3 個標準解

#### 3.1.1 合併至超系統（Merge into Super-System）
**將系統與相鄰系統合併為更高階超系統**

> **eBike 範例**：將 eBike 系統與智慧城市交通管理系統整合，實現即時路況導航與車群協調。

#### 3.1.2 利用超系統中的資源（Use Super-System Resources）
**從超系統中提取可用資源以改善子系統**

> **eBike 範例**：利用手機 GPS 與加速度感測器（超系統資源），替代 eBike 自身的獨立感測器，降低成本。

#### 3.1.3 在超系統層級消除有害因素（Eliminate Harmful Factors at Super-System Level）
**把子系統無法解決的問題，上升到超系統層級處理**

> **eBike 範例**：單車防盜在車輛層級難以完善，上升至社區共享停車站層級設計統一監控防盜系統。

---

### 3.2 轉換至微觀層級（Transition to Micro-Level）— 3 個標準解

#### 3.2.1 從巨觀轉為微觀操作（Transition from Macro to Micro Level）
**將巨觀的機械式操作改為微觀層級操作**

> **eBike 範例**：傳統機械接點式開關改為半導體 MOSFET 固態開關，從巨觀接觸轉為微觀電子層級控制。

#### 3.2.2 利用微觀結構（Use Micro-Structures）
**在微觀層級設計結構以實現巨觀功能**

> **eBike 範例**：車架表面施加奈米疏水塗層（微觀結構），實現巨觀的自潔防鏽功能。

#### 3.2.3 利用物質在微觀層級的物理/化學特性（Use Micro-Level Physical/Chemical Properties）
**利用物質在分子或原子層級的特殊性質**

> **eBike 範例**：鋰電池正極材料採用奈米級磷酸鐵鋰顆粒，利用其微觀層級的高表面積特性提升充放電速率。

---

## Class 4：檢測與測量（Detection and Measurement Standards）

> 適用情境：需要檢測或測量某個參數但現有方法不可行或不夠精確。

### 4.1 間接方法（Indirect Methods）— 1 個標準解

#### 4.1.1 以模型替代直接測量（Use a Detectable Copy/Model Instead of Direct Measurement）
**用可偵測的替代物或模型間接測量目標參數**

若目標參數難以直接測量，用與之相關的可觀測量來間接推算。

> **eBike 範例**：無法直接測量電池內部溫度，透過量測電池內阻變化（間接參數）推算內部核心溫度。

---

### 4.2 建構測量 Su-Field（Synthesis of Measurement Su-Field）— 1 個標準解

#### 4.2.1 建構測量用 Su-Field（Build a Measurement Su-Field）
**為測量需求建構專用的 Su-Field 模型**

若系統中無法量測某參數，建構專用的測量 Su-Field（感測器 + 被測物 + 探測場）。

> **eBike 範例**：在馬達控制中建構轉速測量 Su-Field：磁鐵（S1 在轉子）+ 霍爾感測器（S2）+ 磁場（F），量測轉速。

---

### 4.3 強化測量 Su-Field（Enhancing Measurement Su-Field）— 1 個標準解

#### 4.3.1 強化現有測量 Su-Field（Enhance Existing Measurement Su-Field）
**對現有測量系統加入額外的場或物質以提升量測精度**

> **eBike 範例**：力矩感測器靈敏度不足，在應變規表面增加磁致伸縮塗層（附加場效應），放大力矩信號。

---

### 4.4 轉向鐵磁測量 Su-Field（Transition to Ferromagnetic Measurement Su-Field）— 1 個標準解

#### 4.4.1 使用鐵磁標記物進行測量（Use Ferromagnetic Markers for Measurement）
**在被測物上加入鐵磁標記，利用磁場進行非接觸測量**

> **eBike 範例**：在鏈條每個鏈節嵌入微型磁性標記，以磁感測器非接觸式量測鏈條伸長量（磨損程度）。

---

### 4.5 測量系統的演化方向（Evolution Direction of Measurement Systems）— 2 個標準解

#### 4.5.1 利用物理/化學效應進行測量（Use Physical/Chemical Effects for Measurement）
**利用物理或化學效應實現新的測量方式**

> **eBike 範例**：利用壓電效應（物理效應）量測輪胎壓力，壓電薄膜感測器嵌入輪圈內。

#### 4.5.2 利用共振進行測量（Use Resonance for Measurement）
**利用共振頻率變化來檢測參數變化**

> **eBike 範例**：車架結構健康監測——在車架上安裝壓電元件激發振動，透過共振頻率偏移檢測裂紋。

---

## Class 5：簡化與改進策略（Strategies for Simplification and Improvement）

> 適用情境：已找到概念解，需要進一步簡化實施或提升效果。

### 5.1 引入物質的策略（Strategies for Introducing Substances）— 4 個標準解

#### 5.1.1 間接引入物質（Introduce Substance Indirectly）
**以間接方式引入所需物質，避免直接添加帶來的副作用**

> **eBike 範例**：電路板防潮不直接塗膠，而是在製程中通入惰性氣體後密封，間接實現防潮。

#### 5.1.2 引入場的變體替代物質（Introduce Field Instead of Substance）
**用場來實現原本需要物質才能達到的功能**

> **eBike 範例**：清潔馬達繞組時，用紫外線場殺菌替代化學清洗劑。

#### 5.1.3 利用外部物質作為臨時載體（Use External Substance as Temporary Carrier）
**借用外部物質暫時充當載體，任務完成後移除**

> **eBike 範例**：碳纖維車架成型時使用可溶性芯模（臨時載體），成型後溶解取出。

#### 5.1.4 利用「無」或「虛空」作為物質（Use "Void" / "Nothing" as Substance）
**利用空隙、氣泡、真空等「虛空」結構作為功能元素**

> **eBike 範例**：輪胎內部採用蜂巢式空腔結構（虛空），實現免充氣防爆輪胎。

---

### 5.2 引入場的策略（Strategies for Introducing Fields）— 3 個標準解

#### 5.2.1 利用多功能場（Use Multi-Functional Field）
**讓同一個場同時執行多項功能**

> **eBike 範例**：馬達產生的磁場同時用於驅動轉子和為轉速感測器提供偵測信號，一場兩用。

#### 5.2.2 利用環境中已存在的場（Use Fields from Environment）
**利用環境中自然存在的場作為功能資源**

> **eBike 範例**：利用地球重力場，設計再生煞車系統在下坡時自動回收動能轉為電能。

#### 5.2.3 利用能夠攜帶場的物質（Use Substances that Carry Fields）
**選擇本身攜帶所需場效應的物質**

> **eBike 範例**：選用永磁材料（自帶磁場）作為馬達轉子，無需外部勵磁線圈。

---

### 5.3 相變與物態轉換（Phase Transitions and State Changes）— 5 個標準解

#### 5.3.1 利用相變（Use Phase Transition）
**利用物質的相變（固↔液↔氣）實現功能**

> **eBike 範例**：電池組使用相變材料（PCM）散熱，材料吸熱融化→暫存熱量→低溫時凝固釋熱，平滑溫度波動。

#### 5.3.2 利用「雙態」物質（Use Dual-State Substance）
**同一物質在兩種狀態間切換以實現不同功能**

> **eBike 範例**：形狀記憶合金製成的通風百葉窗，低溫時關閉保溫、高溫時自動張開通風（固態↔回復態）。

#### 5.3.3 利用相變產生的伴隨效應（Use Accompanying Effects of Phase Transition）
**利用相變過程中產生的體積變化、熱量釋放/吸收等效應**

> **eBike 範例**：水結冰膨脹的原理用於防凍監測——在暴露管路中設置膨脹感測器，冰點前發出預警。

#### 5.3.4 利用兩相物質替代單相（Replace Single-Phase with Two-Phase Substance）
**用雙相混合物替代單相物質以獲得額外特性**

> **eBike 範例**：散熱管內使用氣液兩相工質（熱管），相變過程高效傳熱遠優於純液態冷卻液。

#### 5.3.5 利用相互作用的物質（Use Interacting Substances / Physicochemical Effects）
**利用不同物質之間的物理或化學交互作用**

> **eBike 範例**：自修復輪胎——橡膠內層含微膠囊，刺穿時膠囊破裂釋放黏合劑（化學反應），自動封堵孔洞。

---

### 5.4 利用物理效應（Use Physical Effects）— 2 個標準解

#### 5.4.1 自適應物質（Self-Adaptive / Self-Controlled Substances）
**使用能根據環境自動改變特性的物質**

> **eBike 範例**：電致變色車燈罩，根據環境光照強度自動調節透光率，白天高透光、夜間降低眩光。

#### 5.4.2 利用多物理效應耦合（Use Coupled Physical Effects）
**利用不同物理效應之間的耦合關係**

> **eBike 範例**：壓電-電磁耦合式能量收集器，同時從振動中透過壓電效應和電磁感應收集能量。

---

### 5.5 利用實驗方法獲得微粒子（Obtaining Particles / Substances Under Experimental Conditions）— 3 個標準解

#### 5.5.1 由分解或合成方式獲得所需物質（Obtain Substance by Decomposition or Synthesis）
**在系統內原位分解或合成所需的物質**

> **eBike 範例**：電解水產氫用於燃料電池增程器——水（已有物質）在系統內分解為氫氣（所需物質）。

#### 5.5.2 由元素分解獲得所需物質（Obtain Substance by Decomposing an Element of the System）
**從系統中已有的元素分解獲取所需物質**

> **eBike 範例**：利用電池充放電過程中產生的微量氣體驅動壓力感測器，無需額外氣源。

#### 5.5.3 利用添加物的反應產物（Use Reaction Products of Additives）
**引入添加物，利用其反應後的產物來實現功能**

> **eBike 範例**：PCB 焊接助焊劑反應後的殘留物具有防腐蝕特性，設計免清洗助焊劑使殘留物直接充當保護層。

---

## 三、標準解匹配流程（Quick Reference）

```
1. 建立 Su-Field 模型
   ├─ 不完整系統 → Class 1.1（建構 Su-Field）
   ├─ 有害效應系統 → Class 1.2（消除有害作用）
   ├─ 不足效應系統 → Class 1.3 / Class 2（強化或改變系統）
   └─ 測量問題 → Class 4（檢測與測量）

2. 系統改變方向
   ├─ 結構不變 → Class 1
   ├─ 結構改變 → Class 2
   ├─ 層級改變 → Class 3
   └─ 實施簡化 → Class 5

3. 最終選擇
   └─ 對比多個候選標準解，選擇最符合「理想性」的方案
```

---

## 四、參考文獻

1. Altshuller, G. S. (1984). *Creativity as an Exact Science*. Gordon and Breach.
2. Savransky, S. D. (2000). *Engineering of Creativity: Introduction to TRIZ Methodology of Inventive Problem Solving*. CRC Press.
3. Terninko, J., Zusman, A., & Zlotin, B. (1998). *Systematic Innovation: An Introduction to TRIZ*. CRC Press.
4. Mann, D. (2002). *Hands-On Systematic Innovation*. CREAX Press.
5. 檀潤華 (2002).《TRIZ 及應用——技術創新過程與方法》. 高等教育出版社.
