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

def get_signal(self, signal_type: SignalType):
    for signal in self.signals:
        if signal.signal == signal_type:
            return signal
    return None


class SignalType(str, Enum):
    BUDGET_CONCERN = "budget_concern"
    COMPETITOR_MENTION = "competitor_mention"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    POSITIVE_SENTIMENT = "positive_sentiment"
    RENEWAL_URGENCY = "renewal_urgency"
    LOW_ADOPTION = "low_adoption"
    EXPANSION_OPPORTUNITY = "expansion_opportunity"
    EXECUTIVE_ESCALATION = "executive_escalation"


class Evidence(BaseModel):
    """
    Supporting evidence extracted from transcript.
    """

    text: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class WeakSignal(BaseModel):
    """
    Represents one business signal.
    """

    signal: SignalType

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score."
    )

    evidence: List[Evidence] = []

    explanation: Optional[str] = None


class WeakSignalReport(BaseModel):
    """
    Final structured output of Weak Signal Detector.
    """

    transcript_summary: Optional[str] = None

    signals: List[WeakSignal]

    detector_name: str

    processing_time_ms: float

    model_version: str

    metadata: dict = {}