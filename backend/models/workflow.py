from typing import List

from pydantic import BaseModel, Field


class Workflow(BaseModel):
    """
    Represents a workflow configuration loaded from JSON.
    """

    workflow_name: str = Field(
        ...,
        description="Unique workflow name"
    )

    description: str = Field(
        default=""
    )

    agents: List[str] = Field(
        default_factory=list,
        description="Ordered list of agent names to execute"
    )