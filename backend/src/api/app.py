from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.v1.routes.recommend import router as recommend_router
from api.v1.routes.feedback import router as feedback_router
from api.v1.routes.auth import router as auth_router


#intializing the app
app = FastAPI(
    title="FoodGenie API",
    description="AI-powered Food Recommendation Engine",
    version="1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(
    recommend_router,
    prefix="/v1",
    tags=["recommendations"]
)

app.include_router(
    feedback_router,
    prefix="/v1",
    tags=["feedback"]
)

app.include_router(
    auth_router,
    prefix="/v1/auth",
    tags=["auth"]
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