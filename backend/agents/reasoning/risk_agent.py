"""
risk_agent.py

Consumes WeakSignalReport and produces
an enterprise RiskReport.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult
from models.risk_report import (
    RiskReport,
    RiskLevel,
    CustomerHealth,
    RiskContribution,
)

from services.weak_signal.schemas import SignalType


class RiskAssessmentAgent(BaseAgent):

    SIGNAL_WEIGHTS = {

        SignalType.BUDGET_CONCERN: 30,

        SignalType.COMPETITOR_MENTION: 25,

        SignalType.NEGATIVE_SENTIMENT: 15,

        SignalType.RENEWAL_URGENCY: 20,

        SignalType.LOW_ADOPTION: 25,

        SignalType.EXECUTIVE_ESCALATION: 35,

        SignalType.EXPANSION_OPPORTUNITY: -20,

        SignalType.POSITIVE_SENTIMENT: -10,

    }

    @property
    def name(self):

        return "RiskAssessmentAgent"

    @property
    def description(self):

        return "Calculates business risk from detected weak signals."

    def execute(self, context):

        start = time.perf_counter()

        report = context.context_data.get(
            "weak_signal_report"
        )

        if report is None:

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="Weak Signal Report missing."

            )

        contributions = []

        score = 0

        for signal in report.signals:

            weight = self.SIGNAL_WEIGHTS.get(
                signal.signal,
                0
            )

            impact = weight * signal.confidence

            score += impact

            contributions.append(

                RiskContribution(

                    signal=signal.signal,

                    weight=weight,

                    confidence=signal.confidence,

                    impact_score=impact,

                    explanation=signal.explanation

                )

            )

        score = max(0, min(100, score))

        if score < 25:

            level = RiskLevel.LOW
            health = CustomerHealth.HEALTHY

        elif score < 50:

            level = RiskLevel.MEDIUM
            health = CustomerHealth.STABLE

        elif score < 75:

            level = RiskLevel.HIGH
            health = CustomerHealth.AT_RISK

        else:

            level = RiskLevel.CRITICAL
            health = CustomerHealth.CRITICAL

        risk_report = RiskReport(

            customer_health=health,

            overall_risk_score=score,

            overall_risk_level=level,

            contributing_signals=contributions,

            recommendation_priority=level.value,

            explanation=f"Calculated from {len(contributions)} business signals."

        )

        context.context_data["risk_report"] = risk_report

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        result = AgentResult(

            agent_name=self.name,

            status="SUCCESS",

            execution_time_ms=elapsed,

            message="Risk assessment completed.",

            data={

                "risk_score": score,

                "risk_level": level.value,

                "customer_health": health.value

            }

        )

        context.agent_results.append(result)

        return result