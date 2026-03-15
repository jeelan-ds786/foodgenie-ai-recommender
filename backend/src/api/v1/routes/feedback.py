from fastapi import APIRouter
from api.schemas.feedback_schema import FeedbackRequest
from reinforcement.feedback_engine import store_feedback

router = APIRouter()


@router.post("/feedback")
def feedback(request: FeedbackRequest):

    store_feedback(
        user_id=request.user_id,
        food_id=request.food_id,
        event=request.event
    )

    return {"status": "feedback recorded"}