"""
explainability.py

Executive explainability report for the
Enterprise Crisis Intelligence Platform.
"""

from typing import List

from pydantic import BaseModel


class ExplainabilityReport(BaseModel):

    executive_summary: str

    operational_health: str

    overall_risk_score: float

    overall_risk_level: str

    key_risks: List[str]

    supporting_evidence: List[str]

    recommendation_summary: str

    affected_business_functions: List[str]

    business_impact: str

    recovery_estimate: str

    reasoning: str