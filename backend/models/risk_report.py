"""
risk_report.py

Structured output produced by the RiskAssessmentAgent.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from services.weak_signal.schemas import SignalType


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CustomerHealth(str, Enum):
    HEALTHY = "HEALTHY"
    STABLE = "STABLE"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"


class RiskContribution(BaseModel):

    signal: SignalType

    weight: float

    confidence: float

    impact_score: float

    explanation: str


class RiskReport(BaseModel):

    customer_health: CustomerHealth

    overall_risk_score: float = Field(
        ge=0,
        le=100
    )

    overall_risk_level: RiskLevel

    contributing_signals: List[RiskContribution]

    recommendation_priority: str

    explanation: str