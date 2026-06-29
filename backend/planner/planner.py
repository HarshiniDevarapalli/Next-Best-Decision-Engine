# backend/planner/planner.py

import os
from typing import Any, Dict, Optional

from backend.graph.workflow_graph import enterprise_workflow
from backend.graph.state import WorkflowState
from backend.services.ai.planner_chain import PlannerChain


class Planner:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.planner = PlannerChain(api_key=api_key)
        self.workflow = enterprise_workflow

    def execute(
        self,
        workflow: str,
        mode: str,
        incident: Optional[str] = None,
        case_id: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None,
    ):

        execution_plan = self.planner.plan(
            workflow=workflow,
            mode=mode,
            incident=incident or "",
        )

        if hasattr(execution_plan, "model_dump"):
            execution_plan = execution_plan.model_dump()

        state: WorkflowState = {
            "workflow": workflow,
            "mode": mode,
            "incident": incident,
            "case_id": case_id,
            "overrides": overrides or {},

            # Planner output
            "execution_plan": execution_plan,

            # Incident
            "parsed_incident": {},

            # Datasource aggregation
            "datasource_context": {},

            # Weak Signal
            "rule_based_report": None,
            "llm_report": None,
            "shadow_comparison": None,

            # Risk
            "risk_report": None,

            # Recommendation
            "recommendation_report": None,

            # -------- Phase 4 --------
            "simulation_report": None,
            "decision_scores": None,
            "cost_report": None,
            "timeline_report": None,
            "scenario_comparison": None,
            # -------------------------

            # Explainability
            "explainability_report": None,

            # Execution trace
            "executed_agents": [],
            "skipped_agents": [],

            # Final response
            "response": None,

            # -------------------------
            # Human-in-the-Loop
            # -------------------------

            "review_required": execution_plan.get(
                "requires_human_review",
                False,
            ),

            "review_status": None,

            "reviewer": None,

            "reviewer_role": None,

            "review_comments": None,

            "approved_recommendation": None,

            "review_timestamp": None,

            "audit_log": [],
        }

        result = self.workflow.invoke(state)
        # Human-in-the-Loop pause
        if (
            result.get("review_required")
            and result.get("review_status") is None
        ):
            return {
                "status": "WAITING_FOR_HUMAN_REVIEW",
                "case_id": result.get("case_id"),
                "planner": result.get("execution_plan"),
                "recommendation": result.get("recommendation_report"),
                "explainability": result.get("explainability_report"),
                "message": "Awaiting human approval."
            }

        # Normal execution
        if result.get("response") is not None:
            return result["response"]

        return result
def resume_after_review(
    self,
    state: WorkflowState,
):

    result = self.workflow.invoke(state)

    if result.get("response") is not None:
        return result["response"]

    return result