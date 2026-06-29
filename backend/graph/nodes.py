# backend/graph/nodes.py

from backend.registry.registry import registry
from backend.graph.state import WorkflowState
from backend.agents.reasoning.human_review_agent import HumanReviewAgent
def incident_parser_node(state):
    """
    Planner has already created the execution plan.
    WeakSignalAgent owns the incident parser.
    """

    parser = registry.get_reasoning_agent(
        "WeakSignalAgent"
    ).parser

    parsed = parser.parse(state["incident"])

    if hasattr(parsed, "model_dump"):
        parsed = parsed.model_dump()

    state["parsed_incident"] = parsed

    return state


def datasource_node(state):
    """
    Execute datasource agents sequentially.
    Parallel execution is disabled to avoid concurrent
    Chroma initialization during debugging.
    """

    plan = state["execution_plan"]

    datasource_agents = plan.get("datasource_agents", [])
    execution_order = plan.get(
        "execution_order",
        datasource_agents,
    )

    context = {}

    executed = state.setdefault(
        "executed_agents",
        [],
    )
    skipped = state.setdefault(
        "skipped_agents",
        [],
    )

    for name in execution_order:

        if name not in datasource_agents:
            continue

        agent = registry.get_datasource_agent(name)

        if agent is None:
            skipped.append(name)
            continue

        context[name] = agent.execute(
            state["parsed_incident"]
        )

        executed.append(name)

    state["datasource_context"] = context

    return state


def weak_signal_node(state):

    if (
        "WeakSignalAgent"
        not in state["execution_plan"]["reasoning_agents"]
    ):
        return state

    agent = registry.get_reasoning_agent(
        "WeakSignalAgent"
    )

    result = agent.execute(
        incident=state["incident"],
        enterprise_context=state["datasource_context"],
        planner_context=state["execution_plan"],
    )

    state["parsed_incident"] = result["parsed_incident"]
    state["rule_based_report"] = result["rule_based"]
    state["llm_report"] = result["llm"]
    state["shadow_comparison"] = result["shadow_comparison"]

    return state


def risk_node(state):

    if "RiskAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("RiskAgent")

    state["risk_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        enterprise_context=state["datasource_context"],
        rule_report=state.get("rule_based_report"),
        llm_report=state.get("llm_report"),
        planner_context=state["execution_plan"],
    )

    return state


def recommendation_node(state):

    if "RecommendationAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("RecommendationAgent")

    state["recommendation_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        enterprise_context=state["datasource_context"],
        rule_report=state.get("rule_based_report"),
        llm_report=state.get("llm_report"),
        risk_report=state.get("risk_report"),
        planner_context=state["execution_plan"],
    )

    return state


def simulation_node(state):

    if "WhatIfAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("WhatIfAgent")

    state["simulation_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        datasource_context=state["datasource_context"],
        risk_report=state.get("risk_report"),
        recommendation_report=state.get("recommendation_report"),
    )

    return state


def decision_scoring_node(state):

    if "DecisionScoringAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("DecisionScoringAgent")

    state["decision_scores"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        risk_report=state.get("risk_report"),
        recommendation_report=state.get("recommendation_report"),
        simulation_report=state.get("simulation_report"),
    )

    return state


def cost_impact_node(state):

    if "CostImpactAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("CostImpactAgent")

    state["cost_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        recommendation_report=state.get("recommendation_report"),
        simulation_report=state.get("simulation_report"),
    )

    return state

def timeline_prediction_node(state):

    if "TimelinePredictionAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("TimelinePredictionAgent")

    state["timeline_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        risk_report=state.get("risk_report"),
        recommendation_report=state.get("recommendation_report"),
        simulation_report=state.get("simulation_report"),
    )

    return state


def scenario_comparison_node(state):

    if "ScenarioComparisonAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("ScenarioComparisonAgent")

    state["scenario_comparison"] = agent.execute(
        simulation_report=state.get("simulation_report"),
        decision_scores=state.get("decision_scores"),
        cost_report=state.get("cost_report"),
        timeline_report=state.get("timeline_report"),
    )

    return state


def explainability_node(state):

    if "ExplainabilityAgent" not in state["execution_plan"]["reasoning_agents"]:
        return state

    agent = registry.get_reasoning_agent("ExplainabilityAgent")

    state["explainability_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        enterprise_context=state["datasource_context"],
        rule_report=state.get("rule_based_report"),
        llm_report=state.get("llm_report"),
        risk_report=state.get("risk_report"),
        recommendation_report=state.get("recommendation_report"),
        simulation_report=state.get("simulation_report"),
        decision_scores=state.get("decision_scores"),
        cost_report=state.get("cost_report"),
        timeline_report=state.get("timeline_report"),
        scenario_comparison=state.get("scenario_comparison"),
        planner_context=state["execution_plan"],
    )

    state["response"] = {
        "planner": state["execution_plan"],
        "incident": state["parsed_incident"],
        "enterprise_context": state["datasource_context"],
        "weak_signal": {
            "rule_based": state.get("rule_based_report"),
            "llm": state.get("llm_report"),
            "shadow_comparison": state.get("shadow_comparison"),
        },
        "risk": state.get("risk_report"),
        "recommendation": state.get("recommendation_report"),
        "simulation": state.get("simulation_report"),
        "decision_scoring": state.get("decision_scores"),
        "cost_analysis": state.get("cost_report"),
        "timeline_prediction": state.get("timeline_report"),
        "scenario_comparison": state.get("scenario_comparison"),
        "explainability": state.get("explainability_report"),
        "execution_trace": {
            "executed_agents": state.get("executed_agents", []),
            "skipped_agents": state.get("skipped_agents", []),
        },
    }

    return state
def human_review_node(state: WorkflowState) -> WorkflowState:
    """
    Human-in-the-Loop review node.

    If review is not required, simply skip this node.
    During API execution, this node will be resumed after
    the reviewer submits their decision.
    """

    if not state.get("review_required", False):
        state["skipped_agents"].append("HumanReviewAgent")
        return state

    # Workflow pauses here until a human reviews the decision.
    if state.get("review_status") is None:

        state["response"] = {
            "status": "WAITING_FOR_HUMAN_REVIEW",
            "case_id": state.get("case_id"),
            "recommendation": state.get("recommendation_report"),
            "planner": state.get("execution_plan"),
            "message": "Awaiting reviewer approval before continuing.",
        }

        return state

    # Resume workflow after review submission.
    agent = HumanReviewAgent()

    state = agent.execute(
        state=state,
        reviewer=state["reviewer"],
        reviewer_role=state["reviewer_role"],
        decision=state["review_status"],
        comments=state.get("review_comments", ""),
        updated_recommendation=state.get("approved_recommendation"),
    )

    return state