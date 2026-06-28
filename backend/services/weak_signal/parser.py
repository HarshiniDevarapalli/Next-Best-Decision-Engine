"""
parser.py

Converts raw LLM JSON into strongly typed WeakSignalReport objects.
"""

import json
from typing import Dict, Any

from .schemas import (
    WeakSignalReport,
    WeakSignal,
    Evidence,
    SignalType,
    Severity,
)


class WeakSignalParser:

    @staticmethod
    def parse(
        response: str,
        detector_name: str,
        model_version: str,
        processing_time_ms: float
    ) -> WeakSignalReport:

        try:
            data: Dict[str, Any] = json.loads(response)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"LLM returned invalid JSON: {e}"
            )       

        signals = []

        for signal in data.get("signals", []):

            evidence_objects = []

            for evidence in signal.get("evidence", []):

                evidence_objects.append(
                    Evidence(
                        text=evidence["text"],
                        confidence=evidence["confidence"]
                    )
                )

            signals.append(

                WeakSignal(
                    signal=SignalType(signal["signal"]),
                    confidence=signal["confidence"],
                    severity=Severity(signal["severity"]),
                    explanation=signal["explanation"],
                    evidence=evidence_objects
                )

            )

        return WeakSignalReport(

            transcript_summary=data.get("summary", ""),

            detector_name=detector_name,

            model_version=model_version,

            processing_time_ms=processing_time_ms,

            signals=signals

        )