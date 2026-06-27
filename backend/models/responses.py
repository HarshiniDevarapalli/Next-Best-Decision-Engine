from typing import Any, Dict
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """
    Standard response returned by every agent.
    """

    agent_name: str = Field(..., description="Unique name of the agent")

    status: str = Field(
        default="SUCCESS",
        description="Execution status (SUCCESS or FAILED)"
    )

    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Output produced by the agent"
    )

    execution_time_ms: float = Field(
        default=0.0,
        description="Execution time in milliseconds"
    )

    message: str = Field(
        default="",
        description="Optional status or error message"
    )