from pydantic import BaseModel 



class FeedBackRequest(BaseModel):
    user_id :str
    dish_name:str
    action:str


    