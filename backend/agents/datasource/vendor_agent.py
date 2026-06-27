import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class VendorAgent(BaseAgent):

    @property
    def name(self):
        return "vendors"

    @property
    def description(self):
        return "Retrieve alternative vendor information."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/vendors.json")

        with open(data_path, "r") as file:
            vendors = json.load(file)

        vendor_records = [
            vendor
            for vendor in vendors
            if vendor["case_id"] == context.case_id
        ]

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data={
                "vendors": vendor_records
            }
        )