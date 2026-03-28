from pydantic import BaseModel 
from typing import Optional


class FeedbackRequest(BaseModel):
    food_id: str
    event: str


class FeedbackActionRequest(BaseModel):
    food_id: str
    user_id: Optional[str] = None
