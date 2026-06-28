# backend/agents/reasoning/explainability_agent.py

from typing import Dict, Any

from backend.agents.base_agent import BaseAgent
from backend.services.ai.explainability_chain import ExplainabilityChain


class ExplainabilityAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("ExplainabilityAgent")
        self.chain = ExplainabilityChain(api_key)

    # backend/agents/reasoning/explainability_agent.py
# (Update execute() signature)

def execute(
    self,
    parsed_incident: Dict[str, Any],
    enterprise_context: Dict[str, Any],
    rule_report: Dict[str, Any],
    llm_report: Dict[str, Any],
    risk_report: Dict[str, Any],
    recommendation_report: Dict[str, Any],
    simulation_report: Dict[str, Any],
    decision_scores: Dict[str, Any],
    cost_report: Dict[str, Any],
    timeline_report: Dict[str, Any],
    scenario_comparison: Dict[str, Any],
    planner_context: Dict[str, Any],
) -> Dict[str, Any]:

    weak_signal_analysis = {
        "rule_based": rule_report,
        "llm": llm_report,
    }

    result = self.chain.invoke(
        parsed_incident=parsed_incident,
        datasource_context=enterprise_context,
        weak_signal_analysis=weak_signal_analysis,
        risk_report=risk_report,
        recommendation_report=recommendation_report,
        simulation_report=simulation_report,
        decision_scores=decision_scores,
        cost_report=cost_report,
        timeline_report=timeline_report,
        scenario_comparison=scenario_comparison,
        planner_context=planner_context,
    )

    return result.model_dump()