from fastapi import APIRouter

from models.request import WorkflowRequest
from models.simulate_request import SimulateRequest

from planner.planner import Planner
from planner.workflow_loader import WorkflowLoader
from planner.simulator import run_simulation

from registry.registry import AgentRegistry


router = APIRouter()


@router.post("/workflow/run")
async def run_workflow(request: WorkflowRequest):

    workflow_loader = WorkflowLoader()

    registry = AgentRegistry()

    planner = Planner(
        workflow_loader=workflow_loader,
        agent_registry=registry
    )

    context = planner.execute_workflow(
        workflow_name=request.workflow_name,
        case_id=request.case_id
    )

    return context


@router.post("/workflow/simulate")
async def simulate_workflow(request: SimulateRequest):

    workflow_loader = WorkflowLoader()

    registry = AgentRegistry()

    context = run_simulation(
        workflow_name=request.workflow,
        case_id=request.case_id,
        overrides=request.overrides,
        registry=registry,
    )

    return context