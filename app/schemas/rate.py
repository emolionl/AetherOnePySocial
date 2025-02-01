from pydantic import BaseModel

class RateCreate(BaseModel):
    value: float
    description: str

class RateResponse(BaseModel):
    id: int
    value: float
    description: str

    model_config = {
        "from_attributes": True
    }
