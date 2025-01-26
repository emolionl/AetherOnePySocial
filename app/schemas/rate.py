from pydantic import BaseModel

class RateCreate(BaseModel):
    signature: str
    description: str
    catalog_id: int

class RateResponse(BaseModel):
    id: int
    signature: str
    description: str
    catalog_id: int

    class Config:
        orm_mode = True