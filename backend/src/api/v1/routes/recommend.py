from fastapi import APIRouter

from api.schemas.recommend_schema import RecommendationRequest
from recommender.recommendation_pipeline import recommend_food

router = APIRouter()


@router.post("/recommend")
def recommend(request: RecommendationRequest):

    results = recommend_food(
        query=request.query,
        city=request.city,
        user_id=request.user_id,
        top_k=request.top_k
    )

    # detect which score column exists
    score_col = None

    if "ml_score" in results.columns:
        score_col = "ml_score"
    elif "final_score" in results.columns:
        score_col = "final_score"
    else:
        score_col = "similarity_score"

    response = results[
        ["restaurant_name", "dish_name", score_col, "city"]
    ].rename(columns={score_col: "score"}).to_dict(orient="records")

    return {
        "query": request.query,
        "city": request.city,
        "recommendations": response
    }