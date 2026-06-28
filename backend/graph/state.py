# backend/graph/state.py

from typing import Any, Dict, List, Optional, TypedDict


class WorkflowState(TypedDict):

    workflow: str
    mode: str

    incident: Optional[str]
    case_id: Optional[str]

    overrides: Dict[str, Any]

    execution_plan: Dict[str, Any]

    parsed_incident: Dict[str, Any]

    datasource_context: Dict[str, Any]

    rule_based_report: Dict[str, Any]
    llm_report: Dict[str, Any]
    shadow_comparison: Dict[str, Any]

    risk_report: Dict[str, Any]
    recommendation_report: Dict[str, Any]
    explainability_report: Dict[str, Any]

    # -------- Phase 4 --------

    simulation_report: Dict[str, Any]

    decision_scores: Dict[str, Any]

    cost_report: Dict[str, Any]

    timeline_report: Dict[str, Any]

    scenario_comparison: Dict[str, Any]

    # -------------------------

    executed_agents: List[str]
    skipped_agents: List[str]

    response: Dict[str, Any]