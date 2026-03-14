from fastapi import APIRouter
from api.schemas.feedback_schema import FeedBackRequest
from reinforcement.feedback_engine import record_feedback

router = APIRouter()


@router.post("/feedback")
def feedback(request: FeedBackRequest):

    print("hello")
    
    result = record_feedback(
        user_id=request.user_id,
        dish_name=request.dish_name,
        action = request.action
    )

    return {"feedback_recorded":result}

