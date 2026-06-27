import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.responses import Response


class CRMAgent(BaseAgent):

    @property
    def name(self):
        return "crm"

    @property
    def description(self):
        return "Fetch customer information from CRM."

    def execute(self, context: ExecutionContext) -> Response:

        file_path = Path("data/crm.json")

        with open(file_path, "r") as file:
            data = json.load(file)

        return Response(
            agent_name=self.name,
            status="SUCCESS",
            data=data
        )