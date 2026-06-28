from typing import Any, Dict
from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    """
    Request payload for the What-If Simulator.

    Same as WorkflowRequest, but accepts an additional
    'overrides' dictionary that lets the caller modify
    specific fields of the case data before the reasoning
    agents run, without changing the original stored data.

    Example:
    {
        "workflow": "crisis_response",
        "case_id": "incident_001",
        "overrides": {
            "inventory": {
                "stock_days_remaining": 2
            }
        }
    }
    """

    workflow: str = Field(
        ...,
        description="Name of the workflow to execute"
    )

    case_id: str = Field(
        ...,
        description="Unique identifier for the workflow case or incident"
    )

    overrides: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description=(
            "Field overrides keyed by datasource agent name. "
            "Each value is a dict of field_name: new_value pairs "
            "to overwrite on top of the real looked-up data."
        )
    )