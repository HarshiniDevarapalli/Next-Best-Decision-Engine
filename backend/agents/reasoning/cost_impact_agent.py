# backend/agents/reasoning/cost_impact_agent.py

from typing import Any, Dict

from backend.agents.base_agent import BaseAgent
from backend.services.ai.cost_impact_chain import CostImpactChain


class CostImpactAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("CostImpactAgent")
        self.chain = CostImpactChain(api_key)

    def execute(
        self,
        parsed_incident: Dict[str, Any],
        recommendation_report: Dict[str, Any],
        simulation_report: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = self.chain.invoke(
            incident=parsed_incident,
            recommendation_report=recommendation_report,
            simulation_report=simulation_report,
        )

        return result.model_dump()