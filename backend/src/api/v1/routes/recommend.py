from fastapi import APIRouter

from api.schemas.recommend_schema import RecommendationRequest
from recommender.recommendation_pipeline import recommend_food


router = APIRouter()

@router.get("/")
def root():
    return {"message":"Welcome to FoodGenie AI system"}


@router.post("/recommend")
def recommend(request: RecommendationRequest):

    results = recommend_food(
        query=request.query,
        city=request.city,
        top_k=request.top_k
    )

    response = results[
        ["restaurant_name", "dish_name", "final_score", "city"]
    ].to_dict(orient="records")

    return {"recommendations": response}
