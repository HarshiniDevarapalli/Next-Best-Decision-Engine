from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Base class for every agent in the system.
    """

    def __init__(self, name: str, description: str = ""):
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any):
        """
        Execute the agent.
        """
        pass