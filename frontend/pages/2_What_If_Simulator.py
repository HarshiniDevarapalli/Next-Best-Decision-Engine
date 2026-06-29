import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="What-If Simulator",
    page_icon="🔮",
    layout="wide",
)

API_URL = "http://localhost:8000/simulate"

st.title("🔮 AI What-If Simulator")
st.caption("Modify business conditions and compare predicted outcomes.")

# --------------------------------------------------------
# Sidebar
# --------------------------------------------------------

with st.sidebar:

    st.header("Simulation Parameters")

    supplier_delay = st.slider(
        "Supplier Delay (Days)",
        0,
        30,
        14,
    )

    inventory_days = st.slider(
        "Inventory Remaining (Days)",
        0,
        30,
        5,
    )

    lead_time = st.slider(
        "Backup Supplier Lead Time",
        1,
        20,
        6,
    )

    cost_increase = st.slider(
        "Cost Increase (%)",
        0,
        50,
        8,
    )

    backup_supplier = st.checkbox(
        "Backup Supplier Available",
        True,
    )

    expedited_shipping = st.checkbox(
        "Enable Expedited Shipping",
        True,
    )

    simulate = st.button(
        "🚀 Run Simulation",
        use_container_width=True,
    )

# --------------------------------------------------------
# API
# --------------------------------------------------------

def run_simulation(payload):

    response = requests.post(
        API_URL,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()

    return response.json()

# --------------------------------------------------------
# Execute
# --------------------------------------------------------

if simulate:

    payload = {

        "supplier_delay_days": supplier_delay,

        "inventory_days_remaining": inventory_days,

        "backup_supplier_available": backup_supplier,

        "backup_supplier_lead_time": lead_time,

        "estimated_cost_increase": cost_increase,

        "expedited_shipping": expedited_shipping,
    }

    with st.spinner("Running AI Simulation..."):

        result = run_simulation(payload)

    st.success("Simulation Complete")

    # ----------------------------------------------------
    # KPI Cards
    # ----------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Best Scenario",
        result["best_scenario"],
    )

    c2.metric(
        "Worst Scenario",
        result["worst_scenario"],
    )

    c3.metric(
        "Confidence",
        f"{result['confidence']:.2f}",
    )

    st.divider()

    # ----------------------------------------------------
    # Probability Chart
    # ----------------------------------------------------

    scenarios = result.get("scenarios", [])

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=[s["title"] for s in scenarios],

            y=[s["probability"] * 100 for s in scenarios],

            marker_color=[
                "#22c55e",
                "#f59e0b",
                "#ef4444",
            ][: len(scenarios)],
        )
    )

    fig.update_layout(

        title="Scenario Probability",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font_color="white",

        height=420,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # ----------------------------------------------------
    # Scenario Cards
    # ----------------------------------------------------

    for scenario in scenarios:

        with st.expander(
            scenario["title"],
            expanded=False,
        ):

            st.markdown(
                f"### Probability: {scenario['probability']*100:.0f}%"
            )

            st.write(scenario["description"])

            left, right = st.columns(2)

            with left:

                st.subheader("Business Impact")

                st.warning(
                    scenario["business_impact"]
                )

            with right:

                st.subheader("Operational Impact")

                st.info(
                    scenario["operational_impact"]
                )

            st.subheader("Recommended Action")

            st.success(
                scenario["recommended_action"]
            )

    st.divider()

    st.subheader("Simulation Assumptions")

    for assumption in result.get(
        "assumptions",
        [],
    ):

        st.write("•", assumption)