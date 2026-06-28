# backend/agents/reasoning/risk_agent.py
# (Final integrated version)

from typing import Any, Dict

from backend.agents.base_agent import BaseAgent
from backend.services.ai.risk_chain import RiskChain


class RiskAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("RiskAgent")
        self.chain = RiskChain(api_key)

    def execute(
        self,
        parsed_incident: Dict[str, Any],
        enterprise_context: Dict[str, Any],
        rule_report: Dict[str, Any],
        llm_report: Dict[str, Any],
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
            planner_context=planner_context,
        )

        return result.model_dump()