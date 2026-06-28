"""
risk_agent.py

Consumes WeakSignalReport and produces an
Operational Risk Report.
"""

import time

from agents.base_agent import BaseAgent

from models.execution_context import ExecutionContext
from models.agent_result import AgentResult
from models.risk_report import (
    RiskReport,
    RiskContribution,
    OperationalHealth,
    RiskLevel
)

from services.weak_signal.schemas import SignalType


class RiskAssessmentAgent(BaseAgent):

    SIGNAL_WEIGHTS = {

        SignalType.SUPPLIER_FAILURE: 35,

        SignalType.INVENTORY_SHORTAGE: 30,

        SignalType.PRODUCTION_DELAY: 25,

        SignalType.CYBERSECURITY_RISK: 40,

        SignalType.REGULATORY_RISK: 20,

        SignalType.NATURAL_DISASTER: 35,

        SignalType.SINGLE_POINT_OF_FAILURE: 20,

        SignalType.CONTRACT_RISK: 15,

        SignalType.LEGAL_ESCALATION: 20,

        SignalType.REPUTATIONAL_RISK: 25

    }

    @property
    def name(self):
        return "risk"

    @property
    def description(self):
        return "Evaluates enterprise operational risk."

    def execute(self, context: ExecutionContext):

        start = time.perf_counter()

        report = context.context_data.get(
            "weak_signal_report"
        )

        if report is None:

            return AgentResult(

                agent_name=self.name,

                status="FAILED",

                message="WeakSignalReport not found."

            )

        score = 0

        contributions = []

        affected_functions = set()

        for signal in report.signals:

            weight = self.SIGNAL_WEIGHTS.get(
                signal.signal,
                0
            )

            impact = weight * signal.confidence

            score += impact

            contributions.append(

                RiskContribution(

                    signal=signal.signal,

                    weight=weight,

                    confidence=signal.confidence,

                    impact_score=impact,

                    explanation=signal.explanation

                )

            )

            if signal.signal in [
                SignalType.SUPPLIER_FAILURE,
                SignalType.INVENTORY_SHORTAGE,
                SignalType.PRODUCTION_DELAY
            ]:

                affected_functions.add("Operations")

            if signal.signal == SignalType.CYBERSECURITY_RISK:

                affected_functions.add("IT")

            if signal.signal == SignalType.LEGAL_ESCALATION:

                affected_functions.add("Legal")

            if signal.signal == SignalType.REGULATORY_RISK:

                affected_functions.add("Compliance")

        score = max(0, min(score, 100))

        if score < 25:

            level = RiskLevel.LOW
            health = OperationalHealth.NORMAL

        elif score < 50:

            level = RiskLevel.MEDIUM
            health = OperationalHealth.DEGRADED

        elif score < 75:

            level = RiskLevel.HIGH
            health = OperationalHealth.CRITICAL

        else:

            level = RiskLevel.CRITICAL
            health = OperationalHealth.FAILED

        if level == RiskLevel.CRITICAL:

            business_impact = "Immediate disruption to critical business operations."

            recovery = "24-48 Hours"

        elif level == RiskLevel.HIGH:

            business_impact = "High likelihood of operational delays."

            recovery = "2-5 Days"

        elif level == RiskLevel.MEDIUM:

            business_impact = "Moderate operational impact."

            recovery = "Within 1 Week"

        else:

            business_impact = "Minimal operational impact."

            recovery = "No immediate recovery required."

        risk_report = RiskReport(

            operational_health=health,

            overall_risk_score=score,

            overall_risk_level=level,

            contributing_signals=contributions,

            recommendation_priority=level.value,

            estimated_business_impact=business_impact,

            estimated_recovery_time=recovery,

            affected_functions=sorted(list(affected_functions)),

            explanation=f"Risk calculated using {len(contributions)} operational signals."

        )

        context.context_data["risk_report"] = risk_report

        elapsed = (time.perf_counter() - start) * 1000

        result = AgentResult(

            agent_name=self.name,

            status="SUCCESS",

            execution_time_ms=elapsed,

            message="Operational risk assessment completed.",

            data={

                "risk_score": score,

                "risk_level": level.value,

                "operational_health": health.value,

                "affected_functions": sorted(list(affected_functions))

            }

        )

        return result