from agents.base_agent import BaseAgent
from agents.datasource.crm_agent import CRMAgent
from agents.datasource.knowledge_agent import KnowledgeAgent
from agents.datasource.meeting_agent import MeetingAgent
from agents.datasource.news_agent import NewsAgent
from agents.reasoning.explainability_agent import ExplainabilityAgent
from agents.reasoning.recommendation_agent import RecommendationAgent
from agents.reasoning.risk_agent import RiskAgent
from agents.reasoning.weak_signal_agent import WeakSignalAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        defaults: list[BaseAgent] = [
            CRMAgent(),
            MeetingAgent(),
            NewsAgent(),
            KnowledgeAgent(),
            WeakSignalAgent(),
            RiskAgent(),
            RecommendationAgent(),
            ExplainabilityAgent(),
        ]
        for agent in defaults:
            self.register(agent)

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise KeyError(f"Agent not registered: {name}")
        return self._agents[name]

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())
