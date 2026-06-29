from typing import Any, Dict

from backend.agents.base_agent import BaseAgent
from backend.services.ai.timeline_prediction_chain import TimelinePredictionChain


class TimelinePredictionAgent(BaseAgent):
    """
    Predicts the enterprise recovery timeline.
    """

    def __init__(self, api_key: str):
        super().__init__(
            "TimelinePredictionAgent",
            "Predicts recovery timeline and milestones."
        )

        self.chain = TimelinePredictionChain(api_key)

    def execute(
        self,
        *,
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

        if hasattr(result, "model_dump"):
            return result.model_dump()

        return result