# backend/planner/workflow_loader.py

from typing import Any, Dict, List


class WorkflowLoader:
    """
    Dynamically decides which enterprise datasource agents
    should participate based on the parsed incident.

    No business domains are hardcoded.
    """

    def __init__(self):
        self.available_agents = {
            "supplier_contracts": "SupplierContractAgent",
            "inventory": "InventoryAgent",
            "vendors": "VendorAgent",
            "policies": "PolicyAgent",
            "news": "NewsAgent",
            "incident_history": "IncidentHistoryAgent",
        }

    def build_execution_plan(
        self,
        parsed_incident: Dict[str, Any],
    ) -> List[str]:

        plan: List[str] = []

        # Gemini tells us which enterprise sources are useful
        sources = parsed_incident.get(
            "recommended_data_sources",
            []
        )

        for source in sources:
            agent = self.available_agents.get(source)

            if agent and agent not in plan:
                plan.append(agent)

        # Fallback if the LLM couldn't determine sources
        if not plan:
            plan = list(self.available_agents.values())

        return plan