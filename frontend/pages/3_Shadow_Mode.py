import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Shadow Mode",
    page_icon="🌗",
    layout="wide",
)

st.title("🌗 Shadow Mode")
st.caption("Compare AI recommendations against current human decisions without affecting operations.")

st.markdown("---")

# ----------------------------------------------------
# Demo Data (replace with backend API later)
# ----------------------------------------------------

ai = {
    "decision": "Activate Backup Supplier B",
    "risk": "Medium",
    "cost": "$185,000",
    "timeline": "6 Days",
    "confidence": 0.94,
}

human = {
    "decision": "Wait for Primary Supplier",
    "risk": "High",
    "cost": "$420,000",
    "timeline": "14 Days",
    "confidence": 0.72,
}

agreement = 62

# ----------------------------------------------------
# Top Metrics
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Agreement Score", f"{agreement}%")
c2.metric("AI Confidence", f"{ai['confidence']:.2f}")
c3.metric("Human Confidence", f"{human['confidence']:.2f}")
c4.metric("Recommended Decision", "AI")

st.divider()

# ----------------------------------------------------
# Side-by-side Comparison
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🤖 AI Recommendation")

    st.success(ai["decision"])

    st.metric("Risk", ai["risk"])
    st.metric("Cost", ai["cost"])
    st.metric("Recovery", ai["timeline"])

with right:

    st.subheader("👤 Human Decision")

    st.warning(human["decision"])

    st.metric("Risk", human["risk"])
    st.metric("Cost", human["cost"])
    st.metric("Recovery", human["timeline"])

st.divider()

# ----------------------------------------------------
# Confidence Comparison
# ----------------------------------------------------

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=["AI", "Human"],
        y=[
            ai["confidence"] * 100,
            human["confidence"] * 100,
        ],
        marker_color=["#2563eb", "#f59e0b"],
    )
)

fig.update_layout(
    title="Decision Confidence",
    height=350,
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

# ----------------------------------------------------
# Difference Analysis
# ----------------------------------------------------

st.subheader("🔍 Difference Analysis")

comparison = [
    ("Supplier Strategy", "Backup Supplier", "Wait"),
    ("Operational Risk", "Medium", "High"),
    ("Recovery Time", "6 Days", "14 Days"),
    ("Estimated Cost", "$185K", "$420K"),
]

for title, ai_value, human_value in comparison:

    c1, c2, c3 = st.columns([2, 2, 2])

    c1.write(f"**{title}**")
    c2.success(ai_value)
    c3.warning(human_value)

st.divider()

st.subheader("🧠 AI Explanation")

st.info(
    """
The AI selected the backup supplier because it reduces downtime,
minimizes operational risk, and lowers overall recovery cost despite
a higher procurement expense.
"""
)

st.subheader("📌 Recommendation")

st.success(
    "Deploy Backup Supplier B and activate expedited logistics."
)