from datetime import datetime
from typing import Any, Dict

from backend.graph.state import WorkflowState


class HumanReviewAgent:
    """
    Handles Human-in-the-Loop review of AI recommendations.
    """

    def execute(
        self,
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
                "Decision must be approve, reject, or revise."
            )

        state["reviewer"] = reviewer
        state["reviewer_role"] = reviewer_role
        state["review_comments"] = comments
        state["review_timestamp"] = datetime.utcnow().isoformat()
        state["review_status"] = decision

        recommendation = state.get("recommendation_report")

        if decision == "approve":

            state["approved_recommendation"] = recommendation

        elif decision == "revise":

            state["approved_recommendation"] = (
                updated_recommendation
                if updated_recommendation is not None
                else recommendation
            )

        elif decision == "reject":

            state["approved_recommendation"] = None

        audit_entry = {
            "reviewer": reviewer,
            "reviewer_role": reviewer_role,
            "decision": decision,
            "comments": comments,
            "timestamp": state["review_timestamp"],
        }

        state["audit_log"].append(audit_entry)

        state["executed_agents"].append("HumanReviewAgent")

        return state