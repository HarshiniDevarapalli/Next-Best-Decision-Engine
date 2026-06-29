from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    """
    Request payload for executing a workflow.
    """

    workflow: str = Field(
        ...,
        description="Name of the workflow to execute"
    )

    case_id: str = Field(
        ...,
        description="Unique identifier for the workflow case or incident"
    )