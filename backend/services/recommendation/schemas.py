"""
schemas.py

Pydantic schemas for the AI Recommendation Engine.
"""

from typing import List
from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RecommendationReport(BaseModel):
    """
    Structured response returned by the Recommendation Engine.
    """

    title: str = Field(
        description="Short title of the recommendation."
    )

    priority: Priority = Field(
        description="Overall recommendation priority."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score."
    )

    executive_summary: str = Field(
        description="Short executive summary."
    )

    immediate_actions: List[str] = Field(
        default_factory=list
    )

    short_term_actions: List[str] = Field(
        default_factory=list
    )

    long_term_actions: List[str] = Field(
        default_factory=list
    )

    stakeholders: List[str] = Field(
        default_factory=list
    )

    business_continuity_actions: List[str] = Field(
        default_factory=list
    )

    expected_business_outcome: str = Field(
        description="Expected outcome after executing recommendations."
    )

    reasoning: List[str] = Field(
        default_factory=list,
        description="Reasons behind the recommendation."
    )