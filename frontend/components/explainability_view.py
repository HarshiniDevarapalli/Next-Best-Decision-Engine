import streamlit as st


def render_explainability(explainability: dict):

    st.markdown(
        '<div class="section-title">🧠 Explainability & Decision Trace</div>',
        unsafe_allow_html=True,
    )

    # ---------------- Executive Summary ---------------- #

    st.markdown("### 📄 Executive Summary")

    st.info(
        explainability.get(
            "executive_summary",
            "No summary available.",
        )
    )

    st.divider()

    # ---------------- Planner Reasoning ---------------- #

    st.markdown("### 🎯 Planner Reasoning")

    st.success(
        explainability.get(
            "planner_reasoning",
            "-",
        )
    )

    st.divider()

    # ---------------- Reasoning Steps ---------------- #

    st.markdown("### 🔍 Reasoning Steps")

    for i, step in enumerate(
        explainability.get(
            "reasoning_steps",
            [],
        ),
        start=1,
    ):
        st.write(f"**{i}.** {step}")

    st.divider()

    left, right = st.columns(2)

    # ---------------- Evidence ---------------- #

    with left:

        st.markdown("### 📚 Supporting Evidence")

        for evidence in explainability.get(
            "evidence",
            [],
        ):
            st.success(evidence)

    # ---------------- Assumptions ---------------- #

    with right:

        st.markdown("### ⚠ Assumptions")

        for assumption in explainability.get(
            "assumptions",
            [],
        ):
            st.warning(assumption)

    st.divider()

    # ---------------- Uncertainties ---------------- #

    st.markdown("### ❓ Remaining Uncertainties")

    for item in explainability.get(
        "uncertainties",
        [],
    ):
        st.error(item)

    st.divider()

    # ---------------- Data Sources ---------------- #

    with st.expander("📂 Data Sources Used"):

        for source in explainability.get(
            "datasource_evidence",
            [],
        ):
            st.write("•", source)

    st.metric(
        "Overall Confidence",
        f"{explainability.get('confidence',0):.2f}",
    )