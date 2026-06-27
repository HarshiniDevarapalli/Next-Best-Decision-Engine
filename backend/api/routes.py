from fastapi import APIRouter

from models.request import WorkflowRequest
from planner.planner import Planner
from planner.workflow_loader import WorkflowLoader
from registry.registry import AgentRegistry

# Import dummy agents
from backend.agents.datasource.supplier_contract_agent import SupplierContractAgent
from backend.agents.datasource.inventory_agent import InventoryAgent
from backend.agents.datasource.vendor_agent import VendorAgent
from backend.agents.datasource.policy_agent import PolicyAgent
from backend.agents.datasource.news_agent import NewsAgent
from backend.agents.datasource.incident_history_agent import IncidentHistoryAgent

router = APIRouter()

# ---------- Platform Initialization ----------

workflow_loader = WorkflowLoader()

registry = AgentRegistry()

registry.register(SupplierContractAgent())
registry.register(InventoryAgent())
registry.register(VendorAgent())
registry.register(PolicyAgent())
registry.register(NewsAgent())
registry.register(IncidentHistoryAgent())

planner = Planner(workflow_loader, registry)

# ---------- API ----------

@router.post("/workflow/run")
def run_workflow(request: WorkflowRequest):

    context = planner.execute_workflow(
        workflow_name=request.workflow,
        case_id=request.case_id
    )

    return context