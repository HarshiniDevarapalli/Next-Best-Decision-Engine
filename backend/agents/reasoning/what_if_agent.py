# backend/agents/reasoning/what_if_agent.py

from typing import Any, Dict

from backend.agents.base_agent import BaseAgent
from backend.services.ai.simulation_chain import SimulationChain


class WhatIfAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("WhatIfAgent")
        self.chain = SimulationChain(api_key)

    def execute(
        self,
        parsed_incident: Dict[str, Any],
        datasource_context: Dict[str, Any],
        risk_report: Dict[str, Any],
        recommendation_report: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = self.chain.invoke(
            incident=parsed_incident,
            datasource_context=datasource_context,
            risk_report=risk_report,
            recommendation_report=recommendation_report,
        )

        return result.model_dump()