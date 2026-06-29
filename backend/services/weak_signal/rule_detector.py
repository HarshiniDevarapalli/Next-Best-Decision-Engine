# backend/services/weak_signal/rule_detector.py

from typing import Any, Dict


class RuleBasedDetector:
    """
    Rule-based weak signal detector.

    Uses simple heuristics to identify weak signals from a parsed incident.
    This acts as a baseline alongside the LLM detector.
    """

    def __init__(self):
        self.rules = {
            "supplier": "Supplier Risk",
            "vendor": "Vendor Risk",
            "delay": "Delivery Delay",
            "late": "Delivery Delay",
            "inventory": "Inventory Shortage",
            "stock": "Inventory Shortage",
            "quality": "Quality Issue",
            "defect": "Quality Issue",
            "policy": "Policy Compliance",
            "contract": "Contract Risk",
            "shipment": "Logistics Risk",
            "transport": "Logistics Risk",
        }

    def detect(
        self,
        *,
        parsed_incident: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        incident_text = str(parsed_incident).lower()

        signals = []

        for keyword, category in self.rules.items():
            if keyword in incident_text:
                signals.append(
                    {
                        "category": category,
                        "trigger": keyword,
                        "confidence": 0.75,
                    }
                )

        risk_level = "LOW"

        if len(signals) >= 5:
            risk_level = "HIGH"
        elif len(signals) >= 2:
            risk_level = "MEDIUM"

        return {
            "detector": "RuleBasedDetector",
            "risk_level": risk_level,
            "signals": signals,
            "signal_count": len(signals),
            "summary": (
                f"Detected {len(signals)} potential weak signal(s) "
                "using rule-based analysis."
            ),
        }