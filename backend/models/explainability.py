"""
explainability.py

Structured explanation for the final recommendation.
"""

from typing import List
from pydantic import BaseModel


class ExplainabilityReport(BaseModel):

    recommendation: str

    confidence: float

    overall_risk_score: float

    overall_risk_level: str

    key_reasons: List[str]

    evidence: List[str]

    contributing_signals: List[str]

    explanation: str