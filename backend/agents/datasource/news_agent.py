import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.responses import Response


class NewsAgent(BaseAgent):

    @property
    def name(self):
        return "news"

    @property
    def description(self):
        return "Retrieve company news."

    def execute(self, context: ExecutionContext) -> Response:

        with open(Path("data/news.json"), "r") as file:
            data = json.load(file)

        return Response(
            agent_name=self.name,
            status="SUCCESS",
            data=data
        )