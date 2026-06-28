# backend/agents/reasoning/weak_signal_agent.py
# (Final integrated version)

from typing import Any, Dict

from backend.agents.base_agent import BaseAgent

from backend.services.ai.incident_parser import IncidentParser
from backend.services.aiweak_signal.llm_detector import LLMWeakSignalDetector


class WeakSignalAgent(BaseAgent):

    def __init__(
        self,
        rule_detector,
        api_key: str,
    ):
        super().__init__("WeakSignalAgent")

        self.rule_detector = rule_detector
        self.parser = IncidentParser(api_key)
        self.llm_detector = LLMWeakSignalDetector(api_key)

    def execute(
        self,
        incident: str,
        enterprise_context: Dict[str, Any],
        planner_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        # Parse incident
        parsed_incident = self.parser.parse(incident)

        if hasattr(parsed_incident, "model_dump"):
            parsed_incident = parsed_incident.model_dump()

        # Rule-based detection
        rule_report = self.rule_detector.detect(
            parsed_incident=parsed_incident,
            context=enterprise_context,
        )

        # LLM detection
        llm_report = self.llm_detector.detect(
            incident=incident,
            parsed_incident=parsed_incident,
            context=enterprise_context,
            planner_context=planner_context,
        )

        shadow_comparison = {
            "agreement": None,
            "differences": [],
            "recommended_output": llm_report,
        }

        return {
            "parsed_incident": parsed_incident,
            "rule_based": rule_report,
            "llm": llm_report,
            "shadow_comparison": shadow_comparison,
        }