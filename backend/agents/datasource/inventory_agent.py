import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class InventoryAgent(BaseAgent):

    @property
    def name(self):
        return "inventory"

    @property
    def description(self):
        return "Retrieve inventory information."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/inventory.json")

        with open(data_path, "r") as file:
            inventory = json.load(file)

        inventory_record = next(
            (
                item
                for item in inventory
                if item["case_id"] == context.case_id
            ),
            {}
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data=inventory_record
        )