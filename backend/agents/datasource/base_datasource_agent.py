# backend/agents/datasource/base_datasource_agent.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from backend.agents.base_agent import BaseAgent
from backend.utils.enterprise_search import EnterpriseSearch


class BaseDatasourceAgent(BaseAgent, ABC):
    """
    Base class for all enterprise datasource agents.

    Responsibilities:
    - Retrieve enterprise knowledge
    - Convert raw records into evidence
    - Generate insights
    - Return a common response schema
    """

    DATASOURCE: str = ""

    def __init__(self, name: str):
        super().__init__(name)

    @abstractmethod
    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Domain-specific analysis implemented
        by each datasource agent.
        """
        pass

    def execute(
        self,
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        records = EnterpriseSearch().search(
            parsed_incident,
            k=5,
        )

        analysis = self.analyze(
            records=records,
            parsed_incident=parsed_incident,
        )

        return {
            "agent": self.name,
            "status": "SUCCESS",
            "datasource": self.DATASOURCE,
            "records_retrieved": len(records),
            "records": records,
            **analysis,
            "confidence": parsed_incident.get(
                "confidence",
                0.0,
            ),
        }