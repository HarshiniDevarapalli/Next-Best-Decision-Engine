# backend/models/request.py

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    workflow: str = Field(
        ...,
        description="Workflow to execute."
    )

    mode: Literal[
        "live",
        "scenario",
        "what_if"
    ] = "live"

    incident: Optional[str] = Field(
        default=None,
        description="Natural language incident entered by the user."
    )

    case_id: Optional[str] = Field(
        default=None,
        description="Scenario ID (used only in scenario mode)."
    )

    overrides: Dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )