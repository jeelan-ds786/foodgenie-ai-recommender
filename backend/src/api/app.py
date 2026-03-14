from fastapi import FastAPI
from pydantic import BaseModel

from api.v1.routes.recommend import router as recommend_router
from api.v1.routes.feedback import router as feedback_router


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

app.include_router(
    feedback_router,
    prefix = "/v1",
    tags=["feedback"]
)
