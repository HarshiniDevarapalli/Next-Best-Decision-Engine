"""
explainability_agent.py

Produces a human-readable explanation
for the generated recommendation.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult
from models.explainability import ExplainabilityReport


class ExplainabilityAgent(BaseAgent):

    @property
    def name(self):
        return "ExplainabilityAgent"

    @property
    def description(self):
        return (
            "Generates a transparent explanation "
            "for the recommendation."
        )

    def execute(self, context):

        start = time.perf_counter()

        weak_report = context.context_data.get(
            "weak_signal_report"
        )

        risk_report = context.context_data.get(
            "risk_report"
        )

        recommendation = context.context_data.get(
            "recommendation_report"
        )

        if (
            weak_report is None
            or risk_report is None
            or recommendation is None
        ):

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="Missing reasoning reports."

            )

        evidence = []
        signal_names = []
        reasons = []

        for signal in weak_report.signals:

            signal_names.append(signal.signal.value)

            reasons.append(signal.explanation)

            for e in signal.evidence:
                evidence.append(e.text)

        explanation = (
            f"The platform recommends "
            f"'{recommendation.recommendation.value}' "
            f"because the customer has an overall "
            f"{risk_report.overall_risk_level.value} "
            f"risk score of "
            f"{risk_report.overall_risk_score:.1f}. "
            f"The recommendation is supported by "
            f"{len(signal_names)} detected business "
            f"signals."
        )

        report = ExplainabilityReport(

            recommendation=recommendation.recommendation.value,

            confidence=recommendation.confidence,

            overall_risk_score=risk_report.overall_risk_score,

            overall_risk_level=risk_report.overall_risk_level.value,

            key_reasons=reasons,

            evidence=evidence,

            contributing_signals=signal_names,

            explanation=explanation

        )

        context.context_data[
            "explainability_report"
        ] = report

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        result = AgentResult(

            agent_name=self.name,

            status="SUCCESS",

            execution_time_ms=elapsed,

            message="Explainability report generated.",

            data={

                "recommendation": report.recommendation,

                "risk_level": report.overall_risk_level,

                "confidence": report.confidence

            }

        )

        context.agent_results.append(result)

        return result