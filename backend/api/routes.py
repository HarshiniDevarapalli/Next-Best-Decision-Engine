from fastapi import APIRouter

from models.request import WorkflowRequest
from planner.planner import Planner
from planner.workflow_loader import WorkflowLoader
from registry.registry import AgentRegistry

# Import dummy agents
from agents.datasource.crm_agent import CRMAgent
from agents.datasource.meeting_agent import MeetingAgent
from agents.datasource.news_agent import NewsAgent
from agents.datasource.knowledge_agent import KnowledgeAgent

router = APIRouter()

# ---------- Platform Initialization ----------

workflow_loader = WorkflowLoader()

registry = AgentRegistry()

registry.register(CRMAgent())
registry.register(MeetingAgent())
registry.register(NewsAgent())
registry.register(KnowledgeAgent())

planner = Planner(workflow_loader, registry)

# ---------- API ----------

@router.post("/workflow/run")
def run_workflow(request: WorkflowRequest):

    context = planner.execute_workflow(
        workflow_name=request.workflow,
        customer_id=request.customer_id
    )

    return context