import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class KnowledgeAgent(BaseAgent):

    @property
    def name(self):
        return "knowledge"

    @property
    def description(self):
        return "Retrieve organizational knowledge."

    def execute(self, context: ExecutionContext) -> AgentResult:

        with open("data/knowledge.json") as file:
            knowledge = json.load(file)

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data={
                "knowledge": knowledge
            }
        )