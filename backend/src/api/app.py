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

# V1 root endpoint
@app.get("/v1/")
def v1_root():
    return {
        "version": "1.0",
        "endpoints": [
            "POST /v1/recommend - Get food recommendations",
            "POST /v1/feedback - Submit user feedback"
        ]
    }


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}