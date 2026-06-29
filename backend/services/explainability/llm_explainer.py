"""
llm_explainer.py

Gemini-backed Explainability Engine.
"""

from services.llm.gemini_client import GeminiClient

from services.weak_signal.schemas import WeakSignalReport
from models.risk_report import RiskReport
from services.recommendation.schemas import RecommendationReport

from .base_explainer import ExplainabilityEngine
from .prompt import SYSTEM_PROMPT, build_prompt
from .parser import ExplainabilityParser


class GeminiExplainabilityEngine(
    ExplainabilityEngine
):

    def __init__(self):

        self.client = GeminiClient()

    @property
    def engine_name(self):

        return "Gemini Explainability Engine"

    @property
    def model_version(self):

        return self.client.model

    def explain(

        self,

        weak_signal_report: WeakSignalReport,

        risk_report: RiskReport,

        recommendation_report: RecommendationReport

    ):

        try:

            raw_response = self.client.generate_json(

                system_prompt=SYSTEM_PROMPT,

                user_prompt=build_prompt(

                    weak_signal_report,

                    risk_report,

                    recommendation_report

                )

            )

        except Exception as e:

            raise RuntimeError(

                f"Explainability generation failed: {e}"

            )

        return ExplainabilityParser.parse(

            raw_response

        )