from typing import Any, Dict, List
from uuid import uuid4

from pydantic import BaseModel, Field

from models.agent_result import AgentResult


class ExecutionContext(BaseModel):
    """
    Shared context passed between all agents during workflow execution.
    """

    execution_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    workflow_name: str

    case_id: str

    status: str = "RUNNING"

    context_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Shared data accumulated during workflow execution"
    )

    agent_results: List[AgentResult] = Field(
        default_factory=list,
        description="Results returned by executed agents"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata"
    )