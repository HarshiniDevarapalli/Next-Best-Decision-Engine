import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class SupplierContractAgent(BaseAgent):

    @property
    def name(self):
        return "supplier_contracts"

    @property
    def description(self):
        return "Retrieve supplier contract information."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/supplier_contracts.json")

        with open(data_path, "r") as file:
            suppliers = json.load(file)

        supplier = next(
            (
                s for s in suppliers
                if s["case_id"] == context.case_id
            ),
            {}
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data=supplier
        )