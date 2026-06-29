"""
schemas.py

Pydantic schemas for the AI Explainability Engine.
"""

from typing import List

from pydantic import BaseModel, Field


class ExplainabilityReport(BaseModel):
    """
    Structured explainability report returned by the
    Explainability Engine.
    """

    executive_summary: str = Field(
        description="High-level executive summary."
    )

    why_this_decision: str = Field(
        description="Explanation of why this recommendation was generated."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence in the explanation."
    )

    decision_trace: List[str] = Field(
        default_factory=list,
        description="Step-by-step reasoning process."
    )

    evidence: List[str] = Field(
        default_factory=list,
        description="Evidence supporting the reasoning."
    )

    business_impact: str = Field(
        description="Expected operational/business impact."
    )

    recommended_next_steps: List[str] = Field(
        default_factory=list,
        description="Immediate next steps for executives."
    )