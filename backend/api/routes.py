from datetime import datetime

from fastapi import APIRouter, HTTPException

from backend.models.request import WorkflowRequest
from backend.models.review import (
    HumanReviewRequest,
    HumanReviewResponse,
)
from backend.planner.planner import Planner
from backend.services.human_review_service import HumanReviewService


router = APIRouter()

# ---------------------------------------------------------------
# In-memory state store.
#
# Keyed by case_id. Holds the full LangGraph WorkflowState dict for
# any run that is currently paused and waiting on human review, so
# that a later /review/submit call can resume it from where it left
# off. This is intentionally simple (no database) for the hackathon
# timeline - replace with Redis/DB for real persistence.
# ---------------------------------------------------------------
workflow_store: dict = {}

planner = Planner()


def _generate_case_id() -> str:
    return datetime.utcnow().strftime("case_%Y%m%d%H%M%S%f")


@router.post("/analyze", tags=["Workflow"])
def analyze(request: WorkflowRequest):
    """
    Entry point for running the full enterprise decision workflow.

    Accepts a natural-language incident description (or a case_id
    for scenario/what_if mode), runs the Planner + LangGraph
    pipeline, and returns either:
      - the completed response report, or
      - a WAITING_FOR_HUMAN_REVIEW payload if the planner decided
        this incident requires human review before finalizing.

    In the WAITING_FOR_HUMAN_REVIEW case, the full intermediate
    state is cached under a generated case_id so /review/submit can
    resume it later.
    """

    case_id = request.case_id or _generate_case_id()

    result = planner.execute(
        workflow=request.workflow,
        mode=request.mode,
        incident=request.incident,
        case_id=case_id,
        overrides=request.overrides,
    )

    if isinstance(result, dict) and result.get("status") == "WAITING_FOR_HUMAN_REVIEW":
        raw_state = result.pop("_raw_state", None)
        workflow_store[case_id] = raw_state
        result["case_id"] = case_id
        return result

    return {
        "case_id": case_id,
        "status": "COMPLETED",
        "result": result,
    }


@router.post(
    "/review/submit",
    response_model=HumanReviewResponse,
    tags=["Human Review"],
)
def submit_review(request: HumanReviewRequest):
    """
    Record a human reviewer's decision (approve / reject / revise)
    for a case that is currently paused awaiting review, then
    resume the workflow to produce the final response.
    """

    if request.case_id not in workflow_store:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found or not awaiting review.",
        )

    state = workflow_store[request.case_id]

    state = HumanReviewService.apply_review(
        state=state,
        reviewer=request.reviewer,
        reviewer_role=request.reviewer_role,
        decision=request.decision,
        comments=request.comments,
        updated_recommendation=request.updated_recommendation,
    )

    final_result = planner.resume_after_review(state)

    workflow_store[request.case_id] = state

    return HumanReviewResponse(
        case_id=request.case_id,
        status=state["review_status"],
        message="Review recorded and workflow resumed successfully.",
        review_timestamp=datetime.utcnow(),
    )


@router.get("/review/{case_id}", tags=["Human Review"])
def get_review(case_id: str):
    """
    Fetch the current cached state for a case, including its
    audit log, if it exists in the in-memory store.
    """

    if case_id not in workflow_store:
        raise HTTPException(
            status_code=404,
            detail="Case not found.",
        )

    state = workflow_store[case_id]

    return {
        "case_id": case_id,
        "review_required": state.get("review_required"),
        "review_status": state.get("review_status"),
        "audit_log": state.get("audit_log", []),
    }


@router.post("/review/resume/{case_id}", tags=["Human Review"])
def resume_workflow(case_id: str):
    """
    Re-run the resume step for a case that already has a review
    decision recorded. Mainly useful if the initial resume call
    failed and needs to be retried.
    """

    if case_id not in workflow_store:
        raise HTTPException(
            status_code=404,
            detail="Case not found.",
        )

    state = workflow_store[case_id]

    if state.get("review_status") is None:
        raise HTTPException(
            status_code=400,
            detail="No review decision recorded yet for this case.",
        )

    result = planner.resume_after_review(state)

    return {
        "case_id": case_id,
        "status": "RESUMED",
        "result": result,
    }