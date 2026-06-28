# backend/agents/datasource/vendor_agent.py

from typing import Any, Dict, List

from backend.agents.datasource.base_datasource_agent import BaseDatasourceAgent


class VendorAgent(BaseDatasourceAgent):
    """
    Enterprise Vendor Intelligence Agent
    """

    DATASOURCE = "vendors"

    def __init__(self):
        super().__init__("VendorAgent")

    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        affected_vendors = []
        alternate_vendors = []
        dependencies = []
        identified_risks = []
        insights = []

        vendor_names = {
            str(v.get("name", "")).lower()
            for v in parsed_incident.get("vendor_entities", [])
            if isinstance(v, dict)
        }

        for record in records:

            if record.get("status") != "ACTIVE":
                identified_risks.append(
                    f"Vendor {record.get('name')} is not active."
                )

            if record.get("alternate_vendor"):
                alternate_vendors.append(
                    record["alternate_vendor"]
                )

            if record.get("dependencies"):
                dependencies.extend(
                    record["dependencies"]
                )

            affected_vendors.append(record)

        if alternate_vendors:
            insights.append(
                "Alternate vendors are available."
            )

        if not alternate_vendors:
            insights.append(
                "No alternate vendors identified."
            )

        return {
            "affected_vendors": affected_vendors,
            "alternate_vendors": alternate_vendors,
            "dependencies": list(set(dependencies)),
            "identified_risks": identified_risks,
            "insights": insights,
        }