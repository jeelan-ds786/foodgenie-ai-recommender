from fastapi import APIRouter
from api.schemas.feedback_schema import FeedbackRequest, FeedbackActionRequest
from reinforcement.feedback_engine import store_feedback, remove_feedback

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


@router.post("/feedback/like")
def like_food(request: FeedbackActionRequest):
    """Toggle like action for a food item"""
    user_id = str(request.user_id) if request.user_id else "1"
    
    result = store_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event="like"
    )
    
    return {
        "status": "success",
        "action": "like",
        "is_active": True,
        "food_id": request.food_id,
        "reward": result["reward"]
    }


@router.delete("/feedback/like")
def unlike_food(request: FeedbackActionRequest):
    """Remove like action for a food item"""
    user_id = str(request.user_id) if request.user_id else "1"
    
    print(f"🗑️ Removing LIKE - User: {user_id}, Food: {request.food_id}")
    
    result = remove_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event="like"
    )
    
    print(f"✅ Remove result: {result}")
    
    return {
        "status": "success" if result.get("removed") else "not_found",
        "action": "unlike",
        "is_active": False,
        "food_id": request.food_id,
        "removed": result.get("removed", False),
        "message": result.get("message", "Like removed successfully")
    }


@router.post("/feedback/skip")
def skip_food(request: FeedbackActionRequest):
    """Toggle skip action for a food item"""
    user_id = str(request.user_id) if request.user_id else "1"
    
    result = store_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event="skip"
    )
    
    return {
        "status": "success",
        "action": "skip",
        "is_active": True,
        "food_id": request.food_id,
        "reward": result["reward"]
    }


@router.delete("/feedback/skip")
def unskip_food(request: FeedbackActionRequest):
    """Remove skip action for a food item"""
    user_id = str(request.user_id) if request.user_id else "1"
    
    print(f"🗑️ Removing SKIP - User: {user_id}, Food: {request.food_id}")
    
    result = remove_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event="skip"
    )
    
    print(f"✅ Remove result: {result}")
    
    return {
        "status": "success" if result.get("removed") else "not_found",
        "action": "unskip",
        "is_active": False,
        "food_id": request.food_id,
        "removed": result.get("removed", False),
        "message": result.get("message", "Skip removed successfully")
    }


@router.post("/feedback/order")
def order_food(request: FeedbackActionRequest):
    """Toggle order action for a food item"""
    user_id = str(request.user_id) if request.user_id else "1"
    
    result = store_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event="order"
    )
    
    return {
        "status": "success",
        "action": "order",
        "is_active": True,
        "food_id": request.food_id,
        "reward": result["reward"]
    }


@router.delete("/feedback/order")
def unorder_food(request: FeedbackActionRequest):
    """Remove order action for a food item"""
    user_id = str(request.user_id) if request.user_id else "1"
    
    print(f"🗑️ Removing ORDER - User: {user_id}, Food: {request.food_id}")
    
    result = remove_feedback(
        user_id=user_id,
        food_id=request.food_id,
        event="order"
    )
    
    print(f"✅ Remove result: {result}")
    
    return {
        "status": "success" if result.get("removed") else "not_found",
        "action": "unorder",
        "is_active": False,
        "food_id": request.food_id,
        "removed": result.get("removed", False),
        "message": result.get("message", "Order removed successfully")
    }