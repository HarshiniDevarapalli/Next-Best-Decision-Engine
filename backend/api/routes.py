from datetime import datetime

from fastapi import APIRouter, HTTPException

from backend.services.human_review_service import HumanReviewService

workflow_store = {}

from backend.models.review import (
    HumanReviewRequest,
    HumanReviewResponse,
)

router = APIRouter(
    prefix="/review",
    tags=["Human Review"],
)

# Temporary in-memory store
# Replace with Redis/DB later
review_store = {}


@router.post(
    "/submit",
    response_model=HumanReviewResponse,
)
@router.post(
    "/submit",
    response_model=HumanReviewResponse,
)
def submit_review(request: HumanReviewRequest):

    if request.case_id not in workflow_store:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found.",
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

    workflow_store[request.case_id] = state

    return HumanReviewResponse(
        case_id=request.case_id,
        status=state["review_status"],
        message="Review recorded successfully.",
        review_timestamp=datetime.utcnow(),
    )


@router.get("/{case_id}")
def get_review(case_id: str):

    if case_id not in review_store:
        raise HTTPException(
            status_code=404,
            detail="Review not found.",
        )

    return review_store[case_id]


@router.post("/resume/{case_id}")
def resume_workflow(case_id: str):

    if case_id not in review_store:
        raise HTTPException(
            status_code=404,
            detail="Review not found.",
        )

    return {
        "case_id": case_id,
        "status": "READY_TO_RESUME",
        "review": review_store[case_id],
    }