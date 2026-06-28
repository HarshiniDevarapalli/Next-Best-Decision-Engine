# backend/agents/datasource/policy_agent.py

from typing import Any, Dict, List

from backend.agents.datasource.base_datasource_agent import BaseDatasourceAgent


class PolicyAgent(BaseDatasourceAgent):
    """
    Enterprise Policy Intelligence Agent
    """

    DATASOURCE = "policies"

    def __init__(self):
        super().__init__("PolicyAgent")

    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        applicable_policies = []
        compliance_requirements = []
        business_continuity = []
        escalation_rules = []
        identified_risks = []
        insights = []

        for record in records:

            applicable_policies.append(record)

            compliance_requirements.extend(
                record.get("compliance", [])
            )

            business_continuity.extend(
                record.get("business_continuity", [])
            )

            escalation_rules.extend(
                record.get("escalation", [])
            )

            if record.get("risk"):
                identified_risks.append(record["risk"])

        if applicable_policies:
            insights.append(
                f"{len(applicable_policies)} relevant policies found."
            )

        return {
            "applicable_policies": applicable_policies,
            "compliance_requirements": compliance_requirements,
            "business_continuity": business_continuity,
            "escalation_rules": escalation_rules,
            "identified_risks": identified_risks,
            "insights": insights,
        }