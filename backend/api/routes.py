from fastapi import APIRouter

from models.request import WorkflowRequest
from planner.planner import Planner
from planner.workflow_loader import WorkflowLoader
from registry.registry import AgentRegistry

# Datasource agents
from agents.datasource.supplier_contract_agent import SupplierContractAgent
from agents.datasource.inventory_agent import InventoryAgent
from agents.datasource.vendor_agent import VendorAgent
from agents.datasource.policy_agent import PolicyAgent
from agents.datasource.news_agent import NewsAgent
from agents.datasource.incident_history_agent import IncidentHistoryAgent

# Reasoning agents
from agents.reasoning.weak_signal_agent import WeakSignalAgent
from agents.reasoning.risk_agent import RiskAssessmentAgent
from agents.reasoning.recommendation_agent import RecommendationAgent
from agents.reasoning.explainability_agent import ExplainabilityAgent

router = APIRouter()

# -----------------------------------
# Platform Initialization
# -----------------------------------

workflow_loader = WorkflowLoader()
registry = AgentRegistry()

# Register datasource agents
registry.register(SupplierContractAgent())
registry.register(InventoryAgent())
registry.register(VendorAgent())
registry.register(PolicyAgent())
registry.register(NewsAgent())
registry.register(IncidentHistoryAgent())

# Register reasoning agents
registry.register(WeakSignalAgent())
registry.register(RiskAssessmentAgent())
registry.register(RecommendationAgent())
registry.register(ExplainabilityAgent())

planner = Planner(
    workflow_loader=workflow_loader,
    agent_registry=registry
)

# -----------------------------------
# API Endpoint
# -----------------------------------

@router.post("/workflow/run")
def run_workflow(request: WorkflowRequest):
    """
    Execute a workflow for a given crisis case.
    """

    context = planner.execute_workflow(
        workflow_name=request.workflow,
        case_id=request.case_id
    )

    return context