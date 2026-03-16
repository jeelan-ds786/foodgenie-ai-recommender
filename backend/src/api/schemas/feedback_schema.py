from pydantic import BaseModel 


class FeedbackRequest(BaseModel):
    food_id: str
    event: str


    