from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    query:str
    city:str = "chennai"
    top_k:int = 10 

    