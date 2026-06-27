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
        return "Retrieve company news."

    def execute(self, context: ExecutionContext) -> AgentResult:

        with open("data/news.json") as file:
            news = json.load(file)

        customer_news = [
            article
            for article in news
            if article["customer_id"] == context.customer_id
        ]

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data={
                "news": customer_news
            }
        )