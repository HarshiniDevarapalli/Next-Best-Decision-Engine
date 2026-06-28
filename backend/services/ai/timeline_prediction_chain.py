# backend/agents/reasoning/timeline_prediction_agent.py

from typing import Any, Dict

from backend.agents.base_agent import BaseAgent
from backend.services.aitimeline_prediction_chain import TimelinePredictionChain


class TimelinePredictionAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("TimelinePredictionAgent")
        self.chain = TimelinePredictionChain(api_key)

    def execute(
        self,
        parsed_incident: Dict[str, Any],
        risk_report: Dict[str, Any],
        recommendation_report: Dict[str, Any],
        simulation_report: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = self.chain.invoke(
            incident=parsed_incident,
            risk_report=risk_report,
            recommendation_report=recommendation_report,
            simulation_report=simulation_report,
        )

        return result.model_dump()