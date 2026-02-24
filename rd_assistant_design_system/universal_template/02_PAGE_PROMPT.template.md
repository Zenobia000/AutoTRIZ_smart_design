# Page-Level Prompt: {{page_name}}

## [PAGE META]
- **page_name**: {{page_name}}
- **route_path**: `{{route_path}}`
- **page_type**: {{page_type}}
  <!-- landing / form / dashboard / report / search / detail / settings -->
- **primary_goal**: {{primary_goal}}
- **secondary_goal**: {{secondary_goal}}

## [USER CONTEXT]
- **target_user_segment**:
  - 主要：{{primary_user_segment}}
  - 次要：{{secondary_user_segment}}
- **entry_point**:
  - {{entry_point_description}}
  <!-- 使用者從哪裡進入此頁？哪個按鈕 / 哪個前一頁 -->
- **expected_time_on_page**: {{expected_time}}
  <!-- 粗估停留時間，幫助決定資訊密度 -->

## [STRUCTURE: SECTIONS]
<!-- 以 top-down 順序列出所有區塊 -->

1. **{{section_1_id}}**
   - section_type: {{section_1_type}}
   <!-- hero / summary / list / form / faq / footer / stats / tabs ... -->
   - section_purpose: {{section_1_purpose}}

2. **{{section_2_id}}**
   - section_type: {{section_2_type}}
   - section_purpose: {{section_2_purpose}}

3. **{{section_3_id}}**
   - section_type: {{section_3_type}}
   - section_purpose: {{section_3_purpose}}

<!-- 依需求增減 section -->

## [SECTION COMPONENT SPEC]
<!-- 每個 section 各寫一段 -->

### Section: {{section_1_id}}
- **layout**: {{layout_description}}
  <!-- 單欄 / 左右雙欄 / 卡片網格 / 時間軸 ... -->
- **elements**:
  - {{element_name}}: {{element_type}}, {{required_or_optional}}, {{content_or_behavior}}
  - {{element_name}}: {{element_type}}, {{required_or_optional}}, {{content_or_behavior}}
- **states**:
  - 正常：{{normal_state}}
  - hover：{{hover_state}}
  - loading：{{loading_state}}
  - empty：{{empty_state}}
  - error：{{error_state}}
- **copy_constraints**:
  - {{text_constraints}}
  <!-- 標題字數限制、是否允許多行等 -->

### Section: {{section_2_id}}
- **layout**: {{layout_description}}
- **elements**:
  - {{element_name}}: {{element_type}}, {{required_or_optional}}, {{content_or_behavior}}
- **states**:
  - {{states_description}}

<!-- 依照 section 數量重複此區塊 -->

## [INTERACTION & STATE FLOW]
- **主要互動流程**：
  1. {{interaction_step_1}}
  2. {{interaction_step_2}}
  3. {{interaction_step_3}}

- **表單驗證規則**（如適用）：
  - {{field_name}}: {{validation_rule}} → {{error_message}}

- **資料更新策略**：
  - {{data_refresh_strategy}}

- **RWD 行為差異**：
  - Desktop (>{{desktop_breakpoint}}): {{desktop_behavior}}
  - Tablet ({{tablet_range}}): {{tablet_behavior}}
  - Mobile (<{{mobile_breakpoint}}): {{mobile_behavior}}

## [DATA & API]
- **uses_api**: {{true_or_false}}
- **endpoints**:
  - {{http_method}} `{{endpoint_path}}` — {{endpoint_description}}
  - {{http_method}} `{{endpoint_path}}` — {{endpoint_description}}
- **error cases**:
  - {{error_case}}: {{fallback_ui}}

## [EXCEPTION TO GLOBAL RULES]
<!-- 如果這一頁要刻意違反 Global 規範，必須在這裡寫明並說明原因 -->
- {{exception_description}} — 原因：{{exception_reason}}
- 或填寫：無特殊例外，完全遵循 Global System Prompt 規範。

## [ACCEPTANCE CRITERIA]
- [ ] {{acceptance_criteria_1}}
- [ ] {{acceptance_criteria_2}}
- [ ] {{acceptance_criteria_3}}
