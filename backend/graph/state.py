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

    rule_based_report: Optional[Dict[str, Any]]
    llm_report: Optional[Dict[str, Any]]
    shadow_comparison: Optional[Dict[str, Any]]

    risk_report: Optional[Dict[str, Any]]
    recommendation_report: Optional[Dict[str, Any]]

    simulation_report: Optional[Dict[str, Any]]
    decision_scores: Optional[Dict[str, Any]]
    cost_report: Optional[Dict[str, Any]]
    timeline_report: Optional[Dict[str, Any]]
    scenario_comparison: Optional[Dict[str, Any]]

    explainability_report: Optional[Dict[str, Any]]

    executed_agents: List[str]
    skipped_agents: List[str]

    response: Optional[Dict[str, Any]]


    review_required: bool
    review_status: Optional[str]

    reviewer: Optional[str]
    reviewer_role: Optional[str]

    review_comments: Optional[str]

    approved_recommendation: Optional[Dict[str, Any]]

    review_timestamp: Optional[str]

    audit_log: List[Dict[str, Any]]