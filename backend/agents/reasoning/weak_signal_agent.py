"""
weak_signal_agent.py

Reasoning agent responsible for detecting weak operational
signals from enterprise crisis data.
"""

import time

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult

from services.weak_signal.schemas import (
    WeakSignalReport,
    WeakSignal,
    SignalType,
    Severity,
    Evidence,
)


class WeakSignalAgent(BaseAgent):

    @property
    def name(self):
        return "weak_signal"

    @property
    def description(self):
        return "Detects weak operational signals from enterprise crisis data."

    def execute(self, context: ExecutionContext) -> AgentResult:

        start = time.perf_counter()

        # ----------------------------
        # Read outputs from datasource agents
        # ----------------------------

        supplier = context.context_data.get("supplier_contract", {})
        inventory = context.context_data.get("inventory", {})

        vendor_data = context.context_data.get("vendor", {})
        vendors = vendor_data.get("vendors", [])

        policy_data = context.context_data.get("policy", {})
        policies = policy_data.get("policies", [])

        news = context.context_data.get("news", {})

        history_data = context.context_data.get("incident_history", {})
        history = history_data.get("incident_history", [])

        detected_signals = []

        # ----------------------------
        # Supplier Contract
        # ----------------------------

        if supplier.get("penalty_clause", False):
            detected_signals.append(
                WeakSignal(
                    signal=SignalType.CONTRACT_RISK,
                    confidence=0.80,
                    severity=Severity.MEDIUM,
                    explanation="Supplier contract contains penalty clauses.",
                    evidence=[
                        Evidence(
                            text="Penalty clause exists in supplier agreement.",
                            confidence=0.80,
                        )
                    ],
                )
            )

        if supplier.get("service_level") == "High Priority":
            detected_signals.append(
                WeakSignal(
                    signal=SignalType.SUPPLIER_FAILURE,
                    confidence=0.90,
                    severity=Severity.HIGH,
                    explanation="Critical supplier supports high-priority operations.",
                    evidence=[
                        Evidence(
                            text=f"Supplier: {supplier.get('supplier')}",
                            confidence=0.90,
                        )
                    ],
                )
            )

        # ----------------------------
        # Inventory
        # ----------------------------

        if inventory.get("stock_days_remaining", 999) < 7:
            detected_signals.append(
                WeakSignal(
                    signal=SignalType.INVENTORY_SHORTAGE,
                    confidence=0.95,
                    severity=Severity.CRITICAL,
                    explanation="Inventory is below the safety threshold.",
                    evidence=[
                        Evidence(
                            text=f"{inventory.get('stock_days_remaining')} days of stock remaining.",
                            confidence=0.95,
                        )
                    ],
                )
            )

        # ----------------------------
        # Vendors
        # ----------------------------

        backup_available = any(
            vendor.get("approved_vendor") and vendor.get("capacity_available")
            for vendor in vendors
        )

        if not backup_available:
            detected_signals.append(
                WeakSignal(
                    signal=SignalType.PRODUCTION_DELAY,
                    confidence=0.85,
                    severity=Severity.HIGH,
                    explanation="No approved backup vendor with available capacity.",
                    evidence=[
                        Evidence(
                            text="No approved backup vendor available.",
                            confidence=0.85,
                        )
                    ],
                )
            )

        # ----------------------------
        # News
        # ----------------------------

        if news.get("impact", "").lower() == "critical":
            detected_signals.append(
                WeakSignal(
                    signal=SignalType.NATURAL_DISASTER,
                    confidence=0.95,
                    severity=Severity.CRITICAL,
                    explanation=news.get(
                        "headline",
                        "Critical external disruption detected.",
                    ),
                    evidence=[
                        Evidence(
                            text=news.get("summary", ""),
                            confidence=0.95,
                        )
                    ],
                )
            )

        # ----------------------------
        # Policies
        # ----------------------------

        for policy in policies:

            rule = policy.get("rule", "").lower()

            if "legal" in rule:
                detected_signals.append(
                    WeakSignal(
                        signal=SignalType.LEGAL_ESCALATION,
                        confidence=0.75,
                        severity=Severity.MEDIUM,
                        explanation="Enterprise policy requires legal escalation.",
                        evidence=[
                            Evidence(
                                text=policy["rule"],
                                confidence=0.75,
                            )
                        ],
                    )
                )
                break

        # ----------------------------
        # Historical Incidents
        # ----------------------------

        if len(history) > 0:
            detected_signals.append(
                WeakSignal(
                    signal=SignalType.REPUTATIONAL_RISK,
                    confidence=0.70,
                    severity=Severity.MEDIUM,
                    explanation="Similar operational incidents have occurred previously.",
                    evidence=[
                        Evidence(
                            text=f"{len(history)} similar historical incidents found.",
                            confidence=0.70,
                        )
                    ],
                )
            )

        # ----------------------------
        # Build Weak Signal Report
        # ----------------------------

        report = WeakSignalReport(
            transcript_summary="Enterprise crisis assessment completed.",
            signals=detected_signals,
            detector_name="RuleBasedDetector",
            processing_time_ms=(time.perf_counter() - start) * 1000,
            model_version="1.0",
            metadata={
                "workflow": "crisis_response"
            },
        )

        context.context_data["weak_signal_report"] = report

        execution_time = (time.perf_counter() - start) * 1000

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            execution_time_ms=execution_time,
            message="Weak signals detected successfully.",
            data={
                "signals_detected": len(detected_signals),
                "detector": report.detector_name,
                "model": report.model_version,
            },
        )