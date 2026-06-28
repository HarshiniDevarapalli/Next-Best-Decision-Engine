# backend/agents/datasource/inventory_agent.py

from typing import Any, Dict, List

from backend.agents.datasource.base_datasource_agent import BaseDatasourceAgent


class InventoryAgent(BaseDatasourceAgent):
    """
    Enterprise Inventory Intelligence Agent
    """

    DATASOURCE = "inventory"

    def __init__(self):
        super().__init__("InventoryAgent")

    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        critical_items = []
        shortages = []
        safety_stock_alerts = []
        replenishment_options = []
        bottlenecks = []
        identified_risks = []
        insights = []

        for record in records:

            current_stock = record.get("current_stock", 0)
            safety_stock = record.get("safety_stock", 0)

            if current_stock <= safety_stock:
                shortages.append(record)
                safety_stock_alerts.append(
                    f"{record.get('item')} below safety stock."
                )

            if record.get("alternate_source"):
                replenishment_options.append(
                    record["alternate_source"]
                )

            if record.get("is_critical"):
                critical_items.append(record)

            if record.get("bottleneck"):
                bottlenecks.append(record["bottleneck"])

            if record.get("risk"):
                identified_risks.append(record["risk"])

        if shortages:
            insights.append(
                f"{len(shortages)} inventory shortages detected."
            )

        if critical_items:
            insights.append(
                f"{len(critical_items)} critical inventory items affected."
            )

        return {
            "critical_items": critical_items,
            "shortages": shortages,
            "safety_stock_alerts": safety_stock_alerts,
            "replenishment_options": replenishment_options,
            "bottlenecks": list(set(bottlenecks)),
            "identified_risks": identified_risks,
            "insights": insights,
        }