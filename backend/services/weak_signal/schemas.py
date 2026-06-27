"""
schemas.py

Pydantic models for the Weak Signal Intelligence subsystem.
These schemas are shared between the detector, parser,
WeakSignalAgent and downstream reasoning agents.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SignalType(str, Enum):

    SUPPLIER_FAILURE = "supplier_failure"

    INVENTORY_SHORTAGE = "inventory_shortage"

    PRODUCTION_DELAY = "production_delay"

    CYBERSECURITY_RISK = "cybersecurity_risk"

    REGULATORY_RISK = "regulatory_risk"

    NATURAL_DISASTER = "natural_disaster"

    SINGLE_POINT_OF_FAILURE = "single_point_of_failure"

    CONTRACT_RISK = "contract_risk"

    LEGAL_ESCALATION = "legal_escalation"

    REPUTATIONAL_RISK = "reputational_risk"


class Evidence(BaseModel):
    """
    Supporting evidence extracted from transcript.
    """

    text: str

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )


class WeakSignal(BaseModel):
    """
    Represents one detected business signal.
    """

    signal: SignalType

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score."
    )

    severity: Severity

    evidence: List[Evidence] = Field(
        default_factory=list
    )

    explanation: Optional[str] = None


class WeakSignalReport(BaseModel):
    """
    Final structured output produced by
    the Weak Signal Detector.
    """

    transcript_summary: Optional[str] = None

    signals: List[WeakSignal] = Field(
        default_factory=list
    )

    detector_name: str

    processing_time_ms: float

    model_version: str

    metadata: dict = Field(
        default_factory=dict
    )

    def get_signal(
        self,
        signal_type: SignalType
    ) -> Optional[WeakSignal]:

        for signal in self.signals:

            if signal.signal == signal_type:
                return signal

        return None