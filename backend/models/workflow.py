from typing import List, Dict, Any
from pydantic import BaseModel, Field


class WorkflowAgent(BaseModel):
    name: str
    enabled: bool = True


class Workflow(BaseModel):
    workflow_name: str
    description: str
    version: str = "1.0"

    metadata: Dict[str, Any] = Field(default_factory=dict)

    agents: List[WorkflowAgent]