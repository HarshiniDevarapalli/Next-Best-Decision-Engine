# backend/graph/workflow_graph.py
# (Final workflow)

from langgraph.graph import END, START, StateGraph

from backend.graph.nodes import (
    incident_parser_node,
    datasource_node,
    weak_signal_node,
    risk_node,
    recommendation_node,
    simulation_node,
    decision_scoring_node,
    cost_impact_node,
    timeline_prediction_node,
    scenario_comparison_node,
    explainability_node,
)

from backend.graph.state import WorkflowState


def build_enterprise_graph():

    graph = StateGraph(WorkflowState)

    graph.add_node("incident_parser", incident_parser_node)
    graph.add_node("datasource", datasource_node)
    graph.add_node("weak_signal", weak_signal_node)
    graph.add_node("risk", risk_node)
    graph.add_node("recommendation", recommendation_node)
    graph.add_node("explainability", explainability_node)

    graph.add_edge(START, "incident_parser")
    graph.add_edge("incident_parser", "datasource")
    graph.add_edge("datasource", "weak_signal")
    graph.add_edge("weak_signal", "risk")
    graph.add_edge("risk", "recommendation")
    graph.add_edge("recommendation", "explainability")
    graph.add_edge("explainability", END)

    return graph.compile()


enterprise_workflow = build_enterprise_graph()
# backend/graph/workflow_graph.py
# (Add Phase 4 workflow)

from backend.graph.nodes import (
    incident_parser_node,
    datasource_node,
    weak_signal_node,
    risk_node,
    recommendation_node,
    simulation_node,
    decision_scoring_node,
    cost_impact_node,
    timeline_prediction_node,
    scenario_comparison_node,
    explainability_node,
)

graph.add_node("simulation", simulation_node)
graph.add_node("decision_scoring", decision_scoring_node)
graph.add_node("cost_impact", cost_impact_node)
graph.add_node("timeline_prediction", timeline_prediction_node)
graph.add_node("scenario_comparison", scenario_comparison_node)

graph.add_edge("recommendation", "simulation")
graph.add_edge("simulation", "decision_scoring")
graph.add_edge("decision_scoring", "cost_impact")
graph.add_edge("cost_impact", "timeline_prediction")
graph.add_edge("timeline_prediction", "scenario_comparison")
graph.add_edge("scenario_comparison", "explainability")