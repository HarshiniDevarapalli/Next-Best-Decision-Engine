import streamlit as st
import requests

from components.planner_view import render_planner
from components.risk_view import render_risk
from components.recommendation_view import render_recommendations
from components.simulation_view import render_simulation
from components.timeline_view import render_timeline
from components.cost_view import render_cost
from components.explainability_view import render_explainability


st.set_page_config(
    page_title="Enterprise Decision Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000/analyze"


def analyze(workflow, incident):

    response = requests.post(
        API_URL,
        json={
            "workflow": workflow,
            "mode": "analysis",
            "incident": incident,
        },
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


# ---------- CSS ----------

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Header ----------

st.markdown(
    """
<div class="title-card">

<h1>🧠 Enterprise Decision Intelligence Platform</h1>

<p>
AI-Powered Supply Chain Crisis Management &
Next Best Decision Engine
</p>

</div>
""",
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------

with st.sidebar:

    st.image(
        "assets/logo.png",
        use_container_width=True,
    )

    st.markdown("## Incident Configuration")

    workflow = st.selectbox(
        "Workflow",
        [
            "incident_response",
            "business_continuity",
            "supply_chain",
        ],
    )

    incident = st.text_area(
        "Incident Description",
        height=220,
        placeholder="Describe the incident...",
    )

    st.divider()

    run = st.button(
        "🚀 Run Enterprise Analysis",
        use_container_width=True,
    )

# ---------- Run ----------

if run:

    if not incident.strip():

        st.warning("Please enter an incident.")

        st.stop()

    with st.spinner("Running AI Decision Engine..."):

        result = analyze(workflow, incident)

# ---------- Top KPIs ----------

    planner = result["planner"]

    risk = result["risk"]

    recommendation = result["recommendation"]

    explainability = result["explainability"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Workflow",
        planner["workflow"],
    )

    c2.metric(
        "Confidence",
        f'{planner["confidence"]:.2f}',
    )

    c3.metric(
        "Overall Risk",
        risk["overall_risk"],
    )

    c4.metric(
        "Human Review",
        "Required"
        if planner["requires_human_review"]
        else "No",
    )

    st.divider()

# ---------- Planner ----------

    render_planner(planner)

    st.divider()

# ---------- Risk + Recommendation ----------

    left, right = st.columns([1, 1])

    with left:

        render_risk(risk)

    with right:

        render_recommendations(recommendation)

    st.divider()

# ---------- Simulation ----------

    if planner.get("what_if"):

        render_simulation(result["simulation"])

    st.divider()

# ---------- Timeline + Cost ----------

    left, right = st.columns([1, 1])

    with left:

        render_timeline(result["timeline_prediction"])

    with right:

        render_cost(result["cost_analysis"])

    st.divider()

# ---------- Explainability ----------

    render_explainability(explainability)

# ---------- Footer ----------

st.markdown(
    """
<hr>

<center>

Enterprise Decision Intelligence Platform

Built using LangGraph • Gemini • ChromaDB • Streamlit

</center>
""",
    unsafe_allow_html=True,
)