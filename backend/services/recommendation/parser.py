"""
parser.py

Converts Gemini JSON responses into a
RecommendationReport.
"""

import json

from .schemas import (
    RecommendationReport,
    Priority
)


class RecommendationParser:

    @staticmethod
    def parse(response: str) -> RecommendationReport:

        data = json.loads(response)

        return RecommendationReport(

            title=data["title"],

            priority=Priority(data["priority"]),

            confidence=data["confidence"],

            executive_summary=data["executive_summary"],

            immediate_actions=data.get(
                "immediate_actions",
                []
            ),

            short_term_actions=data.get(
                "short_term_actions",
                []
            ),

            long_term_actions=data.get(
                "long_term_actions",
                []
            ),

            stakeholders=data.get(
                "stakeholders",
                []
            ),

            business_continuity_actions=data.get(
                "business_continuity_actions",
                []
            ),

            expected_business_outcome=data.get(
                "expected_business_outcome",
                ""
            ),

            reasoning=data.get(
                "reasoning",
                []
            )

        )