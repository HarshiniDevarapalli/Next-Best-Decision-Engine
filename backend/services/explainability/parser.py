"""
parser.py

Converts Gemini JSON into an
ExplainabilityReport.
"""

import json

from .schemas import ExplainabilityReport


class ExplainabilityParser:

    @staticmethod
    def parse(response: str) -> ExplainabilityReport:

        data = json.loads(response)

        return ExplainabilityReport(

            executive_summary=data["executive_summary"],

            why_this_decision=data["why_this_decision"],

            confidence=data["confidence"],

            decision_trace=data.get(
                "decision_trace",
                []
            ),

            evidence=data.get(
                "evidence",
                []
            ),

            business_impact=data.get(
                "business_impact",
                ""
            ),

            recommended_next_steps=data.get(
                "recommended_next_steps",
                []
            )

        )