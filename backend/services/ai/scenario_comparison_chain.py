# backend/agents/reasoning/scenario_comparison_agent.py

from typing import Any, Dict

from backend.agents.base_agent import BaseAgent
from backend.services.aiscenario_comparison_chain import (
    ScenarioComparisonChain,
)


class ScenarioComparisonAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("ScenarioComparisonAgent")
        self.chain = ScenarioComparisonChain(api_key)

    def execute(
        self,
        simulation_report: Dict[str, Any],
        decision_scores: Dict[str, Any],
        cost_report: Dict[str, Any],
        timeline_report: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = self.chain.invoke(
            simulation_report=simulation_report,
            decision_scores=decision_scores,
            cost_report=cost_report,
            timeline_report=timeline_report,
        )

        return result.model_dump()