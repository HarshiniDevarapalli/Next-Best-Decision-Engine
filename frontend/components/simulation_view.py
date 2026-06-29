import streamlit as st
import plotly.graph_objects as go


def render_simulation(simulation: dict):

    st.markdown(
        '<div class="section-title">🔮 What-If Simulation</div>',
        unsafe_allow_html=True,
    )

    # ---------------- Baseline ---------------- #

    st.markdown("### 📌 Baseline Scenario")

    st.info(simulation.get("baseline", "-"))

    st.divider()

    # ---------------- Best & Worst ---------------- #

    left, right = st.columns(2)

    with left:

        st.markdown(
            """
<div class="success-card">
<h4>🏆 Best Scenario</h4>
</div>
""",
            unsafe_allow_html=True,
        )

        st.write(simulation.get("best_scenario", "-"))

    with right:

        st.markdown(
            """
<div class="danger-card">
<h4>⚠ Worst Scenario</h4>
</div>
""",
            unsafe_allow_html=True,
        )

        st.write(simulation.get("worst_scenario", "-"))

    st.divider()

    # ---------------- Probability Chart ---------------- #

    scenarios = simulation.get("scenarios", [])

    if scenarios:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[s["title"] for s in scenarios],
                y=[s["probability"] * 100 for s in scenarios],
                marker_color=[
                    "#16a34a",
                    "#f59e0b",
                    "#dc2626",
                ][: len(scenarios)],
            )
        )

        fig.update_layout(
            title="Scenario Probability",
            xaxis_title="Scenario",
            yaxis_title="Probability (%)",
            height=350,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="white",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- Scenario Cards ---------------- #

    st.subheader("📊 Scenario Analysis")

    for index, scenario in enumerate(scenarios, start=1):

        with st.expander(f"Scenario {index}: {scenario.get('title')}"):

            st.markdown(
                f"**Probability:** {scenario.get('probability',0)*100:.0f}%"
            )

            st.write("### Description")
            st.write(scenario.get("description", "-"))

            st.write("### Business Impact")
            st.warning(
                scenario.get("business_impact", "-")
            )

            st.write("### Operational Impact")
            st.info(
                scenario.get("operational_impact", "-")
            )

            st.write("### Recommended Action")
            st.success(
                scenario.get("recommended_action", "-")
            )

    st.divider()

    # ---------------- Assumptions ---------------- #

    with st.expander("📄 Simulation Assumptions"):

        for assumption in simulation.get(
            "assumptions",
            [],
        ):
            st.write("•", assumption)

    st.metric(
        "Simulation Confidence",
        f"{simulation.get('confidence',0):.2f}",
    )