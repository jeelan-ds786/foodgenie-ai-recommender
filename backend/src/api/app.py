from fastapi import FastAPI
from pydantic import BaseModel

from recommender.recommendation_pipeline import recommend_food
from api.v1.routes.recommend import router as recommend_router


#intializing the app
app = FastAPI(
    title="FoodGenie API",
    description="AI-powered Food Recommendation Engine",
    version="1.0"
)

app.include_router(
    recommend_router,
    prefix="/v1",
    tags=["recommendations"]
)
