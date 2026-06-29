import streamlit as st
import plotly.graph_objects as go


RISK_SCORE = {
    "Low": 20,
    "Medium": 45,
    "Medium-Low": 35,
    "Medium-High": 65,
    "High": 85,
    "Critical": 100,
}


def render_risk(risk: dict):

    st.markdown(
        '<div class="section-title">⚠️ Enterprise Risk Assessment</div>',
        unsafe_allow_html=True,
    )

    score = RISK_SCORE.get(
        risk.get("overall_risk", "Low"),
        0,
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%"},
            title={"text": "Overall Risk"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#ef4444"},
                "steps": [
                    {"range": [0, 25], "color": "#16a34a"},
                    {"range": [25, 50], "color": "#facc15"},
                    {"range": [50, 75], "color": "#fb923c"},
                    {"range": [75, 100], "color": "#dc2626"},
                ],
            },
        )
    )

    gauge.update_layout(
        height=320,
        paper_bgcolor="#0f172a",
        font_color="white",
    )

    left, right = st.columns([1, 1.3])

    with left:
        st.plotly_chart(
            gauge,
            use_container_width=True,
        )

    with right:

        metrics = [
            ("Supplier", risk.get("supplier_risk")),
            ("Vendor", risk.get("vendor_risk")),
            ("Inventory", risk.get("inventory_risk")),
            ("Logistics", risk.get("logistics_risk")),
            ("Contract", risk.get("contractual_risk")),
            ("Operations", risk.get("operational_impact")),
            ("Financial", risk.get("financial_impact")),
            ("Compliance", risk.get("compliance_impact")),
            ("Reputation", risk.get("reputational_impact")),
        ]

        c1, c2 = st.columns(2)

        for i, (title, value) in enumerate(metrics):

            column = c1 if i % 2 == 0 else c2

            with column:
                st.metric(title, value or "-")

    st.markdown("---")

    st.subheader("🚨 Key Risks")

    for item in risk.get("key_risks", []):

        st.error(item)

    with st.expander("📄 Supporting Evidence"):

        for evidence in risk.get(
            "supporting_evidence",
            [],
        ):
            st.write("•", evidence)

    with st.expander("🧠 AI Reasoning"):

        st.write(risk.get("reasoning", ""))

    st.metric(
        "Confidence",
        f"{risk.get('confidence', 0):.2f}",
    )