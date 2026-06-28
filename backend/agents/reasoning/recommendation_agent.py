"""
recommendation_agent.py

Generates an enterprise Crisis Response Plan.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult
from models.recommendation import (
    RecommendationReport,
    Priority
)
from models.risk_report import RiskLevel


class RecommendationAgent(BaseAgent):

    @property
    def name(self):
        return "recommendation"

    @property
    def description(self):
        return "Generates an enterprise crisis response plan."

    def execute(self, context):

        start = time.perf_counter()

        risk = context.context_data.get("risk_report")

        if risk is None:

            return AgentResult(
                agent_name=self.name,
                status="FAILED",
                message="Risk report not found."
            )

        if risk.overall_risk_level == RiskLevel.CRITICAL:

            report = RecommendationReport(

                title="Activate Enterprise Crisis Response",

                priority=Priority.CRITICAL,

                confidence=0.97,

                summary="Critical operational disruption detected requiring immediate intervention.",

                immediate_actions=[

                    "Activate approved backup supplier.",

                    "Notify executive crisis committee.",

                    "Escalate to procurement leadership.",

                    "Freeze non-essential procurement changes."

                ],

                short_term_actions=[

                    "Validate inventory availability.",

                    "Review supplier contracts.",

                    "Coordinate with logistics."

                ],

                long_term_actions=[

                    "Diversify supplier network.",

                    "Reduce single points of failure.",

                    "Update business continuity strategy."

                ],

                stakeholders_to_notify=[

                    "CEO",

                    "COO",

                    "Procurement",

                    "Legal",

                    "Operations"

                ],

                business_continuity_actions=[

                    "Activate Business Continuity Plan.",

                    "Monitor recovery dashboard.",

                    "Schedule crisis review every 4 hours."

                ],

                expected_business_outcome="Production downtime minimized through rapid supplier transition."

            )

        elif risk.overall_risk_level == RiskLevel.HIGH:

            report = RecommendationReport(

                title="High Risk Operational Response",

                priority=Priority.HIGH,

                confidence=0.93,

                summary="High operational risk requiring coordinated response.",

                immediate_actions=[
                    "Notify procurement.",
                    "Identify backup vendors."
                ],

                short_term_actions=[
                    "Review inventory.",
                    "Assess downstream impact."
                ],

                long_term_actions=[
                    "Strengthen supplier resilience."
                ],

                stakeholders_to_notify=[
                    "Operations",
                    "Procurement"
                ],

                business_continuity_actions=[
                    "Increase monitoring."
                ],

                expected_business_outcome="Reduce likelihood of operational disruption."

            )

        elif risk.overall_risk_level == RiskLevel.MEDIUM:

            report = RecommendationReport(

                title="Preventive Risk Mitigation",

                priority=Priority.MEDIUM,

                confidence=0.89,

                summary="Operational risks detected but currently manageable.",

                immediate_actions=[
                    "Monitor affected systems."
                ],

                short_term_actions=[
                    "Review contingency plans."
                ],

                long_term_actions=[
                    "Conduct resilience assessment."
                ],

                stakeholders_to_notify=[
                    "Operations Manager"
                ],

                business_continuity_actions=[
                    "Maintain readiness."
                ],

                expected_business_outcome="Prevent escalation."

            )

        else:

            report = RecommendationReport(

                title="Normal Operations",

                priority=Priority.LOW,

                confidence=0.98,

                summary="No significant operational risks detected.",

                immediate_actions=[],

                short_term_actions=[],

                long_term_actions=[],

                stakeholders_to_notify=[],

                business_continuity_actions=[],

                expected_business_outcome="Continue normal business operations."

            )

        context.context_data["recommendation_report"] = report

        elapsed = (time.perf_counter() - start) * 1000

        result = AgentResult(

            agent_name=self.name,

            status="SUCCESS",

            execution_time_ms=elapsed,

            message="Crisis response plan generated.",

            data={

                "title": report.title,

                "priority": report.priority.value,

                "confidence": report.confidence

            }

        )

        return result