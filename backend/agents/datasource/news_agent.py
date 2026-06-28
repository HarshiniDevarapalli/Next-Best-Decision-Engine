import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class NewsAgent(BaseAgent):

    @property
    def name(self):
        return "news"

    @property
    def description(self):
        return "Retrieve news related to the crisis."

    def execute(self, context: ExecutionContext) -> AgentResult:

        data_path = Path("data/news.json")

        with open(data_path, "r") as file:
            news = json.load(file)

        article = next(
            (
                item
                for item in news
                if item["case_id"] == context.case_id
            ),
            {}
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data=article
        )