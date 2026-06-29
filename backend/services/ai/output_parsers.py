# backend/services/ai/output_parsers.py

from typing import Any, Dict, List

from pydantic import BaseModel, Field

class ShadowComparison(BaseModel):
    agreement: float | None = None
    differences: List[str] = Field(default_factory=list)
    recommended_output: Dict[str, Any] = Field(default_factory=dict)

class PlannerOutput(BaseModel):
    """
    Planner output consumed by the LangGraph workflow.
    The planner is responsible for deciding which agents execute.
    """

    workflow: str
    objective: str
    crisis_type: str
    execution_strategy: str

    # Agents selected by the planner
    datasource_agents: List[str] = Field(default_factory=list)
    reasoning_agents: List[str] = Field(default_factory=list)

    # Execution plan
    execution_order: List[str] = Field(default_factory=list)
    parallel_groups: List[List[str]] = Field(default_factory=list)

    # Planner decisions
    shadow_mode: bool = False
    what_if: bool = False
    requires_human_review: bool = False

    # Planner explanation
    planner_reasoning: str
    confidence: float


class IncidentContext(BaseModel):
    summary: str
    crisis_type: str
    severity: str

    supplier_entities: List[Dict[str, Any]] = Field(default_factory=list)
    vendor_entities: List[Dict[str, Any]] = Field(default_factory=list)
    inventory_entities: List[Dict[str, Any]] = Field(default_factory=list)
    contract_entities: List[Dict[str, Any]] = Field(default_factory=list)
    logistics_entities: List[Dict[str, Any]] = Field(default_factory=list)

    affected_products: List[str] = Field(default_factory=list)
    affected_locations: List[str] = Field(default_factory=list)
    affected_business_units: List[str] = Field(default_factory=list)

    dependencies: List[str] = Field(default_factory=list)
    identified_risks: List[str] = Field(default_factory=list)
    weak_signals: List[str] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)

    recommended_data_sources: List[str] = Field(default_factory=list)

    confidence: float


class RiskAssessment(BaseModel):
    overall_risk: str

    supplier_risk: str
    vendor_risk: str
    inventory_risk: str
    logistics_risk: str
    contractual_risk: str

    operational_impact: str
    financial_impact: str
    compliance_impact: str
    reputational_impact: str

    key_risks: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)

    reasoning: str

    confidence: float


class RecommendationReport(BaseModel):
    priority: str

    immediate_actions: List[str] = Field(default_factory=list)
    short_term_actions: List[str] = Field(default_factory=list)
    long_term_actions: List[str] = Field(default_factory=list)

    business_continuity_actions: List[str] = Field(default_factory=list)

    stakeholders: List[str] = Field(default_factory=list)

    escalation_steps: List[str] = Field(default_factory=list)

    expected_outcomes: List[str] = Field(default_factory=list)

    confidence: float


class ExplainabilityReport(BaseModel):
    executive_summary: str

    planner_reasoning: str

    reasoning_steps: List[str] = Field(default_factory=list)

    datasource_evidence: List[str] = Field(default_factory=list)

    evidence: List[str] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)

    uncertainties: List[str] = Field(default_factory=list)

    confidence: float

class PlannerOutput(BaseModel):
    workflow: str
    crisis_type: str
    execution_strategy: str

    datasource_agents: List[str] = Field(default_factory=list)
    reasoning_agents: List[str] = Field(default_factory=list)

    execution_order: List[str] = Field(default_factory=list)
    parallel_groups: List[List[str]] = Field(default_factory=list)

    # -------- Phase 4 --------

    simulation_enabled: bool = True
    decision_scoring_enabled: bool = True
    cost_analysis_enabled: bool = True
    timeline_prediction_enabled: bool = True
    scenario_comparison_enabled: bool = True

    # -------------------------

    shadow_mode: bool
    what_if: bool
    requires_human_review: bool

    planner_reasoning: str
    confidence: float
# backend/services/ai/output_parsers.py
# (Add Phase 4 models)

class SimulationScenario(BaseModel):
    title: str
    description: str
    probability: float
    business_impact: str
    operational_impact: str
    recommended_action: str


class SimulationReport(BaseModel):
    baseline: str
    scenarios: List[SimulationScenario] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    best_scenario: str
    worst_scenario: str
    confidence: float


class DecisionOption(BaseModel):
    action: str
    feasibility: float
    business_value: float
    operational_risk: float
    implementation_effort: float
    overall_score: float
    reasoning: str


class DecisionScoringReport(BaseModel):
    ranked_decisions: List[DecisionOption] = Field(default_factory=list)
    best_decision: str
    confidence: float


class CostImpact(BaseModel):
    action: str
    estimated_cost: str
    operational_impact: str
    financial_impact: str
    roi: str


class CostImpactReport(BaseModel):
    impacts: List[CostImpact] = Field(default_factory=list)
    lowest_cost_option: str
    highest_roi_option: str
    confidence: float


class TimelineStage(BaseModel):
    stage: str
    estimated_duration: str
    milestone: str


class TimelinePredictionReport(BaseModel):
    estimated_recovery_time: str
    critical_path: List[str] = Field(default_factory=list)
    stages: List[TimelineStage] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    confidence: float


class ScenarioComparison(BaseModel):
    scenario: str
    advantages: List[str] = Field(default_factory=list)
    disadvantages: List[str] = Field(default_factory=list)
    score: float


class ScenarioComparisonReport(BaseModel):
    comparisons: List[ScenarioComparison] = Field(default_factory=list)
    recommended_scenario: str
    reasoning: str
    confidence: float