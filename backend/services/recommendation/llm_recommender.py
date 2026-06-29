"""
llm_recommender.py

Gemini-backed Recommendation Engine.
"""

from services.llm.gemini_client import GeminiClient

from models.risk_report import RiskReport
from services.weak_signal.schemas import WeakSignalReport

from .base_recommender import RecommendationEngine
from .prompt import (
    SYSTEM_PROMPT,
    build_prompt
)
from .parser import RecommendationParser


class GeminiRecommendationEngine(
    RecommendationEngine
):

    def __init__(self):

        self.client = GeminiClient()

    @property
    def engine_name(self):

        return "Gemini Recommendation Engine"

    @property
    def model_version(self):

        return self.client.model

    def recommend(

        self,

        weak_signal_report: WeakSignalReport,

        risk_report: RiskReport

    ):

        raw_response = self.client.generate_json(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=build_prompt(

                weak_signal_report,

                risk_report

            )

        )

        return RecommendationParser.parse(

            raw_response

        )