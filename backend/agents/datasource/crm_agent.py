import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class CRMAgent(BaseAgent):

    @property
    def name(self):
        return "crm"

    @property
    def description(self):
        return "Fetch customer information from CRM."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/crm.json")

        with open(data_path, "r") as f:
            customers = json.load(f)

        customer = next(
            (
                c
                for c in customers
                if c["customer_id"] == context.customer_id
            ),
            {}
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data=customer
        )