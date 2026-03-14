from pydantic import BaseModel
from typing import Optional


class RecommendationRequest(BaseModel):

    query: str
    city: str = "Delhi"
    user_id: Optional[int] = None
    top_k: int = 10