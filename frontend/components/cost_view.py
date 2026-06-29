import streamlit as st
import plotly.graph_objects as go


def render_cost(cost: dict):

    st.markdown(
        '<div class="section-title">💰 Cost & ROI Analysis</div>',
        unsafe_allow_html=True,
    )

    impacts = cost.get("impacts", [])

    if impacts:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[f"Action {i+1}" for i in range(len(impacts))],
                y=[
                    i + 1
                    for i in range(len(impacts))
                ],
                text=[
                    impact["action"]
                    for impact in impacts
                ],
                textposition="outside",
                marker_color="#3b82f6",
            )
        )

        fig.update_layout(
            height=400,
            title="Recommended Actions",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="white",
            yaxis=dict(visible=False),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    for impact in impacts:

        with st.expander(impact.get("action", "Action")):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Estimated Cost",
                    impact.get(
                        "estimated_cost",
                        "-",
                    ),
                )

                st.metric(
                    "ROI",
                    impact.get(
                        "roi",
                        "-",
                    ),
                )

            with col2:

                st.write("### Operational Impact")

                st.info(
                    impact.get(
                        "operational_impact",
                        "-",
                    )
                )

                st.write("### Financial Impact")

                st.success(
                    impact.get(
                        "financial_impact",
                        "-",
                    )
                )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.success(
            f"""
Lowest Cost Option

{cost.get('lowest_cost_option', '-')}
"""
        )

    with right:

        st.info(
            f"""
Highest ROI Option

{cost.get('highest_roi_option', '-')}
"""
        )

    st.metric(
        "Analysis Confidence",
        f"{cost.get('confidence',0):.2f}",
    )