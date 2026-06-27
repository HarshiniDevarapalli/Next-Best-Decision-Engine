"""
risk_report.py

Structured output produced by the
Operational Risk Assessment Agent.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from services.weak_signal.schemas import SignalType


class OperationalHealth(str, Enum):
    NORMAL = "NORMAL"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    FAILED = "FAILED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskContribution(BaseModel):
    """
    Describes how a detected signal contributed
    to the overall operational risk score.
    """

    signal: SignalType

    weight: float

    confidence: float

    impact_score: float

    explanation: str


class RiskReport(BaseModel):
    """
    Final output of the Operational Risk Assessment Agent.
    """

    operational_health: OperationalHealth

    overall_risk_score: float = Field(
        ge=0,
        le=100
    )

    overall_risk_level: RiskLevel

    contributing_signals: List[RiskContribution]


    estimated_business_impact: str

    estimated_recovery_time: str

    affected_functions: List[str]

    recommendation_priority: str

    explanation: str