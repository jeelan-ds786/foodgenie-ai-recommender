from fastapi import APIRouter

from api.schemas.recommend_schema import RecommendationRequest
from recommender.recommendation_pipeline import recommend_food

router = APIRouter()


@router.post("/recommend")
def recommend(request: RecommendationRequest):

    # Use default user_id for now (auth removed)
    user_id = request.user_id if hasattr(request, 'user_id') and request.user_id else 1
    
    results = recommend_food(
        query=request.query,
        city=request.city,
        user_id=user_id,
        top_k=request.top_k
    )

    # detect score column
    if "ml_score" in results.columns:
        score_col = "ml_score"
    elif "final_score" in results.columns:
        score_col = "final_score"
    else:
        score_col = "similarity_score"

    response = (
        results[["restaurant_name", "dish_name", score_col, "city"]]
        .rename(columns={score_col: "score"})
        .to_dict(orient="records")
    )

    return {
        "query": request.query,
        "city": request.city,
        "user_id": user_id,
        "recommendations": response
    }