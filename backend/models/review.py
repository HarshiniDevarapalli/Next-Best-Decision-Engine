from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class HumanReviewRequest(BaseModel):
    case_id: str

    reviewer: str

    reviewer_role: str

    decision: Literal[
        "approve",
        "reject",
        "revise",
    ]

    comments: str = ""

    updated_recommendation: Optional[
        Dict[str, Any]
    ] = None


class HumanReviewResponse(BaseModel):
    case_id: str

    status: str

    message: str

    review_timestamp: datetime


class AuditEntry(BaseModel):
    reviewer: str

    reviewer_role: str

    decision: str

    comments: str = ""

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


class HumanReviewState(BaseModel):
    review_required: bool = False

    review_status: Optional[str] = None

    reviewer: Optional[str] = None

    reviewer_role: Optional[str] = None

    review_comments: Optional[str] = None

    approved_recommendation: Optional[
        Dict[str, Any]
    ] = None

    review_timestamp: Optional[
        datetime
    ] = None

    audit_log: List[
        AuditEntry
    ] = Field(default_factory=list)