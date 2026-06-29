# backend/agents/datasource/news_agent.py

from typing import Any, Dict, List

from backend.agents.datasource.base_datasource_agent import BaseDatasourceAgent


class NewsAgent(BaseDatasourceAgent):
    """
    Enterprise News Intelligence Agent
    """

    DATASOURCE = "news"

    def __init__(self):
        super().__init__("NewsAgent")

    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        relevant_articles = []
        external_events = []
        supplier_alerts = []
        regulatory_updates = []
        market_impacts = []
        identified_risks = []
        insights = []

        for record in records:

            relevant_articles.append(record)

            if record.get("event"):
                external_events.append(record["event"])

            if record.get("supplier_alert"):
                supplier_alerts.append(record["supplier_alert"])

            if record.get("regulation"):
                regulatory_updates.append(record["regulation"])

            if record.get("market_impact"):
                market_impacts.append(record["market_impact"])

            if record.get("risk"):
                identified_risks.append(record["risk"])

        if external_events:
            insights.append(
                f"{len(external_events)} external events may impact the supply chain."
            )

        return {
            "relevant_articles": relevant_articles,
            "external_events": external_events,
            "supplier_alerts": supplier_alerts,
            "regulatory_updates": regulatory_updates,
            "market_impacts": market_impacts,
            "identified_risks": identified_risks,
            "insights": insights,
        }