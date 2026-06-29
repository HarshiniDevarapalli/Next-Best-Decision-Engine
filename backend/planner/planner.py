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
        }

        result = self.workflow.invoke(state)

        # During development, return the whole state if response wasn't produced.
        if result.get("response") is not None:
            return result["response"]

        return result