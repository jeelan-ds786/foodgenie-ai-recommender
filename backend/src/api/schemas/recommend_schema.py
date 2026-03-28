from pydantic import BaseModel
from typing import Optional, Union


class RecommendationRequest(BaseModel):

    query: str
    city: str = "Chennai"
    user_id: Optional[Union[int, str]] = None
    top_k: int = 10