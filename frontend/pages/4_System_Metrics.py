import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="System Metrics",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Enterprise System Metrics")
st.caption("Monitor AI workflow execution, agent performance, and platform health.")

# --------------------------------------------------
# Demo Data (replace with backend API)
# --------------------------------------------------

metrics = {
    "runtime": 8.42,
    "api_latency": 1.31,
    "llm_calls": 9,
    "rag_queries": 6,
    "confidence": 0.93,
    "planner_agents": 11,
    "parallel_groups": 2,
    "success_rate": 99.2,
}

executed_agents = [
    "IncidentParser",
    "DatasourceAgent",
    "WeakSignalAgent",
    "RiskAgent",
    "RecommendationAgent",
    "WhatIfAgent",
    "DecisionScoringAgent",
    "CostImpactAgent",
    "TimelinePredictionAgent",
    "ScenarioComparisonAgent",
    "ExplainabilityAgent",
]

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Runtime", f"{metrics['runtime']} sec")
c2.metric("API Latency", f"{metrics['api_latency']} sec")
c3.metric("LLM Calls", metrics["llm_calls"])
c4.metric("RAG Queries", metrics["rag_queries"])

c5, c6, c7, c8 = st.columns(4)

c5.metric("Planner Agents", metrics["planner_agents"])
c6.metric("Parallel Groups", metrics["parallel_groups"])
c7.metric("Confidence", f"{metrics['confidence']:.2f}")
c8.metric("Success Rate", f"{metrics['success_rate']}%")

st.divider()

# --------------------------------------------------
# Confidence Gauge
# --------------------------------------------------

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=metrics["confidence"] * 100,
        number={"suffix": "%"},
        title={"text": "Overall Confidence"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#3b82f6"},
            "steps": [
                {"range": [0, 50], "color": "#ef4444"},
                {"range": [50, 75], "color": "#f59e0b"},
                {"range": [75, 100], "color": "#22c55e"},
            ],
        },
    )
)

fig.update_layout(
    height=330,
    paper_bgcolor="#0f172a",
    font_color="white",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Execution Timeline
# --------------------------------------------------

timeline = pd.DataFrame(
    {
        "Agent": executed_agents,
        "Execution Time (s)": [
            0.4,
            0.8,
            0.5,
            0.9,
            1.1,
            1.2,
            0.7,
            0.6,
            0.8,
            0.5,
            0.4,
        ],
    }
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=timeline["Execution Time (s)"],
        y=timeline["Agent"],
        orientation="h",
        marker_color="#2563eb",
    )
)

fig.update_layout(
    title="Agent Execution Timeline",
    height=500,
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Execution Trace
# --------------------------------------------------

st.subheader("🔄 Workflow Execution Trace")

for i, agent in enumerate(executed_agents, start=1):
    st.success(f"{i}. {agent}")

st.divider()

# --------------------------------------------------
# Parallel Execution
# --------------------------------------------------

st.subheader("⚡ Parallel Execution Groups")

group1, group2 = st.columns(2)

with group1:
    st.info(
        """
Group 1

• InventoryAgent

• VendorAgent

• PolicyAgent
"""
    )

with group2:
    st.info(
        """
Group 2

• NewsAgent

• IncidentHistoryAgent
"""
    )

st.divider()

# --------------------------------------------------
# Resource Usage
# --------------------------------------------------

usage = pd.DataFrame(
    {
        "Metric": [
            "CPU",
            "Memory",
            "GPU",
            "Network",
        ],
        "Usage": [
            42,
            61,
            18,
            33,
        ],
    }
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=usage["Metric"],
        y=usage["Usage"],
        marker_color=[
            "#2563eb",
            "#22c55e",
            "#f59e0b",
            "#ef4444",
        ],
    )
)

fig.update_layout(
    title="Resource Utilization (%)",
    height=350,
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# System Health
# --------------------------------------------------

st.subheader("🟢 Platform Health")

st.success("✓ Planner Operational")
st.success("✓ LangGraph Workflow Active")
st.success("✓ Vector Database Connected")
st.success("✓ Gemini API Reachable")
st.success("✓ AI Agents Healthy")
st.success("✓ Explainability Service Active")
st.success("✓ Shadow Mode Ready")
st.success("✓ Human Review Pipeline Ready")