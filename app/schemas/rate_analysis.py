from pydantic import BaseModel

class RateAnalysisCreate(BaseModel):
    rate_id: int
    analysis_id: int

class RateAnalysisResponse(BaseModel):
    id: int
    rate_id: int
    analysis_id: int

    model_config = {
        "from_attributes": True
    }
