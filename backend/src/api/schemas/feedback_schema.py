from pydantic import BaseModel 


class FeedbackRequest(BaseModel):
    user_id: str
    food_id: str
    event: str


    