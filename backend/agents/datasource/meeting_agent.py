import json
from pathlib import Path

from agents.base_agent import BaseAgent
from models.execution_context import ExecutionContext
from models.agent_result import AgentResult


class MeetingAgent(BaseAgent):

    @property
    def name(self):
        return "meeting"

    @property
    def description(self):
        return "Read meeting transcripts."

    def execute(self, context: ExecutionContext) -> AgentResult:

        with open("data/meetings.json") as file:
            meetings = json.load(file)

        customer_meetings = [
            meeting
            for meeting in meetings
            if meeting["customer_id"] == context.customer_id
        ]

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            data={
                "meetings": customer_meetings
            }
        )