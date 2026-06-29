# backend/planner/planner.py

import os
from pprint import pprint
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
            # Request
            "workflow": workflow,
            "mode": mode,
            "incident": incident,
            "case_id": case_id,
            "overrides": overrides or {},

            # Planner
            "execution_plan": execution_plan,

            # Incident
            "parsed_incident": {},

            # Datasource
            "datasource_context": {},

            # Weak Signal
            "rule_based_report": None,
            "llm_report": None,
            "shadow_comparison": None,

            # Risk
            "risk_report": None,

            # Recommendation
            "recommendation_report": None,

            # Phase 4
            "simulation_report": None,
            "decision_scores": None,
            "cost_report": None,
            "timeline_report": None,
            "scenario_comparison": None,

            # Explainability
            "explainability_report": None,

            # Execution Trace
            "executed_agents": [],
            "skipped_agents": [],

            # Final Response
            "response": None,

            # Human-in-the-Loop
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

        # ---------------- DEBUG ----------------

        print("\n===== LANGGRAPH RESULT KEYS =====")
        pprint(result.keys())

        print("\n===== DEBUG =====")
        print("risk_report:", result.get("risk_report") is not None)
        print("simulation_report:", result.get("simulation_report") is not None)
        print("decision_scores:", result.get("decision_scores") is not None)
        print("cost_report:", result.get("cost_report") is not None)
        print("timeline_report:", result.get("timeline_report") is not None)
        print("scenario_comparison:", result.get("scenario_comparison") is not None)

        if result.get("response"):
            print("\n===== RESPONSE KEYS =====")
            pprint(result["response"].keys())

        # ---------------------------------------

        # If workflow paused for Human Review,
        # return exactly what HumanReviewNode created.
        if (
            result.get("response")
            and result["response"].get("status") == "WAITING_FOR_HUMAN_REVIEW"
        ):
            return result["response"]

        # Normal completion
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