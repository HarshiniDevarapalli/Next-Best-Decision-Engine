# backend/agents/datasource/incident_history_agent.py

from typing import Any, Dict, List

from backend.agents.datasource.base_datasource_agent import BaseDatasourceAgent


class IncidentHistoryAgent(BaseDatasourceAgent):
    """
    Enterprise Incident History Intelligence Agent
    """

    DATASOURCE = "incident_history"

    def __init__(self):
        super().__init__("IncidentHistoryAgent")

    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        similar_incidents = []
        lessons_learned = []
        successful_actions = []
        recurring_patterns = []
        recovery_metrics = []
        insights = []

        for record in records:

            similar_incidents.append(record)

            lessons_learned.extend(
                record.get("lessons_learned", [])
            )

            successful_actions.extend(
                record.get("successful_actions", [])
            )

            recurring_patterns.extend(
                record.get("patterns", [])
            )

            if record.get("recovery_time"):
                recovery_metrics.append(
                    record["recovery_time"]
                )

        if similar_incidents:
            insights.append(
                f"{len(similar_incidents)} similar historical incidents identified."
            )

        return {
            "similar_incidents": similar_incidents,
            "lessons_learned": lessons_learned,
            "successful_actions": successful_actions,
            "recurring_patterns": recurring_patterns,
            "recovery_metrics": recovery_metrics,
            "insights": insights,
        }