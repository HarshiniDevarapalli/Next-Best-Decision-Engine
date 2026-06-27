import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class IncidentHistoryAgent(BaseAgent):

    @property
    def name(self):
        return "incident_history"

    @property
    def description(self):
        return "Retrieve historical incidents similar to the current crisis."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/incident_history.json")

        with open(data_path, "r") as file:
            incidents = json.load(file)

        incident_records = [
            incident
            for incident in incidents
            if incident["case_id"] == context.case_id
        ]

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data={
                "incident_history": incident_records
            }
        )