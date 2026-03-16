from fastapi import APIRouter
from api.schemas.feedback_schema import FeedbackRequest
from reinforcement.feedback_engine import store_feedback

router = APIRouter()


@router.post("/feedback")
def feedback(request: FeedbackRequest):

    # Use default user_id for now (auth removed)
    user_id = str(request.user_id) if hasattr(request, 'user_id') and request.user_id else "1"
    
    store_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event=request.event
    )

    return {"status": "feedback recorded", "user_id": user_id}