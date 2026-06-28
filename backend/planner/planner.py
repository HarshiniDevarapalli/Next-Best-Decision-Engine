# backend/planner/planner.py
# (Final integrated Planner)

import os
from typing import Any, Dict
from backend.graph.workflow_graph import enterprise_workflow
from backend.graph.state import WorkflowState
from backend.services.ai.planner_chain import PlannerChain


class Planner:

    def __init__(self):

        self.planner = PlannerChain(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.workflow = enterprise_workflow

    def execute(
        self,
        workflow: str,
        mode: str,
        incident: str | None = None,
        case_id: str | None = None,
        overrides: Dict[str, Any] | None = None,
    ):

        execution_plan = self.planner.plan(
            workflow=workflow,
            mode=mode,
            incident=incident or "",
        ).model_dump()

        state: WorkflowState = {
            "workflow": workflow,
            "mode": mode,
            "incident": incident,
            "case_id": case_id,
            "overrides": overrides or {},

            "execution_plan": execution_plan,

            "parsed_incident": {},
            "datasource_context": {},

            "rule_based_report": None,
            "llm_report": None,
            "shadow_comparison": None,

            "risk_report": None,
            "recommendation_report": None,
            "simulation_report": None,
            "decision_scores": None,
            "cost_report": None,
            "timeline_report": None,
            "scenario_comparison": None,
            "explainability_report": None,

            "executed_agents": [],
            "skipped_agents": [],
            "response": None,
        }

        result = self.workflow.invoke(state)

        return result["response"]