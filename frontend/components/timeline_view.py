import streamlit as st
import plotly.graph_objects as go


def render_timeline(timeline: dict):

    st.markdown(
        '<div class="section-title">📅 Recovery Timeline</div>',
        unsafe_allow_html=True,
    )

    st.metric(
        "Estimated Recovery",
        timeline.get("estimated_recovery_time", "-"),
    )

    st.divider()

    # ---------- Timeline ----------

    stages = timeline.get("stages", [])

    if stages:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(stages) + 1)),
                y=[1] * len(stages),
                mode="lines+markers+text",
                text=[
                    stage["stage"]
                    for stage in stages
                ],
                textposition="top center",
                marker=dict(
                    size=18,
                    color="#3b82f6",
                ),
                line=dict(
                    width=4,
                    color="#3b82f6",
                ),
            )
        )

        fig.update_layout(
            height=250,
            showlegend=False,
            xaxis=dict(
                visible=False,
            ),
            yaxis=dict(
                visible=False,
            ),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="white",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    # ---------- Stages ----------

    st.subheader("Recovery Milestones")

    for index, stage in enumerate(stages, start=1):

        with st.expander(
            f"Stage {index}: {stage.get('stage')}"
        ):

            st.write(
                f"**Estimated Duration:** {stage.get('estimated_duration')}"
            )

            st.success(
                stage.get("milestone", "-")
            )

    st.divider()

    # ---------- Critical Path ----------

    st.subheader("Critical Path")

    critical_path = timeline.get(
        "critical_path",
        [],
    )

    if critical_path:

        for step in critical_path:

            st.write("➡️", step)

    st.divider()

    # ---------- Blockers ----------

    st.subheader("Potential Blockers")

    blockers = timeline.get(
        "blockers",
        [],
    )

    if blockers:

        for blocker in blockers:

            st.error(blocker)

    st.metric(
        "Prediction Confidence",
        f"{timeline.get('confidence',0):.2f}",
    )