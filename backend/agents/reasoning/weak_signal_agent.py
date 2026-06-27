"""
weak_signal_agent.py

Reasoning agent responsible for extracting weak business
signals from customer meeting transcripts.

The actual signal detection is delegated to a WeakSignalDetector
implementation (LLM today, ML tomorrow).
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult

from services.weak_signal.base_detector import WeakSignalDetector
from services.weak_signal.llm_detector import LLMWeakSignalDetector


class WeakSignalAgent(BaseAgent):

    def __init__(
        self,
        detector: WeakSignalDetector | None = None
    ):
        self.detector = detector or LLMWeakSignalDetector()

    @property
    def name(self) -> str:
        return "WeakSignalAgent"

    @property
    def description(self) -> str:
        return (
            "Detects hidden business signals from "
            "meeting transcripts."
        )

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:

        start = time.perf_counter()

        transcript = context.context_data.get(
            "meeting_transcript"
        )

        if not transcript:

            return AgentResult(
                agent_name=self.name,
                status="FAILED",
                message="Meeting transcript not found."
            )

        # Run weak signal detection
        report = self.detector.predict(transcript)

        # Store report in shared execution context
        context.context_data["weak_signal_report"] = report

        execution_time = (
            time.perf_counter() - start
        ) * 1000

        result = AgentResult(

            agent_name=self.name,

            status="SUCCESS",

            execution_time_ms=execution_time,

            message="Weak signals extracted successfully.",

            data={

                "summary": report.transcript_summary,

                "signals_detected": len(report.signals),

                "detector": report.detector_name,

                "model": report.model_version,

                "processing_time_ms": report.processing_time_ms

            }

        )

        context.agent_results.append(result)

        return result