# backend/graph/nodes.py

from backend.registry.registry import registry


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

    agent = registry.get_reasoning_agent(
        "RiskAgent"
    )

    state["risk_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        enterprise_context=state["datasource_context"],
        rule_report=state["rule_based_report"],
        llm_report=state["llm_report"],
        planner_context=state["execution_plan"],
    )

    return state


def recommendation_node(state):

    agent = registry.get_reasoning_agent(
        "RecommendationAgent"
    )

    state["recommendation_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        enterprise_context=state["datasource_context"],
        rule_report=state["rule_based_report"],
        llm_report=state["llm_report"],
        risk_report=state["risk_report"],
        planner_context=state["execution_plan"],
    )

    return state


def simulation_node(state):

    agent = registry.get_reasoning_agent(
        "WhatIfAgent"
    )

    state["simulation_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        datasource_context=state["datasource_context"],
        risk_report=state["risk_report"],
        recommendation_report=state["recommendation_report"],
    )

    return state


def decision_scoring_node(state):

    agent = registry.get_reasoning_agent(
        "DecisionScoringAgent"
    )

    state["decision_scores"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        risk_report=state["risk_report"],
        recommendation_report=state["recommendation_report"],
        simulation_report=state["simulation_report"],
    )

    return state


def cost_impact_node(state):

    agent = registry.get_reasoning_agent(
        "CostImpactAgent"
    )

    state["cost_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        recommendation_report=state["recommendation_report"],
        simulation_report=state["simulation_report"],
    )

    return state


def timeline_prediction_node(state):

    agent = registry.get_reasoning_agent(
        "TimelinePredictionAgent"
    )

    state["timeline_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        risk_report=state["risk_report"],
        recommendation_report=state["recommendation_report"],
        simulation_report=state["simulation_report"],
    )

    return state


def scenario_comparison_node(state):

    agent = registry.get_reasoning_agent(
        "ScenarioComparisonAgent"
    )

    state["scenario_comparison"] = agent.execute(
        simulation_report=state["simulation_report"],
        decision_scores=state["decision_scores"],
        cost_report=state["cost_report"],
        timeline_report=state["timeline_report"],
    )

    return state


def explainability_node(state):

    agent = registry.get_reasoning_agent(
        "ExplainabilityAgent"
    )

    state["explainability_report"] = agent.execute(
        parsed_incident=state["parsed_incident"],
        enterprise_context=state["datasource_context"],
        rule_report=state["rule_based_report"],
        llm_report=state["llm_report"],
        risk_report=state["risk_report"],
        recommendation_report=state["recommendation_report"],
        simulation_report=state["simulation_report"],
        decision_scores=state["decision_scores"],
        cost_report=state["cost_report"],
        timeline_report=state["timeline_report"],
        scenario_comparison=state["scenario_comparison"],
        planner_context=state["execution_plan"],
    )

    state["response"] = {
        "planner": state["execution_plan"],
        "incident": state["parsed_incident"],
        "enterprise_context": state["datasource_context"],
        "weak_signal": {
            "rule_based": state["rule_based_report"],
            "llm": state["llm_report"],
            "shadow_comparison": state["shadow_comparison"],
        },
        "risk": state["risk_report"],
        "recommendation": state["recommendation_report"],
        "simulation": state["simulation_report"],
        "decision_scoring": state["decision_scores"],
        "cost_analysis": state["cost_report"],
        "timeline_prediction": state["timeline_report"],
        "scenario_comparison": state["scenario_comparison"],
        "explainability": state["explainability_report"],
        "execution_trace": {
            "executed_agents": state["executed_agents"],
            "skipped_agents": state["skipped_agents"],
        },
    }

    return state