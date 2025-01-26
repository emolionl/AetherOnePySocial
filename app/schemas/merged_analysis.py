from pydantic import BaseModel

class MergedAnalysisCreate(BaseModel):
    analysis_ids: str
    user_id: int

class MergedAnalysisResponse(BaseModel):
    id: int
    analysis_ids: str
    user_id: int

    class Config:
        orm_mode = True