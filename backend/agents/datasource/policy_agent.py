import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class PolicyAgent(BaseAgent):

    @property
    def name(self):
        return "policy"

    @property
    def description(self):
        return "Retrieve enterprise crisis response policies."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/policies.json")

        with open(data_path, "r") as file:
            policies = json.load(file)

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data={
                "policies": policies
            }
        )