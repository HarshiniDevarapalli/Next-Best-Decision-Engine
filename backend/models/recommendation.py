"""
recommendation.py

Structured recommendation produced by the
RecommendationAgent.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel


class RecommendationType(str, Enum):
    EXECUTIVE_REVIEW = "Executive Business Review"
    DISCOUNT = "Offer Discount"
    SUPPORT_ESCALATION = "Support Escalation"
    CUSTOMER_TRAINING = "Customer Training"
    EXPANSION = "Expansion Opportunity"
    NO_ACTION = "No Action Required"


class RecommendationReport(BaseModel):

    recommendation: RecommendationType

    confidence: float

    priority: str

    expected_business_impact: str

    reasoning: List[str]

    next_steps: List[str]