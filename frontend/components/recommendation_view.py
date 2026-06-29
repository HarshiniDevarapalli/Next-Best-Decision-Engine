import streamlit as st


def render_recommendations(recommendation: dict):

    st.markdown(
        '<div class="section-title">🎯 AI Recommendations</div>',
        unsafe_allow_html=True,
    )

    priority = recommendation.get("priority", "Unknown")

    color = {
        "Critical": "#dc2626",
        "High": "#ea580c",
        "Medium": "#eab308",
        "Low": "#16a34a",
    }.get(priority, "#2563eb")

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:18px;
            border-radius:16px;
            margin-bottom:20px;
            color:white;
            font-size:22px;
            font-weight:bold;">
            Priority Level: {priority}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- Immediate ---------------- #

    st.subheader("🚨 Immediate Actions")

    for action in recommendation.get("immediate_actions", []):

        st.success(action)

    st.divider()

    # ---------------- Short Term ---------------- #

    st.subheader("📅 Short-Term Actions")

    for action in recommendation.get("short_term_actions", []):

        st.info(action)

    st.divider()

    # ---------------- Long Term ---------------- #

    st.subheader("🏗 Long-Term Strategy")

    for action in recommendation.get("long_term_actions", []):

        st.write("✅", action)

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("👥 Stakeholders")

        for person in recommendation.get(
            "stakeholders",
            [],
        ):
            st.write("•", person)

    with right:

        st.subheader("📢 Escalation Steps")

        for step in recommendation.get(
            "escalation_steps",
            [],
        ):
            st.warning(step)

    st.divider()

    st.subheader("🛡 Business Continuity")

    for action in recommendation.get(
        "business_continuity_actions",
        [],
    ):
        st.success(action)

    st.divider()

    st.subheader("🎯 Expected Outcomes")

    outcomes = recommendation.get(
        "expected_outcomes",
        [],
    )

    if outcomes:

        cols = st.columns(2)

        for i, outcome in enumerate(outcomes):

            with cols[i % 2]:

                st.markdown(
                    f"""
                    <div class="card">
                    ✅ {outcome}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.metric(
        "Recommendation Confidence",
        f"{recommendation.get('confidence', 0):.2f}",
    )