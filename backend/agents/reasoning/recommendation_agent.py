"""
recommendation_agent.py

Generates the Next Best Decision based on
the Risk Report.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult
from models.risk_report import RiskLevel
from models.recommendation import (
    RecommendationReport,
    RecommendationType,
)


class RecommendationAgent(BaseAgent):

    @property
    def name(self):
        return "RecommendationAgent"

    @property
    def description(self):
        return "Generates the Next Best Decision."

    def execute(self, context):

        start = time.perf_counter()

        risk = context.context_data.get("risk_report")

        if risk is None:

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="Risk Report not found."

            )

        if risk.overall_risk_level == RiskLevel.CRITICAL:

            recommendation = RecommendationReport(

                recommendation=RecommendationType.EXECUTIVE_REVIEW,

                confidence=0.96,

                priority="CRITICAL",

                expected_business_impact=(
                    "Prevent customer churn "
                    "through executive intervention."
                ),

                reasoning=[
                    "Critical customer health.",
                    "Multiple high-impact risk signals detected.",
                    "Immediate executive attention required."
                ],

                next_steps=[
                    "Schedule executive meeting.",
                    "Assign senior customer success manager.",
                    "Prepare recovery plan."
                ]

            )

        elif risk.overall_risk_level == RiskLevel.HIGH:

            recommendation = RecommendationReport(

                recommendation=RecommendationType.SUPPORT_ESCALATION,

                confidence=0.91,

                priority="HIGH",

                expected_business_impact=(
                    "Reduce churn risk."
                ),

                reasoning=[
                    "High overall risk score.",
                    "Customer requires proactive engagement."
                ],

                next_steps=[
                    "Escalate support case.",
                    "Review adoption metrics."
                ]

            )

        elif risk.overall_risk_level == RiskLevel.MEDIUM:

            recommendation = RecommendationReport(

                recommendation=RecommendationType.CUSTOMER_TRAINING,

                confidence=0.84,

                priority="MEDIUM",

                expected_business_impact=(
                    "Increase adoption and product engagement."
                ),

                reasoning=[
                    "Customer is stable but showing warning signs."
                ],

                next_steps=[
                    "Schedule onboarding session.",
                    "Share best practices."
                ]

            )

        else:

            recommendation = RecommendationReport(

                recommendation=RecommendationType.NO_ACTION,

                confidence=0.95,

                priority="LOW",

                expected_business_impact=(
                    "Maintain healthy relationship."
                ),

                reasoning=[
                    "Customer health is strong."
                ],

                next_steps=[
                    "Continue regular engagement."
                ]

            )

        context.context_data[
            "recommendation_report"
        ] = recommendation

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        result = AgentResult(

            agent_name=self.name,

            status="SUCCESS",

            execution_time_ms=elapsed,

            message="Recommendation generated.",

            data={

                "recommendation": recommendation.recommendation.value,

                "confidence": recommendation.confidence,

                "priority": recommendation.priority

            }

        )

        context.agent_results.append(result)

        return result