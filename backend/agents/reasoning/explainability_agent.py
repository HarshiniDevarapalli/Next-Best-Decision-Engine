"""
explainability_agent.py

Reasoning agent responsible for generating
an executive AI explanation.

The actual explanation generation is delegated
to an ExplainabilityEngine implementation.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult

from services.explainability.base_explainer import (
    ExplainabilityEngine
)

from services.explainability.llm_explainer import (
    GeminiExplainabilityEngine
)


class ExplainabilityAgent(BaseAgent):

    def __init__(

        self,

        engine: ExplainabilityEngine | None = None

    ):

        self.engine = engine or GeminiExplainabilityEngine()

    @property
    def name(self):

        return "ExplainabilityAgent"

    @property
    def description(self):

        return (

            "Generates executive AI explanations "

            "for crisis response decisions."

        )

    def execute(

        self,

        context: ExecutionContext

    ):

        start = time.perf_counter()

        weak_signal_report = context.context_data.get(
            "weak_signal_report"
        )

        risk_report = context.context_data.get(
            "risk_report"
        )

        recommendation_report = context.context_data.get(
            "recommendation_report"
        )

        if weak_signal_report is None:

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="WeakSignalReport not found."

            )

        if risk_report is None:

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="RiskReport not found."

            )

        if recommendation_report is None:

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="RecommendationReport not found."

            )

        report = self.engine.explain(

            weak_signal_report,

            risk_report,

            recommendation_report

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

            message="Executive explanation generated successfully.",

            data={

                "confidence": report.confidence,

                "decision_steps": len(

                    report.decision_trace

                ),

                "evidence_items": len(

                    report.evidence

                )

            }

        )

        context.agent_results.append(result)

        return result