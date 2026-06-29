from typing import Dict, List

from agents.base_agent import BaseAgent


class AgentRegistry:
    """
    Registry for all available agents.

    The Planner interacts only with this registry to
    discover and retrieve agents.
    """

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """
        Register an agent.

        Raises:
            ValueError: If an agent with the same name already exists.
        """
        if agent.name in self._agents:
            raise ValueError(f"Agent '{agent.name}' is already registered.")

        self._agents[agent.name] = agent

    def get(self, agent_name: str) -> BaseAgent:
        """
        Retrieve an agent by name.

        Raises:
            KeyError: If the agent is not registered.
        """
        if agent_name not in self._agents:
            raise KeyError(f"Agent '{agent_name}' is not registered.")

        return self._agents[agent_name]

    def list_agents(self) -> List[str]:
        """
        Return a list of all registered agent names.
        """
        return list(self._agents.keys())

    def is_registered(self, agent_name: str) -> bool:
        """
        Check whether an agent is registered.
        """
        return agent_name in self._agents