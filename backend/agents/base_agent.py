# backend/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Any

from backend.models.execution_context import ExecutionContext
from backend.models.agent_result import AgentResult


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Next Best Decision Engine.

    Every agent in the platform (data source, reasoning, or future plugins)
    must inherit from this class and implement the execute() method.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the agent."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description of the agent's responsibility."""
        pass

    @abstractmethod
    def execute(self, context: ExecutionContext) -> AgentResult:
        """
        Execute the agent.

        Parameters
        ----------
        context : ExecutionContext
            Shared execution context containing the current workflow state.

        Returns
        -------
        AgentResult
            Standardized result returned by every agent.
        """
        pass