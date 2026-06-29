import streamlit as st


def render_planner(planner: dict):

    st.markdown(
        '<div class="section-title">🧠 AI Planner</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Execution Strategy")

        st.write(planner.get("execution_strategy", "-"))

        st.write("")

        st.subheader("Planner Reasoning")

        st.info(planner.get("planner_reasoning", "-"))

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.metric(
            "Confidence",
            f"{planner.get('confidence', 0):.2f}",
        )

        st.metric(
            "Human Review",
            "Required"
            if planner.get("requires_human_review")
            else "Not Required",
        )

        st.metric(
            "Shadow Mode",
            "Enabled"
            if planner.get("shadow_mode")
            else "Disabled",
        )

        st.metric(
            "What-If",
            "Enabled"
            if planner.get("what_if")
            else "Disabled",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Datasource Agents")

        for agent in planner.get("datasource_agents", []):

            st.success(f"✅ {agent}")

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Reasoning Agents")

        for agent in planner.get("reasoning_agents", []):

            st.info(f"🧠 {agent}")

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Execution Pipeline")

    execution = planner.get("execution_order", [])

    if execution:

        pipeline = " ➜ ".join(execution)

        st.code(pipeline)

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Parallel Execution Groups")

    groups = planner.get("parallel_groups", [])

    if groups:

        for index, group in enumerate(groups, start=1):

            st.markdown(f"**Parallel Group {index}**")

            cols = st.columns(len(group))

            for col, agent in zip(cols, group):

                with col:
                    st.success(agent)

    else:

        st.info("No parallel execution groups.")

    st.markdown("</div>", unsafe_allow_html=True)