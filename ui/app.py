"""RD Design Copilot - Streamlit UI"""
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path for both `streamlit run ui/app.py` and `streamlit run app.py`
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st
from ui import api_client as api

st.set_page_config(page_title="RD Design Copilot", page_icon="🔧", layout="wide")

# --- Session State ---
if "project_id" not in st.session_state:
    st.session_state.project_id = None


def set_project(pid: str):
    st.session_state.project_id = pid


# --- Sidebar ---
st.sidebar.title("RD Design Copilot")

# Project selector
try:
    projects = api.list_projects()
except Exception:
    st.sidebar.error("無法連接後端 API，請確認 FastAPI 已啟動 (port 8000)")
    st.stop()

project_names = {p["id"]: p["name"] for p in projects}
if projects:
    selected = st.sidebar.selectbox(
        "選擇專案",
        options=[p["id"] for p in projects],
        format_func=lambda x: f"{project_names[x]} ({x[:8]}...)",
        index=0 if not st.session_state.project_id else
              next((i for i, p in enumerate(projects) if p["id"] == st.session_state.project_id), 0),
    )
    set_project(selected)

# New project
with st.sidebar.expander("建立新專案"):
    new_name = st.text_input("專案名稱", key="new_name")
    new_desc = st.text_area("描述", key="new_desc", height=80)
    if st.button("建立") and new_name:
        p = api.create_project(new_name, new_desc)
        set_project(p["id"])
        st.rerun()

# Navigation
if st.session_state.project_id:
    project = api.get_project(st.session_state.project_id)
    st.sidebar.markdown(f"**狀態**: `{project['status']}`")

    page = st.sidebar.radio(
        "導航",
        [
            "Step 1.1 - 問題界定",
            "Step 1.2 - 索克拉底問答",
            "Step 1.2 - 矛盾識別",
            "Step 1.3 - 因果迴路圖",
            "Step 1.3 - 斷路點識別",
            "Gate 1.1",
            "Step 2.1 - 假設台帳",
            "Step 2.1 - 未知集合 (U)",
            "Step 2.2.1 - Anti-Anchor Sprint",
            "Step 2.2.2 - TRIZ 解法",
            "Step 2.2.4 - SCAMPER 變形",
            "Step 2.2.5 - 方案集合",
            "Step 2.2.6 - MUST 篩選",
            "Gate 2.2",
            "Step 3.2 - WANT 評分",
            "Step 3.1 - 風險評估",
            "Step 3.2 - KT 決策記錄",
            "Step 3.1.loop - 最小實驗",
            "Gate 3.2",
            "匯出報告",
        ],
    )
else:
    st.info("請先建立或選擇一個專案")
    st.stop()

pid = st.session_state.project_id


# ========== PAGES ==========

# --- Step 1.1: Task Definition ---
if page == "Step 1.1 - 問題界定":
    st.header("任務定義表")

    defn = api.get_definition(pid)

    with st.expander("AI 生成任務定義", expanded=not defn):
        req_text = st.text_area("需求描述", height=150, key="req_text")
        constraints = st.text_area("補充約束", height=80, key="constraints")
        if st.button("AI 生成", type="primary") and req_text:
            try:
                with st.spinner("AI 正在生成任務定義表..."):
                    defn = api.generate_definition(pid, req_text, constraints)
                st.success("生成完成！")
                st.rerun()
            except Exception as e:
                st.error(f"生成失敗：{e}")

    if defn:
        st.subheader("Mission")
        mission = st.text_area("Mission", value=defn.get("mission", ""), height=100, key="mission_edit")

        st.subheader("Hard Constraints")
        hc_data = defn.get("hard_constraints", [])
        for i, hc in enumerate(hc_data):
            cols = st.columns(3)
            hc["name"] = cols[0].text_input("名稱", value=hc.get("name", ""), key=f"hc_name_{i}")
            hc["value"] = cols[1].text_input("值", value=hc.get("value", ""), key=f"hc_val_{i}")
            hc["source"] = cols[2].text_input("來源", value=hc.get("source", ""), key=f"hc_src_{i}")

        st.subheader("Critical Metrics (三個最不能失敗指標)")
        cm_data = defn.get("critical_metrics", [])
        for i, cm in enumerate(cm_data):
            cols = st.columns(3)
            cm["name"] = cols[0].text_input("指標名", value=cm.get("name", ""), key=f"cm_name_{i}")
            cm["target"] = cols[1].text_input("目標", value=cm.get("target", ""), key=f"cm_target_{i}")
            cm["method"] = cols[2].text_input("判斷方式", value=cm.get("method", ""), key=f"cm_method_{i}")

        st.subheader("Non-Goals")
        ng = defn.get("non_goals", [])
        non_goals_text = st.text_area("Non-Goals (一行一個)", value="\n".join(ng), key="ng_edit")

        if st.button("儲存修改"):
            api.update_definition(pid, {
                "mission": mission,
                "hard_constraints": hc_data,
                "soft_objectives": defn.get("soft_objectives", []),
                "non_goals": [x.strip() for x in non_goals_text.split("\n") if x.strip()],
                "critical_metrics": cm_data,
            })
            st.success("已儲存")


# --- Step 1.2: Socratic Questions ---
elif page == "Step 1.2 - 索克拉底問答":
    st.header("索克拉底式提問")

    if st.button("AI 生成問題", type="primary"):
        with st.spinner("AI 正在生成索克拉底問題..."):
            api.generate_questions(pid)
        st.rerun()

    questions = api.list_questions(pid)
    if not questions:
        st.info("尚無問題。請先生成任務定義表，再按「AI 生成問題」。")
    else:
        categories = {"clarify": "釐清", "assumption": "假設", "evidence": "證據",
                      "perspective": "觀點", "consequence": "後果", "reflection": "反思"}
        for cat_key, cat_name in categories.items():
            cat_qs = [q for q in questions if q["category"] == cat_key]
            if cat_qs:
                st.subheader(f"{cat_name}類")
                for q in cat_qs:
                    with st.expander(q["question"], expanded=not q.get("answer")):
                        answer = st.text_area(
                            "回答",
                            value=q.get("answer") or "",
                            key=f"ans_{q['id']}",
                            height=80,
                        )
                        if st.button("儲存", key=f"save_{q['id']}"):
                            api.answer_question(pid, q["id"], answer)
                            st.success("已儲存")


# --- Step 1.2: Contradictions ---
elif page == "Step 1.2 - 矛盾識別":
    st.header("TRIZ 矛盾識別")

    if st.button("AI 識別矛盾", type="primary"):
        with st.spinner("AI 正在識別工程矛盾..."):
            api.identify_contradictions(pid)
        st.rerun()

    contradictions = api.list_contradictions(pid)
    if contradictions:
        for c in contradictions:
            with st.expander(f"{c['code']}: {c['improve_param']} vs {c['worsen_param']}"):
                st.write(f"**工程描述**: {c['engineering_desc']}")
                if c.get("physical_contradiction"):
                    st.write(f"**物理矛盾**: {c['physical_contradiction']}")
                st.write(f"**來源**: {c.get('source', '')}")
    else:
        st.info("尚無矛盾。請先完成索克拉底問答，再按「AI 識別矛盾」。")


# --- Step 1.3: Causal Loops ---
elif page == "Step 1.3 - 因果迴路圖":
    st.header("因果迴路圖")
    st.caption("找到耦合點（未知會放大的地方），為 TRIZ 矛盾定義與斷路點識別打基礎。")

    if st.button("AI 建模因果迴路 + 斷路點", type="primary"):
        try:
            with st.spinner("AI 正在從問答與矛盾中抽取因果關係..."):
                result = api.generate_causal_loops(pid)
            n_loops = len(result.get("causal_loops", []))
            n_bps = len(result.get("breakpoints", []))
            st.success(f"生成完成！{n_loops} 個因果迴路 + {n_bps} 個斷路點")
            st.rerun()
        except Exception as e:
            st.error(f"生成失敗：{e}")

    loops = api.list_causal_loops(pid)

    with st.expander("手動新增因果迴路", expanded=not loops):
        cl_name = st.text_input("迴路名稱", placeholder="例如：熱-機-振 耦合迴路", key="cl_name")
        cl_desc = st.text_area("迴路說明", height=60, key="cl_desc")

        st.markdown("**節點** (一行一個，格式：`id,標籤`)")
        cl_nodes_text = st.text_area(
            "節點列表", height=100, key="cl_nodes",
            placeholder="P,功率/負載\nH,發熱增加\nT,溫度上升\nR,效率下降\nD,零件變形\nN,NVH上升",
        )
        st.markdown("**邊** (一行一條，格式：`from,to,極性(+/-),標籤(選填)`)")
        cl_edges_text = st.text_area(
            "邊列表", height=100, key="cl_edges",
            placeholder="P,H,+,負載驅動發熱\nH,T,+,\nT,R,-,溫升降低效率\nR,P,+,效率下降加重負載\nT,D,+,熱變形\nD,N,+,變形引發振動",
        )

        if st.button("建立迴路", type="primary") and cl_name:
            nodes = []
            for line in cl_nodes_text.strip().split("\n"):
                parts = [p.strip() for p in line.split(",", 1)]
                if len(parts) == 2:
                    nodes.append({"id": parts[0], "label": parts[1]})
            edges = []
            for line in cl_edges_text.strip().split("\n"):
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 3:
                    edges.append({
                        "from": parts[0], "to": parts[1],
                        "polarity": parts[2],
                        "label": parts[3] if len(parts) > 3 else "",
                    })
            api.create_causal_loop(pid, {
                "name": cl_name, "description": cl_desc,
                "nodes": nodes, "edges": edges,
            })
            st.rerun()

    if loops:
        for loop in loops:
            with st.expander(f"🔄 {loop['name']}", expanded=True):
                if loop.get("description"):
                    st.markdown(f"**說明**：{loop['description']}")

                # Display nodes
                nodes = loop.get("nodes", [])
                edges = loop.get("edges", [])

                if nodes:
                    st.markdown("**節點**")
                    node_labels = {n["id"]: n["label"] for n in nodes}
                    st.write(" → ".join(f"`{n['id']}` {n['label']}" for n in nodes))

                if edges:
                    st.markdown("**因果關係**")
                    for e in edges:
                        src = node_labels.get(e["from"], e["from"])
                        tgt = node_labels.get(e["to"], e["to"])
                        pol = "➕" if e.get("polarity") == "+" else "➖"
                        label = f" ({e['label']})" if e.get("label") else ""
                        st.write(f"  {src} —{pol}→ {tgt}{label}")

                # Mermaid preview
                if nodes and edges:
                    st.markdown("**迴路圖 (Mermaid)**")
                    mermaid_lines = ["flowchart LR"]
                    for n in nodes:
                        mermaid_lines.append(f"    {n['id']}[{n['label']}]")
                    for e in edges:
                        pol = e.get("polarity", "+")
                        mermaid_lines.append(f"    {e['from']} -->|{pol}| {e['to']}")
                    st.code("\n".join(mermaid_lines), language="mermaid")

                # Delete
                if st.button("刪除此迴路", key=f"del_cl_{loop['id']}"):
                    api.delete_causal_loop(pid, loop["id"])
                    st.rerun()


# --- Step 1.3: Breakpoints ---
elif page == "Step 1.3 - 斷路點識別":
    st.header("斷路點識別")
    st.caption("在因果迴路中找到可介入切斷耦合的位置，為解法方向提供指引。")

    loops = api.list_causal_loops(pid)
    breakpoints = api.list_breakpoints(pid)

    if not loops:
        st.warning("請先建立因果迴路圖")
    else:
        loop_map = {l["id"]: l["name"] for l in loops}

        with st.expander("新增斷路點", expanded=not breakpoints):
            bp_code = st.text_input("編號", value=f"BP-{len(breakpoints)+1:03d}", key="bp_code")
            bp_loop = st.selectbox(
                "所屬因果迴路",
                options=[l["id"] for l in loops],
                format_func=lambda x: loop_map.get(x, x),
                key="bp_loop",
            )
            bp_location = st.text_input("斷路位置", key="bp_loc", placeholder="例如：馬達-減速機界面")
            bp_desc = st.text_area("斷路點說明", height=60, key="bp_desc")
            bp_solution = st.text_input("可能解法方向", key="bp_sol", placeholder="例如：隔熱隔振分區")
            bp_triz = st.text_input("TRIZ 原理提示", key="bp_triz", placeholder="例如：#1分割, #2分離")
            if st.button("建立斷路點", type="primary") and bp_location:
                api.create_breakpoint(pid, {
                    "code": bp_code, "causal_loop_id": bp_loop,
                    "location": bp_location, "description": bp_desc,
                    "solution_direction": bp_solution, "triz_principles": bp_triz,
                })
                st.rerun()

    if breakpoints:
        st.divider()
        st.subheader("斷路點列表")

        # Summary table
        cols_header = st.columns([1, 2, 2, 2, 2])
        cols_header[0].markdown("**編號**")
        cols_header[1].markdown("**位置**")
        cols_header[2].markdown("**解法方向**")
        cols_header[3].markdown("**TRIZ 原理**")
        cols_header[4].markdown("**所屬迴路**")

        for bp in breakpoints:
            with st.expander(f"🔧 {bp['code']}：{bp['location']}"):
                st.write(f"**位置**：{bp['location']}")
                if bp.get("description"):
                    st.write(f"**說明**：{bp['description']}")
                st.write(f"**可能解法方向**：{bp.get('solution_direction', '')}")
                st.write(f"**TRIZ 原理提示**：{bp.get('triz_principles', '')}")
                loop_name = loop_map.get(bp.get("causal_loop_id", ""), "—") if loops else "—"
                st.write(f"**所屬迴路**：{loop_name}")

                ecols = st.columns([2, 2, 1])
                new_sol = ecols[0].text_input("更新解法方向", value=bp.get("solution_direction", ""), key=f"bps_{bp['id']}")
                new_triz = ecols[1].text_input("更新 TRIZ 原理", value=bp.get("triz_principles", ""), key=f"bpt_{bp['id']}")
                if ecols[2].button("更新", key=f"bpu_{bp['id']}"):
                    api.update_breakpoint(pid, bp["id"], {"solution_direction": new_sol, "triz_principles": new_triz})
                    st.rerun()

                if st.button("刪除", key=f"bpd_{bp['id']}"):
                    api.delete_breakpoint(pid, bp["id"])
                    st.rerun()


# --- Gate 1.1 ---
elif page == "Gate 1.1":
    st.header("Gate 1.1 檢查")
    if st.button("執行 Gate 1.1 檢查", type="primary"):
        result = api.check_gate(pid, 1)
        st.session_state["gate1_result"] = result
    result = st.session_state.get("gate1_result")
    if result:
        for item in result["checklist"]:
            icon = "✅" if item["passed"] else "❌"
            st.write(f"{icon} {item['item']} {item.get('note', '')}")
        if result["overall_pass"]:
            st.success("Gate 1.1 通過！可進入 Phase 2: Diverge")
        else:
            st.warning("Gate 1.1 未通過，請補齊缺項")


# --- Step 2.1: Assumptions ---
elif page == "Step 2.1 - 假設台帳":
    st.header("假設台帳")

    ASSUMPTION_TYPES = ["介面/包絡", "系統邊界/架構", "可靠度/壽命", "NVH/體驗", "環境可靠度", "低溫性能", "製程/DFM", "成本", "其他"]
    RISK_LEVELS = ["High", "Medium-High", "Medium", "Low"]
    SOURCES = ["規格需求", "案例/競品", "工程常識", "初算/推估", "供應商資料", "文獻"]
    STATUSES = ["Open", "Planned", "Verifying", "Verified", "Disproved"]

    assumptions = api.list_assumptions(pid)

    # AI batch extraction
    st.subheader("AI 萃取假設")
    st.caption("從任務定義、問答記錄、矛盾、斷路點、因果迴路等上游工件，批次萃取隱含假設。已有的手動假設不會被覆蓋。")
    if st.button("AI 萃取假設", type="secondary"):
        with st.spinner("正在分析上游工件並萃取假設..."):
            try:
                result = api.extract_assumptions(pid)
                st.success(f"已萃取 {result['extracted_count']} 個假設")
                st.rerun()
            except Exception as e:
                st.error(f"萃取失敗：{e}")

    st.divider()

    with st.expander("手動新增假設", expanded=not assumptions):
        cols = st.columns([1, 2])
        a_code = cols[0].text_input("編號", value=f"A-{len(assumptions)+1:03d}")
        a_type = cols[1].selectbox("假設類型", ASSUMPTION_TYPES, key="new_a_type")
        a_content = st.text_area("假設內容", height=80, key="new_a_content", placeholder="描述具體假設，包含數值條件...")
        cols2 = st.columns(3)
        a_source = cols2[0].selectbox("依據/來源", SOURCES, key="new_a_source")
        a_risk = cols2[1].selectbox("風險等級", RISK_LEVELS, index=2, key="new_a_risk")
        a_owner = cols2[2].text_input("Owner", key="new_a_owner", placeholder="例如：機構 RD")
        a_worst = st.text_area("若假設不成立的影響", height=60, key="new_a_worst")
        a_verify = st.text_area("驗證方法", height=80, key="new_a_verify", placeholder="1) ...\n2) ...\n3) ...")
        a_accept = st.text_area("驗收/判定標準", height=60, key="new_a_accept")
        a_due = st.text_input("目標完成", key="new_a_due", placeholder="例如：Gate 1.2 前, Phase Gate 1 前")
        if st.button("新增假設", type="primary") and a_content:
            api.create_assumption(pid, {
                "code": a_code, "content": a_content, "assumption_type": a_type,
                "source": a_source, "worst_consequence": a_worst, "risk_level": a_risk,
                "verification_method": a_verify, "acceptance_criteria": a_accept,
                "owner": a_owner, "due_date": a_due,
            })
            st.rerun()

    if assumptions:
        # Summary bar
        risk_counts = {}
        for a in assumptions:
            rl = a.get("risk_level", "Medium")
            risk_counts[rl] = risk_counts.get(rl, 0) + 1
        status_counts = {}
        for a in assumptions:
            s = a.get("status", "Open")
            status_counts[s] = status_counts.get(s, 0) + 1
        scols = st.columns(len(risk_counts) + len(status_counts))
        i = 0
        risk_icons = {"High": "🔴", "Medium-High": "🟠", "Medium": "🟡", "Low": "🟢"}
        for rl, cnt in sorted(risk_counts.items()):
            scols[i].metric(f"{risk_icons.get(rl, '⚪')} {rl}", cnt)
            i += 1
        for s, cnt in sorted(status_counts.items()):
            scols[i].metric(s, cnt)
            i += 1

        st.divider()

        for a in assumptions:
            risk_icon = risk_icons.get(a.get("risk_level", ""), "⚪")
            label = f"{risk_icon} {a['code']}｜{a['content'][:50]}{'...' if len(a['content']) > 50 else ''} [{a.get('status', 'Open')}]"
            with st.expander(label):
                st.markdown(f"**假設內容**：{a['content']}")
                cols = st.columns(4)
                cols[0].write(f"**類型**：{a.get('assumption_type', '')}")
                cols[1].write(f"**依據**：{a['source']}")
                cols[2].write(f"**風險**：{risk_icon} {a.get('risk_level', '')}")
                cols[3].write(f"**Owner**：{a.get('owner', '')}")

                if a.get("worst_consequence"):
                    st.markdown(f"**若不成立的影響**：{a['worst_consequence']}")
                if a.get("verification_method"):
                    st.markdown(f"**驗證方法**：\n{a['verification_method']}")
                if a.get("acceptance_criteria"):
                    st.markdown(f"**驗收/判定標準**：\n{a['acceptance_criteria']}")
                if a.get("due_date"):
                    st.write(f"**目標完成**：{a['due_date']}")
                if a.get("source_refs"):
                    refs = a["source_refs"]
                    tags = " ".join(f"`{r.get('type', '')}:{r.get('code', '')}`" for r in refs)
                    st.markdown(f"**來源追溯**：{tags}")

                # Edit status
                st.divider()
                ecols = st.columns([2, 2, 1])
                new_status = ecols[0].selectbox("狀態", STATUSES,
                    index=STATUSES.index(a.get("status", "Open")) if a.get("status", "Open") in STATUSES else 0,
                    key=f"ast_{a['id']}")
                new_risk = ecols[1].selectbox("風險等級", RISK_LEVELS,
                    index=RISK_LEVELS.index(a.get("risk_level", "Medium")) if a.get("risk_level", "Medium") in RISK_LEVELS else 2,
                    key=f"arl_{a['id']}")
                if ecols[2].button("更新", key=f"aup_{a['id']}"):
                    api.update_assumption(pid, a["id"], {"status": new_status, "risk_level": new_risk})
                    st.rerun()

                # Disprove section
                if a.get("status") == "Disproved":
                    st.error(f"已推翻：{a.get('disproved_reason', '')}")
                    if a.get("disproved_at"):
                        st.caption(f"推翻時間：{a['disproved_at']}")
                elif a.get("status") not in ("Disproved",):
                    with st.popover("標記為推翻", use_container_width=False):
                        dreason = st.text_area("推翻原因", key=f"dreason_{a['id']}", placeholder="說明為什麼此假設不成立...")
                        if st.button("確認推翻", key=f"disprove_{a['id']}") and dreason:
                            try:
                                result = api.disprove_assumption(pid, a["id"], dreason)
                                if result.get("impact_analysis"):
                                    st.warning(f"受影響工件：{len(result['impact_analysis'])} 個")
                                    for item in result["impact_analysis"]:
                                        st.write(f"- {item['type']}: {item['code']} — {item['description']}")
                                    for action in result.get("recommended_actions", []):
                                        st.info(f"建議：{action}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"操作失敗：{e}")


# --- Step 2.1: Unknown Factors ---
elif page == "Step 2.1 - 未知集合 (U)":
    st.header("未知集合 (U)")
    st.caption("假設台帳管「對/錯」，未知集合管「變/不變」——兩者搭配完整描述早期設計的不確定性。")

    CATEGORIES = ["環境", "使用者行為", "製程", "材料", "供應", "介面", "其他"]

    factors = api.list_unknown_factors(pid)
    assumptions = api.list_assumptions(pid)
    assumption_options = {f"{a['code']}: {a['content'][:40]}": a for a in assumptions}

    with st.expander("新增未知因子", expanded=not factors):
        cols = st.columns([1, 2, 1])
        uf_code = cols[0].text_input("編號", value=f"U-{len(factors)+1:03d}", key="uf_code")
        uf_name = cols[1].text_input("因子名稱", key="uf_name", placeholder="例如：負載變化")
        uf_cat = cols[2].selectbox("分類", CATEGORIES, key="uf_cat")

        cols2 = st.columns(2)
        uf_levels = cols2[0].text_input("離散水準 (逗號分隔)", key="uf_levels", placeholder="低, 中, 高")
        uf_range = cols2[1].text_input("連續範圍描述", key="uf_range", placeholder="-20°C ~ +55°C")

        uf_impact = st.text_input("影響指標", key="uf_impact", placeholder="例如：溫升, 壽命, NVH")
        selected_assumptions = st.multiselect("關聯假設", list(assumption_options.keys()), key="uf_refs")
        uf_assumption_refs = [
            {"assumption_id": assumption_options[s]["id"], "code": assumption_options[s]["code"]}
            for s in selected_assumptions
        ]

        if st.button("新增未知因子", type="primary") and uf_name:
            levels = [l.strip() for l in uf_levels.split(",") if l.strip()] if uf_levels else []
            api.create_unknown_factor(pid, {
                "code": uf_code, "name": uf_name, "category": uf_cat,
                "levels": levels, "range_desc": uf_range,
                "impact_on": uf_impact, "assumption_refs": uf_assumption_refs,
            })
            st.rerun()

    if factors:
        # Summary by category
        cat_counts = {}
        for f in factors:
            c = f.get("category", "其他")
            cat_counts[c] = cat_counts.get(c, 0) + 1
        scols = st.columns(min(len(cat_counts), 6))
        for i, (cat, cnt) in enumerate(sorted(cat_counts.items())):
            scols[i % len(scols)].metric(cat, cnt)

        st.divider()

        for f in factors:
            levels_str = ", ".join(f.get("levels", [])) if f.get("levels") else f.get("range_desc", "")
            label = f"📊 {f['code']}｜{f['name']} [{f.get('category', '')}] — {levels_str}"
            with st.expander(label):
                cols = st.columns(3)
                cols[0].write(f"**分類**：{f.get('category', '')}")
                cols[1].write(f"**水準**：{', '.join(f.get('levels', []))}")
                cols[2].write(f"**範圍**：{f.get('range_desc', '')}")

                st.write(f"**影響指標**：{f.get('impact_on', '')}")
                if f.get("assumption_refs"):
                    tags = " ".join(f"`{r.get('code', '')}`" for r in f["assumption_refs"])
                    st.markdown(f"**關聯假設**：{tags}")

                # Edit
                st.divider()
                ecols = st.columns([2, 2, 1])
                new_impact = ecols[0].text_input("更新影響指標", value=f.get("impact_on", ""), key=f"ufi_{f['id']}")
                # Build current selection for multiselect
                current_codes = {r.get("code") for r in (f.get("assumption_refs") or [])}
                current_selected = [k for k, v in assumption_options.items() if v["code"] in current_codes]
                new_selected = ecols[1].multiselect("更新關聯假設", list(assumption_options.keys()),
                    default=current_selected, key=f"ufr_{f['id']}")
                new_refs = [
                    {"assumption_id": assumption_options[s]["id"], "code": assumption_options[s]["code"]}
                    for s in new_selected
                ]
                if ecols[2].button("更新", key=f"ufu_{f['id']}"):
                    api.update_unknown_factor(pid, f["id"], {"impact_on": new_impact, "assumption_refs": new_refs})
                    st.rerun()

                if st.button("刪除", key=f"ufd_{f['id']}"):
                    api.delete_unknown_factor(pid, f["id"])
                    st.rerun()


# --- Step 2.2.2: TRIZ ---
elif page == "Step 2.2.2 - TRIZ 解法":
    st.header("TRIZ 統一求解")
    st.caption("三路徑統一求解：技術矛盾 (矩陣+40原理) / 物理矛盾 (分離原則) / Su-Field (76標準解)")

    contradictions = api.list_contradictions(pid)
    if not contradictions:
        st.info("請先在 Step 1.2 識別矛盾")
    else:
        selected_c = st.selectbox(
            "選擇矛盾",
            options=contradictions,
            format_func=lambda c: f"{c['code']}: {c['improve_param']} vs {c['worsen_param']}",
            key="triz_c_select",
        )

        if selected_c:
            st.markdown(f"**工程描述**: {selected_c['engineering_desc']}")
            if selected_c.get("physical_contradiction"):
                st.markdown(f"**物理矛盾**: {selected_c['physical_contradiction']}")

            col_solve, col_load = st.columns(2)
            do_solve = col_solve.button("統一求解", type="primary", key="triz_solve_btn")
            do_load = col_load.button("載入歷史結果", key="triz_load_btn")

            result = None
            if do_solve:
                with st.spinner("AI 正在執行三路徑統一求解（分類 → 路由 → 具體化）..."):
                    result = api.solve_triz(pid, selected_c["id"])
                st.session_state["triz_result"] = result
            elif do_load:
                try:
                    result = api.get_triz_result(pid, selected_c["id"])
                    st.session_state["triz_result"] = result
                except Exception:
                    st.warning("此矛盾尚無歷史求解結果")

            result = st.session_state.get("triz_result")

            if result:
                # Classification badges
                cls = result.get("classification", {})
                types = cls.get("types", [])
                type_labels = {"technical": "TC 技術矛盾", "physical": "PC 物理矛盾", "sufield": "SF Su-Field"}
                badge_cols = st.columns(len(types) if types else 1)
                for i, t in enumerate(types):
                    badge_cols[i].success(type_labels.get(t, t))
                if cls.get("reasoning"):
                    with st.expander("分類推理"):
                        st.write(cls["reasoning"])

                st.divider()

                # Three tabs
                tab_tc, tab_pc, tab_sf = st.tabs([
                    "Path A: 技術矛盾 (矩陣 + 40原理)",
                    "Path B: 物理矛盾 (分離原則)",
                    "Path C: Su-Field (76標準解)",
                ])

                with tab_tc:
                    tc_sols = result.get("technical_solutions", [])
                    pm = result.get("param_mapping")
                    ml = result.get("matrix_lookup")

                    if pm:
                        with st.expander("參數映射軌跡", expanded=True):
                            pcols = st.columns(2)
                            pcols[0].markdown("**改善參數**")
                            for p in pm.get("improve_params", []):
                                pcols[0].write(f"- #{p['triz_id']} {p['triz_name']} (信心: {p['confidence']})")
                            pcols[1].markdown("**惡化參數**")
                            for p in pm.get("worsen_params", []):
                                pcols[1].write(f"- #{p['triz_id']} {p['triz_name']} (信心: {p['confidence']})")

                    if ml:
                        st.info(f"矩陣查表結果 → 推薦原理: {', '.join(f'#{x}' for x in ml)}")

                    if tc_sols:
                        for s in tc_sols:
                            with st.expander(f"原理 #{s['principle_number']}: {s['principle_name']}"):
                                st.write(f"**抽象策略**: {s['abstract_strategy']}")
                                mappings = s.get("engineering_mappings", [])
                                if mappings:
                                    st.write(f"**工程對映**: {', '.join(mappings) if isinstance(mappings, list) else mappings}")
                                st.write(f"**代價**: {s.get('cost_description', '')}")
                                robust = s.get("robust_estimate", {})
                                if robust:
                                    st.write(f"**穩健性**: {json.dumps(robust, ensure_ascii=False)}")
                                st.write(f"**驗證方式**: {s.get('experiment_desc', '')}")
                    elif "technical" not in types:
                        st.info("此矛盾未被分類為技術矛盾，此路徑不適用。")
                    else:
                        st.warning("未生成技術矛盾解法（可能參數映射或矩陣查表無結果）。")

                with tab_pc:
                    sep_sols = result.get("separation_solutions", [])
                    if sep_sols:
                        for s in sep_sols:
                            with st.expander(f"{s['separation_type']}: {s['separation_name']}"):
                                st.write(f"**分離策略**: {s['strategy']}")
                                mappings = s.get("engineering_mappings", [])
                                if mappings:
                                    st.write(f"**工程對映**: {', '.join(mappings) if isinstance(mappings, list) else mappings}")
                                st.write(f"**代價**: {s.get('cost_description', '')}")
                                st.write(f"**驗證方式**: {s.get('experiment_desc', '')}")
                    elif "physical" not in types:
                        st.info("此矛盾未被分類為物理矛盾，此路徑不適用。")
                    else:
                        st.warning("未生成物理矛盾解法。")

                with tab_sf:
                    sf_sols = result.get("sufield_solutions", [])
                    sf_state = cls.get("sufield_state", "")
                    if sf_state:
                        st.info(f"Su-Field 狀態: {sf_state}")
                    if sf_sols:
                        for s in sf_sols:
                            with st.expander(f"{s['standard_code']}: {s['standard_name']}"):
                                st.write(f"**Su-Field 模型**: {s['sufield_model']}")
                                mappings = s.get("engineering_mappings", [])
                                if mappings:
                                    st.write(f"**工程對映**: {', '.join(mappings) if isinstance(mappings, list) else mappings}")
                                st.write(f"**代價**: {s.get('cost_description', '')}")
                                st.write(f"**驗證方式**: {s.get('experiment_desc', '')}")
                    elif "sufield" not in types:
                        st.info("此矛盾未被分類為 Su-Field 問題，此路徑不適用。")
                    else:
                        st.warning("未生成 Su-Field 解法。")


# --- Step 2.2.1: Anti-Anchor Sprint ---
elif page == "Step 2.2.1 - Anti-Anchor Sprint":
    st.header("Anti-Anchor Sprint (反路徑依賴)")
    st.caption("刻意打破慣性思維，產出 3 種非典型架構概念，至少 1 種與市場主流不相容。")

    if st.button("AI 產生非典型架構", type="primary"):
        with st.spinner("AI 正在產生非典型架構概念..."):
            try:
                api.anti_anchor_sprint(pid)
                st.rerun()
            except RuntimeError as e:
                st.error(str(e))

    alts = api.list_alternatives(pid)
    aa_alts = [a for a in alts if a.get("status") == "anti_anchor"]
    if aa_alts:
        for a in aa_alts:
            with st.expander(f"{a['code']}: {a['name']} [Anti-Anchor]"):
                st.write(f"**來源**: {a.get('source', '')}")
                st.write(f"**機構**: {json.dumps(a.get('mechanism', {}), ensure_ascii=False, indent=2)}")
                st.write(f"**假設**: {a.get('assumptions', [])}")
                st.write(f"**風險**: {json.dumps(a.get('risks', {}), ensure_ascii=False, indent=2)}")
                scores = a.get("robust_scores", {})
                if scores:
                    st.write(f"**Robust 預評分**: {json.dumps(scores, ensure_ascii=False)}")
    else:
        st.info("尚未產生非典型架構，請點擊上方按鈕。")


# --- Step 2.2.4: SCAMPER ---
elif page == "Step 2.2.4 - SCAMPER 變形":
    st.header("SCAMPER 變形")

    # Subsystem input with suggestions
    suggestions = api.suggest_subsystems(pid)
    if suggestions:
        subsystem_option = st.selectbox("子系統名稱", ["(自訂)"] + suggestions)
        if subsystem_option == "(自訂)":
            subsystem = st.text_input("輸入子系統名稱", placeholder="例如：馬達-減速機模組")
        else:
            subsystem = subsystem_option
    else:
        subsystem = st.text_input("子系統名稱", placeholder="例如：馬達-減速機模組")

    if st.button("AI 生成 SCAMPER 變形", type="primary") and subsystem:
        with st.spinner("AI 正在生成 SCAMPER 變形..."):
            api.generate_scamper(pid, subsystem)
        st.rerun()

    variants = api.list_scamper(pid)
    if variants:
        # Check for new contradictions
        has_new_contradictions = any(v.get("new_contradictions") for v in variants)
        if has_new_contradictions:
            st.warning("部分變形發現了新矛盾，可回饋到矛盾列表。")
            if st.button("回饋新矛盾到矛盾列表"):
                result = api.feedback_scamper_contradictions(pid)
                count = result.get("created_count", 0)
                if count > 0:
                    st.success(f"已建立 {count} 條新矛盾")
                else:
                    st.info("無新矛盾需要建立（已存在或無新發現）")

        actions = {"S": "Substitute", "C": "Combine", "A": "Adapt", "M": "Modify",
                   "P": "Put to other use", "E": "Eliminate", "R": "Rearrange"}
        for action_key, action_name in actions.items():
            group = [v for v in variants if v["action"] == action_key]
            if group:
                st.subheader(f"{action_key} - {action_name}")
                for v in group:
                    with st.expander(v["target"]):
                        st.write(f"**機構**: {v['mechanism']}")
                        st.write(f"**失效模式**: {v.get('failure_mode', '')}")
                        st.write(f"**供應風險**: {v.get('supply_risk', '')}")
                        ncs = v.get("new_contradictions", [])
                        if ncs:
                            st.warning(f"發現 {len(ncs)} 條新矛盾：")
                            for nc in ncs:
                                st.write(f"  - 改善「{nc.get('improve', '')}」vs 惡化「{nc.get('worsen', '')}」— {nc.get('engineering_desc', '')}")


# --- Step 2.2.5: Alternatives ---
elif page == "Step 2.2.5 - 方案集合":
    st.header("方案集合")

    if st.button("AI 彙整生成候選方案", type="primary"):
        with st.spinner("AI 正在彙整 TRIZ + SCAMPER 生成候選方案..."):
            api.generate_alternatives(pid)
        st.rerun()

    alts = api.list_alternatives(pid)
    if alts:
        for a in alts:
            with st.expander(f"{a['code']}: {a['name']} [{a['status']}]"):
                st.write(f"**來源**: {a.get('source', '')}")
                st.write(f"**機構**: {json.dumps(a.get('mechanism', {}), ensure_ascii=False, indent=2)}")
                st.write(f"**假設**: {a.get('assumptions', [])}")
                st.write(f"**風險**: {json.dumps(a.get('risks', {}), ensure_ascii=False, indent=2)}")


# --- Step 2.2.6: MUST ---
elif page == "Step 2.2.6 - MUST 篩選":
    st.header("MUST 篩選")

    defn = api.get_definition(pid)
    alts = api.list_alternatives(pid)

    if not defn or not alts:
        st.info("請先建立任務定義表和候選方案")
    else:
        hard_constraints = defn.get("hard_constraints", [])
        must_items = {f"M{i+1}": hc.get("name", f"M{i+1}") for i, hc in enumerate(hard_constraints)}

        if not must_items:
            st.warning("沒有 Hard Constraints 可用作 MUST 條件")
        else:
            for a in alts:
                if a["status"] in ("candidate", "must_pass", "must_fail"):
                    st.subheader(f"{a['code']}: {a['name']}")
                    results = {}
                    for code, name in must_items.items():
                        results[code] = st.checkbox(f"{code}: {name}", key=f"must_{a['id']}_{code}", value=True)
                    notes = st.text_input("備註", key=f"must_note_{a['id']}")
                    if st.button(f"評估 {a['code']}", key=f"must_eval_{a['id']}"):
                        api.evaluate_must(pid, a["id"], results, notes)
                        st.rerun()

        st.divider()
        evals = api.list_must(pid)
        if evals:
            st.subheader("篩選結果")
            for ev in evals:
                icon = "✅" if ev["overall_pass"] else "❌"
                st.write(f"{icon} {ev['alternative_id'][:8]}... — {'Pass' if ev['overall_pass'] else 'Fail'}")


# --- Gate 2.2 ---
elif page == "Gate 2.2":
    st.header("Gate 2.2 檢查")
    if st.button("執行 Gate 2.2 檢查", type="primary"):
        result = api.check_gate(pid, 2)
        st.session_state["gate2_result"] = result
    result = st.session_state.get("gate2_result")
    if result:
        for item in result["checklist"]:
            icon = "✅" if item["passed"] else "❌"
            st.write(f"{icon} {item['item']} {item.get('note', '')}")
        if result["overall_pass"]:
            st.success("Gate 2.2 通過！可進入 Phase 3: Converge")
        else:
            st.warning("Gate 2.2 未通過")


# --- Step 3.2: WANT ---
elif page == "Step 3.2 - WANT 評分":
    st.header("WANT 評分")

    # Criteria management
    criteria = api.list_want_criteria(pid)
    with st.expander("管理 WANT 條件"):
        cols = st.columns(4)
        w_code = cols[0].text_input("編號", value=f"W{len(criteria)+1}", key="w_code")
        w_name = cols[1].text_input("名稱", key="w_name")
        w_weight = cols[2].number_input("權重 (1-10)", min_value=1, max_value=10, value=5, key="w_weight")
        w_evidence = cols[3].text_input("證據類型", key="w_evidence")
        if st.button("新增 WANT 條件") and w_name:
            api.create_want_criteria(pid, {"code": w_code, "name": w_name, "weight": w_weight, "evidence_type": w_evidence})
            st.rerun()

        if criteria:
            st.write("**現有條件:**")
            for c in criteria:
                st.write(f"- {c['code']}: {c['name']} (權重: {c['weight']})")

    # Scoring
    alts = api.list_alternatives(pid)
    passed_alts = [a for a in alts if a["status"] in ("must_pass", "selected", "backup")]

    if criteria and passed_alts:
        st.subheader("評分表")
        for a in passed_alts:
            st.write(f"### {a['code']}: {a['name']}")
            existing_scores = api.list_want_scores(pid, a["id"])
            score_map = {s["criteria_id"]: s for s in existing_scores}

            for c in criteria:
                cols = st.columns([2, 1, 3])
                cols[0].write(f"{c['code']}: {c['name']} (w={c['weight']})")
                existing = score_map.get(c["id"], {})
                score = cols[1].number_input(
                    "分數", min_value=1, max_value=10,
                    value=existing.get("score", 5),
                    key=f"ws_{a['id']}_{c['id']}",
                )
                evidence = cols[2].text_input(
                    "證據",
                    value=existing.get("evidence") or "",
                    key=f"we_{a['id']}_{c['id']}",
                )
                if st.button("存", key=f"wsave_{a['id']}_{c['id']}"):
                    api.score_want(pid, {
                        "alternative_id": a["id"],
                        "criteria_id": c["id"],
                        "score": score,
                        "evidence": evidence,
                    })
                    st.rerun()
            st.divider()

        # Totals
        totals = api.get_want_totals(pid)
        if totals:
            st.subheader("加權總分")
            for alt_id, total in sorted(totals.items(), key=lambda x: -x[1]):
                alt = next((a for a in alts if a["id"] == alt_id), None)
                name = f"{alt['code']}: {alt['name']}" if alt else alt_id[:8]
                st.metric(name, total)


# --- Step 3.1: Risks ---
elif page == "Step 3.1 - 風險評估":
    st.header("風險評估")

    with st.expander("新增風險"):
        r_desc = st.text_input("描述", key="r_desc")
        cols = st.columns(4)
        r_type = cols[0].selectbox("類型", ["technical", "process", "supply", "integration", "verification", "production"])
        r_prob = cols[1].selectbox("機率", ["L", "M", "H"])
        r_sev = cols[2].selectbox("嚴重度", ["L", "M", "H"])
        r_owner = cols[3].text_input("負責人", key="r_owner")
        r_mit = st.text_area("緩解措施", key="r_mit", height=60)
        if st.button("新增風險") and r_desc:
            api.create_risk(pid, {
                "description": r_desc, "risk_type": r_type,
                "probability": r_prob, "severity": r_sev,
                "owner": r_owner, "mitigation": r_mit,
            })
            st.rerun()

    risks = api.list_risks(pid)
    if risks:
        st.subheader("風險列表")
        for r in risks:
            level_color = {"H*": "🔴", "H": "🟠", "M": "🟡", "L": "🟢"}.get(r["level"], "⚪")
            with st.expander(f"{level_color} [{r['level']}] {r['description'][:60]}"):
                st.write(f"**類型**: {r['risk_type']}")
                st.write(f"**P×S**: {r['probability']} × {r['severity']} = {r['level']}")
                st.write(f"**負責人**: {r['owner']}")
                st.write(f"**緩解措施**: {r['mitigation']}")


# --- Step 3.2: KT Decision ---
elif page == "Step 3.2 - KT 決策記錄":
    st.header("KT 決策記錄")

    decision = api.get_decision(pid)

    if st.button("AI 生成決策記錄草稿", type="primary"):
        with st.spinner("AI 正在生成 KT 決策記錄..."):
            decision = api.generate_decision(pid)
        st.rerun()

    if decision:
        st.subheader("決策聲明")
        st.info(decision.get("statement", ""))

        st.subheader("MUST 結果")
        mr = decision.get("must_results", {})
        st.write(f"**通過**: {mr.get('passed', [])}")
        st.write(f"**淘汰**: {mr.get('eliminated', [])}")

        st.subheader("WANT 總分")
        wr = decision.get("want_results", {})
        for alt, score in sorted(wr.items(), key=lambda x: -x[1] if isinstance(x[1], (int, float)) else 0):
            st.write(f"- {alt}: **{score}**")

        st.subheader("決策")
        st.success(f"**首選**: {decision.get('primary_choice', '')} — {decision.get('primary_reason', '')}")
        st.info(f"**備選**: {decision.get('backup_choice', '')} — {decision.get('backup_reason', '')}")

        st.subheader("Action Items")
        for item in decision.get("action_items", []):
            st.write(f"- [ ] {item.get('task', '')} (負責: {item.get('owner', '')}, 期限: {item.get('due', '')})")

        st.divider()
        st.subheader("簽核")
        if decision.get("signed_by"):
            st.success(f"已簽核：{decision['signed_by']} @ {decision.get('signed_at', '')}")
        else:
            signer = st.text_input("簽核人")
            if st.button("簽核") and signer:
                api.signoff_decision(pid, signer)
                st.rerun()


# --- Step 3.1.loop: Experiments ---
elif page == "Step 3.1.loop - 最小實驗":
    st.header("最小實驗計畫")

    with st.expander("新增實驗"):
        e_goal = st.text_input("目標", key="e_goal")
        e_question = st.text_input("要回答的問題", key="e_question")
        e_method = st.text_area("方法", key="e_method", height=60)
        e_success = st.text_input("成功標準", key="e_success")
        e_failure = st.text_input("失敗後行動", key="e_failure")
        if st.button("新增實驗") and e_goal:
            api.create_experiment(pid, {
                "goal": e_goal, "question": e_question, "method": e_method,
                "success_criteria": e_success, "failure_action": e_failure,
            })
            st.rerun()

    experiments = api.list_experiments(pid)
    if experiments:
        for e in experiments:
            status_icon = {"planned": "📋", "in_progress": "🔬", "completed": "✅"}.get(e["status"], "")
            with st.expander(f"{status_icon} {e['goal'][:60]}"):
                st.write(f"**問題**: {e['question']}")
                st.write(f"**方法**: {e['method']}")
                st.write(f"**狀態**: {e['status']}")
                new_status = st.selectbox("更新狀態", ["planned", "in_progress", "completed"], key=f"es_{e['id']}")
                result = st.text_area("結果", value=e.get("result") or "", key=f"er_{e['id']}")
                if st.button("更新", key=f"eu_{e['id']}"):
                    api.update_experiment(pid, e["id"], {"status": new_status, "result": result})
                    st.rerun()


# --- Gate 3.2 ---
elif page == "Gate 3.2":
    st.header("Gate 3.2 檢查")
    if st.button("執行 Gate 3.2 檢查", type="primary"):
        result = api.check_gate(pid, 3)
        st.session_state["gate3_result"] = result
    result = st.session_state.get("gate3_result")
    if result:
        for item in result["checklist"]:
            icon = "✅" if item["passed"] else "❌"
            st.write(f"{icon} {item['item']} {item.get('note', '')}")
        if result["overall_pass"]:
            st.success("Gate 3.2 通過！專案完成 🎉")
        else:
            st.warning("Gate 3.2 未通過")


# --- Export ---
elif page == "匯出報告":
    st.header("匯出報告")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Markdown 報告")
        if st.button("生成 Markdown"):
            md = api.export_markdown(pid)
            st.session_state["export_md"] = md
        if "export_md" in st.session_state:
            st.download_button("下載 Markdown", st.session_state["export_md"], file_name="report.md", mime="text/markdown")
            with st.expander("預覽"):
                st.markdown(st.session_state["export_md"])

    with col2:
        st.subheader("JSON 匯出")
        if st.button("生成 JSON"):
            data = api.export_json(pid)
            st.session_state["export_json"] = json.dumps(data, ensure_ascii=False, indent=2)
        if "export_json" in st.session_state:
            st.download_button("下載 JSON", st.session_state["export_json"], file_name="report.json", mime="application/json")
