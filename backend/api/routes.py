# backend/api/routes.py

from fastapi import APIRouter, HTTPException

from backend.planner.planner import Planner
from backend.models.request import WorkflowRequest

router = APIRouter()

planner = Planner()


@router.post("/workflow/run")
async def run_workflow(request: WorkflowRequest):

    try:

        response = planner.execute(
            workflow=request.workflow,
            mode=request.mode,
            incident=request.incident,
            case_id=request.case_id,
            overrides=request.overrides,
        )

        return {
            "status": "SUCCESS",
            "message": "Workflow executed successfully.",
            "data": response,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )