"""
recommendation_agent.py

Reasoning agent responsible for generating
an AI Crisis Response Plan.

The actual recommendation generation is delegated
to a RecommendationEngine implementation.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult

from services.recommendation.base_recommender import RecommendationEngine
from services.recommendation.llm_recommender import (
    GeminiRecommendationEngine
)


class RecommendationAgent(BaseAgent):

    def __init__(

        self,

        engine: RecommendationEngine | None = None

    ):

        self.engine = engine or GeminiRecommendationEngine()

    @property
    def name(self) -> str:
        return "RecommendationAgent"

    @property
    def description(self) -> str:
        return (
            "Generates an AI-powered crisis response plan."
        )

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:

        start = time.perf_counter()

        weak_signal_report = context.context_data.get(
            "weak_signal_report"
        )

        risk_report = context.context_data.get(
            "risk_report"
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

        recommendation = self.engine.recommend(

            weak_signal_report,

            risk_report

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

            message="Recommendation generated successfully.",

            data={

                "title": recommendation.title,

                "priority": recommendation.priority.value,

                "confidence": recommendation.confidence,

                "immediate_actions": len(
                    recommendation.immediate_actions
                ),

                "stakeholders": len(
                    recommendation.stakeholders
                )

            }

        )

        context.agent_results.append(result)

        return result