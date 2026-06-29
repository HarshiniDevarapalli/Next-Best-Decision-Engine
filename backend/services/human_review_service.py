from datetime import datetime
from typing import Any, Dict

from backend.graph.state import WorkflowState


class HumanReviewService:
    """
    Processes reviewer decisions and updates the workflow state.
    """

    @staticmethod
    def apply_review(
        state: WorkflowState,
        reviewer: str,
        reviewer_role: str,
        decision: str,
        comments: str = "",
        updated_recommendation: Dict[str, Any] | None = None,
    ) -> WorkflowState:

        decision = decision.lower()

        if decision not in {"approve", "reject", "revise"}:
            raise ValueError(
                "Invalid review decision."
            )

        state["reviewer"] = reviewer
        state["reviewer_role"] = reviewer_role
        state["review_comments"] = comments
        state["review_timestamp"] = datetime.utcnow().isoformat()
        state["review_status"] = decision

        if decision == "approve":
            state["approved_recommendation"] = state.get(
                "recommendation_report"
            )

        elif decision == "revise":
            state["approved_recommendation"] = (
                updated_recommendation
                or state.get("recommendation_report")
            )

        elif decision == "reject":
            state["approved_recommendation"] = None

        state["audit_log"].append(
            {
                "reviewer": reviewer,
                "reviewer_role": reviewer_role,
                "decision": decision,
                "comments": comments,
                "timestamp": state["review_timestamp"],
            }
        )

        return state